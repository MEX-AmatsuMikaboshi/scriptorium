"""Rutas y ajustes de Scriptorium.

Los ajustes por defecto viven aquí; el usuario puede sobrescribirlos editando
`ajustes.json` en la carpeta de datos (D:\\Scriptorium en Windows).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

PROYECTO = Path(__file__).resolve().parents[2]
KIT_VIDEO = PROYECTO / "video"
DATOS = Path(os.environ.get("SCRIPTORIUM_DATOS", "/mnt/d/Scriptorium"))
ENTRADA = DATOS / "00_entrada"
CANONICO = DATOS / "01_canonico"
DERIVADOS = DATOS / "02_derivados"
BIBLIOTECA = DATOS / "03_biblioteca"
# Archivos intermedios en el disco de Linux (mucho más rápido que el disco USB).
TRABAJO = Path.home() / ".cache" / "scriptorium"
# Voces fijadas (referencia sintética + motor que la clona) y los venvs de esos motores.
VOCES = PROYECTO / "voces"
ENTORNOS_VOZ = Path.home() / ".local" / "share" / "scriptorium" / "voces"


@dataclass
class Ajustes:
    ollama_url: str = "http://127.0.0.1:11434"
    modelo: str = "gemma4:12b"
    modelo_juez: str = "gemma4:12b"
    contexto: int = 16384
    temperatura: float = 0.2
    # Una voz fijada de voces/voces.json o un nombre de Kokoro (em_alex, ef_dora).
    voz_narrador: str = "narrador"
    voz_anfitrion: str = "anfitriona"
    velocidad_voz: float = 1.0  # solo Kokoro
    video_fps: int = 60
    video_ancho: int = 1920
    video_alto: int = 1080
    video_hilos: int = 8
    palabras_por_bloque: int = 5000


def cargar_ajustes() -> Ajustes:
    ajustes = Ajustes()
    archivo = DATOS / "ajustes.json"
    if archivo.exists():
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        validos = {f.name for f in fields(Ajustes)}
        for clave, valor in datos.items():
            if clave in validos:
                setattr(ajustes, clave, valor)
    return ajustes


def guardar_ajustes_por_defecto() -> None:
    archivo = DATOS / "ajustes.json"
    if not archivo.exists():
        archivo.write_text(json.dumps(asdict(Ajustes()), indent=2, ensure_ascii=False), encoding="utf-8")


def preparar_carpetas() -> None:
    for carpeta in (ENTRADA, CANONICO, DERIVADOS, BIBLIOTECA, TRABAJO):
        carpeta.mkdir(parents=True, exist_ok=True)
    guardar_ajustes_por_defecto()


def ruta_desde_windows(ruta: str) -> Path:
    """Acepta rutas de Windows (D:\\libros\\x.pdf) y las traduce a /mnt/d/libros/x.pdf."""
    m = re.match(r"^([A-Za-z]):[\\/](.*)$", ruta)
    if m:
        return Path(f"/mnt/{m.group(1).lower()}") / m.group(2).replace("\\", "/")
    return Path(ruta).expanduser()


def ruta_para_windows(ruta: Path) -> str:
    m = re.match(r"^/mnt/([a-z])/(.*)$", str(ruta))
    if m:
        return f"{m.group(1).upper()}:\\" + m.group(2).replace("/", "\\")
    return str(ruta)
