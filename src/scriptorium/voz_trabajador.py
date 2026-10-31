"""Proceso trabajador de voz para los motores que clonan una voz fijada (VoxCPM2, Qwen3-TTS).

Cada motor vive en su propio venv (`~/.local/share/scriptorium/voces/<motor>`, ver
`herramientas_wsl/voces_instalar.sh`) porque pide versiones de torch/transformers que no conviven con
las del proyecto. Por eso este archivo no importa nada de `scriptorium`: `audio.Voz` lo lanza con el
python de ese venv y se queda cargado mientras dura la etapa de voz.

Protocolo: una línea JSON por pedido en stdin
    {"texto", "referencia", "texto_referencia", "salida", "semilla", "opciones"}
y una línea JSON de respuesta en stdout: {"ok": true, "segundos": ...} o {"error": "..."}.
El audio va por archivo .npy (mono, float32, 24 kHz, sin nivelar).
"""

import json
import os
import sys
import traceback

import numpy as np
import torch

TASA = 24000


class _ParadaTardia(torch.nn.Module):
    """VoxCPM2 genera por parches de 160 ms y a veces decide parar uno antes de acabar la última palabra
    («su profe-»). Cuando pide parar, se le dejan `extra` parches más: si ya había terminado sale
    silencio (que `audio._recortar` quita) y si no, termina la palabra. Y a los `limite` parches se le
    para: suelto, a veces ya no vuelve a pedirlo y tras un segundo de silencio empieza otro sonido."""

    def __init__(self, cabeza: torch.nn.Module, extra: int = 2, limite: int = 4):
        super().__init__()
        self.cabeza = cabeza
        self.extra, self.limite = extra, limite
        self.n = None  # parches desde que pidió parar por primera vez

    def forward(self, x):
        logits = self.cabeza(x)
        para = logits.argmax(dim=-1)[0].item() == 1
        if self.n is None:
            if not para:
                return logits
            self.n = 0
        else:
            self.n += 1
        if self.n < self.extra:
            quiere = False
        elif self.n >= self.limite:
            quiere = True
        else:
            return logits
        return logits if quiere == para else logits.flip(-1)  # [seguir, parar] al revés


class VoxCPM2:
    def __init__(self):
        from voxcpm import VoxCPM

        self.m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)  # Triton no soporta Pascal
        # El decodificador termina en tanh, que aplana los picos cuando la voz sale fuerte: esa es la
        # «saturación» que se oía. Sin ella la onda sale entera y se nivela después con ganancia lineal.
        dec = self.m.tts_model.audio_vae.decoder.model
        for i, capa in enumerate(dec):
            if isinstance(capa, torch.nn.Tanh):
                dec[i] = torch.nn.Identity()
        self.parada = self.m.tts_model.stop_head = _ParadaTardia(self.m.tts_model.stop_head)
        self.tasa = self.m.tts_model.sample_rate

    def decir(self, texto: str, referencia: str, texto_referencia: str, opciones: dict) -> np.ndarray:
        self.parada.n = None
        # Referencia aislada (timbre) + continuación de la misma toma (ritmo y entonación).
        return self.m.generate(text=texto, reference_wav_path=referencia, prompt_wav_path=referencia,
                               prompt_text=texto_referencia, **{"cfg_value": 2.0, "inference_timesteps": 10, **opciones})


class Qwen3:
    def __init__(self):
        from qwen_tts import Qwen3TTSModel

        # La GP100 (Pascal) no tiene bfloat16; fp16 sí es rápido en esta tarjeta.
        self.m = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0",
                                               dtype=torch.float16, attn_implementation="sdpa")
        self.idioma = next((l for l in self.m.get_supported_languages() or [] if l.lower().startswith("span")), "Spanish")
        self._prompts = {}
        self.tasa = None

    def decir(self, texto: str, referencia: str, texto_referencia: str, opciones: dict) -> np.ndarray:
        clave = (referencia, texto_referencia)
        if clave not in self._prompts:  # la referencia se codifica una sola vez
            self._prompts[clave] = self.m.create_voice_clone_prompt(ref_audio=referencia, ref_text=texto_referencia)
        wavs, self.tasa = self.m.generate_voice_clone(text=texto, language=self.idioma, voice_clone_prompt=self._prompts[clave], **opciones)
        return np.asarray(wavs[0], dtype=np.float32)


MOTORES = {"voxcpm2": VoxCPM2, "qwen3": Qwen3}


def _a_24k(audio, tasa: int) -> np.ndarray:
    import torchaudio.functional as F

    a = torch.from_numpy(np.ascontiguousarray(np.asarray(audio, dtype=np.float32).squeeze()))
    return (F.resample(a, tasa, TASA) if tasa != TASA else a).numpy()


def main() -> None:
    # Las bibliotecas escriben en stdout; el protocolo usa una copia del descriptor original y todo lo
    # demás (también lo que imprime código en C) se desvía a stderr, que va al registro.
    canal = os.fdopen(os.dup(1), "w", buffering=1, encoding="utf-8")
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    motor = MOTORES[sys.argv[1]]()
    # Los pesos pasan por la RAM antes de ir a la GPU; sin esto el proceso se queda con varios GB
    # que ya no usa (y WSL solo tiene ~8 GB para todo).
    import ctypes
    import gc

    gc.collect()
    ctypes.CDLL("libc.so.6").malloc_trim(0)
    canal.write(json.dumps({"listo": True}) + "\n")
    for linea in sys.stdin:
        try:
            p = json.loads(linea)
            torch.manual_seed(p.get("semilla", 1))
            audio = _a_24k(motor.decir(p["texto"], p["referencia"], p["texto_referencia"], p.get("opciones", {})), motor.tasa)
            if not np.isfinite(audio).all() or np.abs(audio).max() < 1e-4:
                raise RuntimeError("audio vacío o con NaN")
            temporal = p["salida"] + ".tmp.npy"
            np.save(temporal, audio)
            os.replace(temporal, p["salida"])
            canal.write(json.dumps({"ok": True, "segundos": round(len(audio) / TASA, 2)}) + "\n")
        except Exception as e:
            traceback.print_exc()
            canal.write(json.dumps({"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
