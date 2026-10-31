"""Alineación forzada palabra por palabra y transcripción de control (wav2vec2 CTC en español).

Sirve para que lo que se ilumina en pantalla sea exactamente lo que dice la voz y en el momento en
que lo dice, y para detectar cuándo la voz sintética se come o añade palabras.
"""

from __future__ import annotations

import difflib
import re
import unicodedata

import numpy as np

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"
TASA_MODELO = 16000


def sin_acentos(s: str) -> str:
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()


def norma(palabra: str) -> str:
    """Forma comparable de una palabra: minúsculas, sin acentos ni signos."""
    return re.sub(r"[^a-z0-9]", "", sin_acentos(palabra.lower()))


def emparejar(mostradas: list[str], dichas: list[str]) -> list[int | None]:
    """Para cada palabra mostrada, el índice de la palabra dicha que le corresponde (en orden) o None."""
    a, b = [norma(p) for p in mostradas], [norma(p) for p in dichas]
    pares: list[int | None] = [None] * len(a)
    for bloque in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(bloque.size):
            if a[bloque.a + k]:
                pares[bloque.a + k] = bloque.b + k
    return pares


def _remuestrear(audio: np.ndarray, tasa: int) -> np.ndarray:
    """Remuestreo de banda limitada por FFT (clips de pocos segundos)."""
    audio = np.asarray(audio, dtype=np.float64)
    if tasa == TASA_MODELO or len(audio) == 0:
        return audio.astype(np.float32)
    n = int(round(len(audio) * TASA_MODELO / tasa))
    espectro = np.fft.rfft(audio)[: n // 2 + 1]
    return (np.fft.irfft(espectro, n) * n / len(audio)).astype(np.float32)


def _viterbi(lp: np.ndarray, fichas: list[int], blanco: int) -> np.ndarray | None:
    """Camino CTC más probable: estado por cuadro (impar = ficha (s-1)//2, par = blanco)."""
    cuadros = lp.shape[0]
    ext = np.full(2 * len(fichas) + 1, blanco)
    ext[1::2] = fichas
    estados = len(ext)
    if cuadros < len(fichas):
        return None
    emis = lp[:, ext]
    salto = np.zeros(estados, bool)  # de s-2 a s: solo entre fichas distintas
    salto[3::2] = ext[3::2] != ext[1:-2:2]
    dp = np.full(estados, -np.inf)
    dp[0] = emis[0, 0]
    if estados > 1:
        dp[1] = emis[0, 1]
    atras = np.zeros((cuadros, estados), np.int8)
    menos_inf = np.array([-np.inf, -np.inf])
    for t in range(1, cuadros):
        opciones = np.stack([dp, np.concatenate((menos_inf[:1], dp[:-1])), np.where(salto, np.concatenate((menos_inf, dp[:-2])), -np.inf)])
        eleccion = opciones.argmax(0)
        dp = opciones[eleccion, np.arange(estados)] + emis[t]
        atras[t] = eleccion
    s = estados - 1 if estados == 1 or dp[-1] >= dp[-2] else estados - 2
    if not np.isfinite(dp[s]):
        return None
    camino = np.empty(cuadros, int)
    for t in range(cuadros - 1, -1, -1):
        camino[t] = s
        s -= int(atras[t, s])
    return camino


class Alineador:
    """wav2vec2 en la GPU; una sola pasada da los tiempos de cada palabra y una transcripción."""

    def __init__(self):
        self._modelo = None

    def __enter__(self) -> "Alineador":
        return self

    def __exit__(self, *exc) -> None:
        if self._modelo is not None:
            import torch

            self._modelo = None
            torch.cuda.empty_cache()

    def _cargar(self):
        if self._modelo is None:
            import torch
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

            self._dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
            self._procesador = Wav2Vec2Processor.from_pretrained(MODELO)
            self._modelo = Wav2Vec2ForCTC.from_pretrained(MODELO).to(self._dispositivo).eval()
            vocab = self._procesador.tokenizer.get_vocab()
            self._vocab = vocab
            self._letras = {i: c for c, i in vocab.items()}
            self._blanco = self._procesador.tokenizer.pad_token_id
            self._separador = vocab.get("|")
        return self._modelo

    def _fichas(self, palabra: str) -> list[int]:
        """Fichas del modelo para una palabra mostrada; los números se alinean dichos en letra."""
        from .audio import _numero

        hablada = re.sub(r"\d+", lambda m: f" {_numero(int(m.group()))} ", palabra.lower())
        fichas: list[int] = []
        for c in hablada:
            if c == " ":
                if fichas and self._separador is not None and fichas[-1] != self._separador:
                    fichas.append(self._separador)
            elif c in self._vocab:
                fichas.append(self._vocab[c])
            elif sin_acentos(c) in self._vocab:
                fichas.append(self._vocab[sin_acentos(c)])
        while fichas and fichas[-1] == self._separador:
            fichas.pop()
        return fichas

    def analizar(self, audio: np.ndarray, tasa: int, palabras: list[str]) -> tuple[list[dict | None], str]:
        """Tiempos (s) de cada palabra dada y transcripción de lo que realmente se oye."""
        import torch

        modelo = self._cargar()
        senal = _remuestrear(audio, tasa)
        entrada = self._procesador(senal, sampling_rate=TASA_MODELO, return_tensors="pt").input_values.to(self._dispositivo)
        with torch.inference_mode():
            lp = torch.log_softmax(modelo(entrada).logits[0].float(), -1).cpu().numpy()
        por_cuadro = len(senal) / TASA_MODELO / lp.shape[0]

        ids = lp.argmax(-1)
        colapsados = [int(i) for k, i in enumerate(ids) if (k == 0 or i != ids[k - 1]) and i != self._blanco]
        transcripcion = re.sub(r"\s+", " ", "".join(self._letras.get(i, "") for i in colapsados).replace("|", " ")).strip()

        fichas, duenos = [], []  # duenos[k] = palabra a la que pertenece la ficha k (None = separador)
        for n, palabra in enumerate(palabras):
            propias = self._fichas(palabra)
            if not propias:
                continue
            if fichas and self._separador is not None:
                fichas.append(self._separador)
                duenos.append(None)
            fichas += propias
            duenos += [n if f != self._separador else None for f in propias]
        tiempos: list[dict | None] = [None] * len(palabras)
        camino = _viterbi(lp, fichas, self._blanco) if fichas else None
        if camino is None:
            return tiempos, transcripcion
        for k in range(len(fichas)):
            cuadros = np.nonzero(camino == 2 * k + 1)[0]
            n = duenos[k]
            if n is None or not len(cuadros):
                continue
            confianza = float(np.exp(lp[cuadros, fichas[k]]).mean())
            t = tiempos[n]
            if t is None:
                tiempos[n] = {"inicio": cuadros[0] * por_cuadro, "fin": (cuadros[-1] + 1) * por_cuadro, "confianza": [confianza]}
            else:
                t["fin"] = (cuadros[-1] + 1) * por_cuadro
                t["confianza"].append(confianza)
        for t in tiempos:
            if t is not None:
                t["confianza"] = round(float(np.mean(t["confianza"])), 3)
                t["inicio"], t["fin"] = round(t["inicio"], 3), round(t["fin"], 3)
        return tiempos, transcripcion


def _sonido(palabra: str) -> str:
    """Forma fonética aproximada del español (seseo, b/v, ll/y, h muda), para no confundir errores de
    ortografía del reconocedor («valmes») con palabras que la voz no dijo."""
    p = norma(palabra)
    for a, b in (("v", "b"), ("z", "s"), ("ce", "se"), ("ci", "si"), ("ll", "y"), ("qu", "k"), ("c", "k"), ("w", "u")):
        p = p.replace(a, b)
    return p.replace("h", "")


def palabras_perdidas(esperado: str, transcripcion: str) -> tuple[float, list[str], list[str]]:
    """Fracción de palabras esperadas que no se oyen, y cuáles faltan o sobran (control de la voz)."""
    a = [_sonido(p) for p in esperado.split() if norma(p)]
    b = [_sonido(p) for p in transcripcion.split() if norma(p)]
    faltan, sobran = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "replace" and "".join(a[i1:i2]) == "".join(b[j1:j2]):
            continue  # solo cambian los espacios: «por qué» se oye «porque», «sobre todo», «sobretodo»
        if op in ("delete", "replace"):
            faltan += a[i1:i2]
        if op in ("insert", "replace"):
            sobran += b[j1:j2]
    if len(faltan) < 2:  # un nombre propio mal reconocido no es una palabra perdida
        return 0.0, faltan, sobran
    return (len(faltan) / len(a) if a else 0.0), faltan, sobran
