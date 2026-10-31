"""Cata de voces: genera los mismos textos con un motor candidato.

Se ejecuta con el python del venv de cada motor (ver voces_instalar.sh):
    <venv>/bin/python cata_voces.py <motor> <carpeta_salida>
Motores: qwen3, voxcpm2, chatterbox, omnivoice, kokoro (este con el venv principal).
Qwen3 va primero: su voz diseñada por descripción (sintética, de nadie real) es la referencia de los
motores que clonan (Chatterbox LatAm y OmniVoice).
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

TEXTOS = {
    "narracion": (
        "¿Cómo podemos alcanzar el conocimiento de la verdad? Para Balmes, el primer medio es atender. "
        "Pero la atención no es una fijeza de espíritu que clava la mente sobre los objetos: es una aplicación "
        "suave y reposada, que nos deja la agilidad necesaria para pasar sin esfuerzo de unas ocupaciones a otras."
    ),
    "lectura": (
        "Tan lejos estoy de considerar la atención como abstracción severa y continuada, que, muy al contrario, "
        "cuento en el número de los distraídos no sólo a los atolondrados, sino también a los ensimismados. "
        "Aquéllos se derraman por la parte de afuera; éstos divagan por las tenebrosas regiones de adentro."
    ),
}
REFERENCIA = "Bienvenidos. Hoy vamos a leer juntos a un autor clásico, con calma, prestando atención a cada idea."
DISENO = {
    "m": "Male narrator in his forties from Mexico, neutral Latin American Spanish accent, warm and deep voice, "
    "calm and engaging documentary storytelling tone, natural pauses and expressive intonation.",
    "f": "Female narrator in her thirties from Mexico, neutral Latin American Spanish accent, warm and clear voice, "
    "friendly and engaging educational tone, natural pauses and expressive intonation.",
}
# La GP100 (Pascal) no tiene bfloat16; fp16 sí es rápido en esta tarjeta (y fp32 queda de respaldo).
DTYPE = torch.float16


def guardar(salida: Path, nombre: str, audio, tasa: int, inicio: float, registro: dict) -> None:
    audio = np.asarray(audio.detach().cpu() if hasattr(audio, "detach") else audio, dtype=np.float32).squeeze()
    if not np.isfinite(audio).all() or np.abs(audio).max() < 1e-4:
        raise RuntimeError(f"{nombre}: audio vacío o con NaN")
    sf.write(salida / f"{nombre}.wav", audio, tasa)
    segundos = len(audio) / tasa
    registro[nombre] = {"segundos": round(segundos, 1), "rtf": round((time.time() - inicio) / segundos, 2)}
    print(f"  {nombre}: {segundos:.1f} s de audio en {time.time() - inicio:.1f} s", flush=True)


def qwen3(salida: Path, registro: dict) -> None:
    from qwen_tts import Qwen3TTSModel

    for dtype in (DTYPE, torch.float32):
        try:
            m = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cuda:0", dtype=dtype, attn_implementation="sdpa")
            idioma = next((l for l in m.get_supported_languages() if l.lower().startswith("span")), "Spanish")
            for g, instruct in DISENO.items():
                wavs, sr = m.generate_voice_design(text=REFERENCIA, instruct=instruct, language=idioma)
                guardar(salida, f"referencia_{g}", wavs[0], sr, time.time(), {})
                for clave, texto in TEXTOS.items():
                    t = time.time()
                    wavs, sr = m.generate_voice_design(text=texto, instruct=instruct, language=idioma)
                    guardar(salida, f"qwen3_{g}_{clave}", wavs[0], sr, t, registro)
            registro["_dtype"] = str(dtype)
            return
        except RuntimeError as e:
            print(f"  qwen3 en {dtype} falló ({e}); reintento", flush=True)
            m = None
            torch.cuda.empty_cache()
    raise RuntimeError("qwen3 no generó audio")


def voxcpm2(salida: Path, registro: dict) -> None:
    from voxcpm import VoxCPM

    m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)  # torch.compile/Triton no soporta Pascal
    disenos = {
        "m": "(Mexican male narrator in his forties, warm deep voice, calm documentary tone, neutral Latin American Spanish accent)",
        "f": "(Mexican female narrator in her thirties, warm clear voice, friendly educational tone, neutral Latin American Spanish accent)",
    }
    for g, d in disenos.items():
        for clave, texto in TEXTOS.items():
            t = time.time()
            wav = m.generate(text=d + texto, cfg_value=2.0, inference_timesteps=10)
            guardar(salida, f"voxcpm2_{g}_{clave}", wav, m.tts_model.sample_rate, t, registro)


def chatterbox(salida: Path, registro: dict) -> None:
    from huggingface_hub import snapshot_download
    import chatterbox.mtl_tts as mtl

    base = Path(snapshot_download("ResembleAI/chatterbox", allow_patterns=["ve.pt", "conds.pt", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json", "Cangjie5_TC.json"]))
    latam = Path(snapshot_download("ResembleAI/Chatterbox-Multilingual-es-mx-latam"))
    local = Path.home() / ".cache/scriptorium/chatterbox-latam"  # t3 LatAm + codificador y vocoder del base
    local.mkdir(parents=True, exist_ok=True)
    # El s3gen_v3 del paquete LatAm no trae los búferes del tokenizador; se usa el s3gen del base, el mismo
    # que carga from_pretrained para los modelos v3.
    enlaces = {n: base / n for n in ("ve.pt", "conds.pt", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json", "Cangjie5_TC.json")}
    enlaces["t3_es_mx_latam.safetensors"] = latam / "t3_es_mx_latam.safetensors"
    for nombre, origen in enlaces.items():
        destino = local / nombre
        if destino.is_symlink() or destino.exists():
            destino.unlink()
        destino.symlink_to(origen.resolve())
    mtl._resolve_multilingual_t3_model = lambda nombre: nombre  # admite el archivo del paquete LatAm
    m = mtl.ChatterboxMultilingualTTS.from_local(local, "cuda", t3_model="t3_es_mx_latam.safetensors")
    for g in DISENO:
        for clave, texto in TEXTOS.items():
            t = time.time()
            wav = m.generate(texto, language_id="es", audio_prompt_path=str(salida / f"referencia_{g}.wav"), exaggeration=0.6, cfg_weight=0.4)
            guardar(salida, f"chatterbox_{g}_{clave}", wav, m.sr, t, registro)


def omnivoice(salida: Path, registro: dict) -> None:
    from omnivoice import OmniVoice

    m = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=DTYPE)
    tasa = getattr(m, "sampling_rate", None) or getattr(getattr(m, "config", None), "sampling_rate", None) or 24000
    for g in DISENO:
        for clave, texto in TEXTOS.items():
            t = time.time()
            wavs = m.generate(text=texto, language="es", ref_audio=str(salida / f"referencia_{g}.wav"), ref_text=REFERENCIA)
            guardar(salida, f"omnivoice_{g}_{clave}", wavs[0], tasa, t, registro)


def kokoro(salida: Path, registro: dict) -> None:
    from scriptorium import config
    from scriptorium.audio import TASA, Voz

    with Voz(config.cargar_ajustes()) as voz:
        for g, nombre in {"m": "em_alex", "f": "ef_dora"}.items():
            for clave, texto in TEXTOS.items():
                t = time.time()
                guardar(salida, f"kokoro_{g}_{clave}", voz.decir(texto, voz=nombre), TASA, t, registro)


if __name__ == "__main__":
    motor, salida = sys.argv[1], Path(sys.argv[2])
    salida.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "120")
    registro: dict = {}
    inicio = time.time()
    globals()[motor](salida, registro)
    registro["_total_s"] = round(time.time() - inicio)
    (salida / f"registro_{motor}.json").write_text(json.dumps(registro, indent=2), encoding="utf-8")
