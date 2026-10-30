"""Cliente mínimo de Ollama. Ollama corre en Windows; desde WSL se llega por 127.0.0.1."""

from __future__ import annotations

import hashlib
import json
import time

import httpx

from . import config
from .config import Ajustes


class ErrorLLM(RuntimeError):
    pass


def objeto(**propiedades) -> dict:
    """Esquema JSON de un objeto cuyas propiedades son todas obligatorias."""
    return {"type": "object", "properties": propiedades, "required": list(propiedades)}


def lista(items: dict) -> dict:
    return {"type": "array", "items": items}


TEXTO = {"type": "string"}
ANCLAS = lista(TEXTO)


class LLM:
    def __init__(self, ajustes: Ajustes, modelo: str | None = None, pensar: bool = False):
        self.ajustes = ajustes
        self.modelo = modelo or ajustes.modelo
        self.pensar = pensar  # modo de razonamiento: más lento, más preciso (útil para el juez)
        self.cliente = httpx.Client(base_url=ajustes.ollama_url, timeout=httpx.Timeout(1200, connect=10))
        self.llamadas = 0
        self.tokens = 0
        self.segundos = 0.0

    def json(self, sistema: str, usuario: str, esquema: dict, temperatura: float | None = None, intentos: int = 3) -> dict:
        """Respuesta JSON validada por esquema. Se guarda en caché: si una corrida se interrumpe,
        lo ya generado no se vuelve a pedir (borra ~/.cache/scriptorium/llm para regenerar)."""
        temperatura = self.ajustes.temperatura if temperatura is None else temperatura
        clave = hashlib.sha1(
            json.dumps([self.modelo, self.pensar, sistema, usuario, esquema, temperatura, self.ajustes.contexto], ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()
        cache = config.TRABAJO / "llm" / f"{clave}.json"
        if cache.exists():
            try:
                return json.loads(cache.read_text(encoding="utf-8"))
            except ValueError:  # quedó a medio escribir: se vuelve a pedir
                cache.unlink()
        resultado = self._pedir_json(sistema, usuario, esquema, temperatura, intentos)
        cache.parent.mkdir(parents=True, exist_ok=True)
        temporal = cache.with_suffix(".tmp")  # escritura atómica: un corte no deja basura
        temporal.write_text(json.dumps(resultado, ensure_ascii=False), encoding="utf-8")
        temporal.replace(cache)
        return resultado

    def _post(self, ruta: str, cuerpo: dict) -> httpx.Response:
        """POST con reintentos: si el runner de Ollama se cae (p. ej. por falta de RAM), Ollama lo
        reinicia en la siguiente petición."""
        for intento in range(5):
            try:
                r = self.cliente.post(ruta, json=cuerpo)
                if r.status_code < 500:
                    return r
                error = f"{r.status_code}: {r.text[:200]}"
            except httpx.TransportError as e:
                error = repr(e)
            espera = 15 * (intento + 1)
            print(f"Ollama falló ({error}); reintento en {espera} s", flush=True)
            time.sleep(espera)
        raise ErrorLLM(f"Ollama no respondió tras 5 intentos: {error}")

    def _pedir_json(self, sistema: str, usuario: str, esquema: dict, temperatura: float, intentos: int) -> dict:
        cuerpo = {
            "model": self.modelo,
            "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": usuario}],
            "format": esquema,
            "stream": False,
            "think": self.pensar,
            "keep_alive": "15m",
            "options": {"num_ctx": self.ajustes.contexto, "temperature": temperatura},
        }
        error = None
        for _ in range(intentos):
            inicio = time.time()
            r = self._post("/api/chat", cuerpo)
            if r.status_code == 400 and "think" in r.text and "think" in cuerpo:
                cuerpo.pop("think")  # modelos sin modo de razonamiento
                continue
            if r.status_code >= 400:
                raise ErrorLLM(f"Ollama respondió {r.status_code}: {r.text[:300]}")
            datos = r.json()
            self.llamadas += 1
            self.tokens += datos.get("eval_count", 0)
            self.segundos += time.time() - inicio
            try:
                return json.loads(datos["message"]["content"])
            except json.JSONDecodeError as e:
                error = e
                cuerpo["options"]["temperature"] = min(0.6, cuerpo["options"]["temperature"] + 0.2)
        raise ErrorLLM(f"El modelo no devolvió JSON válido: {error}")

    def descargar(self) -> None:
        """Libera la VRAM para la siguiente etapa (voz, video)."""
        try:
            self.cliente.post("/api/generate", json={"model": self.modelo, "keep_alive": 0}, timeout=60)
        except httpx.HTTPError:
            pass

    def disponible(self) -> bool:
        try:
            modelos = self.cliente.get("/api/tags", timeout=10).json().get("models", [])
        except httpx.HTTPError:
            return False
        return any(m["name"] == self.modelo or m["name"] == f"{self.modelo}:latest" for m in modelos)

    def resumen_uso(self) -> str:
        velocidad = self.tokens / self.segundos if self.segundos else 0
        return f"{self.llamadas} llamadas · {self.tokens} tokens · {self.segundos:.0f} s · {velocidad:.0f} tok/s"
