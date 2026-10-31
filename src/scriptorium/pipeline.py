"""Orquestador. Ejecuta las etapas por lotes —todo el LLM, luego la voz, luego el video—
para que en la VRAM de la GPU solo haya un modelo a la vez."""

from __future__ import annotations

import time

from rich.console import Console

from . import config, publicar, textos
from .config import Ajustes
from .ingesta import Obra, ingerir, listar_obras
from .llm import LLM, ErrorLLM

consola = Console()
FORMATOS = ("texto", "interactivo", "audio", "video")


def avisar(mensaje: str) -> None:
    consola.log(mensaje)


def etapa_texto(obras: list[Obra], ajustes: Ajustes, forzar: bool, con_video: bool, forzar_video: bool = False) -> None:
    llm = LLM(ajustes)
    if not llm.disponible():
        raise ErrorLLM(f"El modelo {ajustes.modelo} no está en Ollama. Instálalo con: ollama pull {ajustes.modelo}")
    for obra in obras:
        derivados = textos.cargar(obra)
        if derivados is None or forzar:
            consola.rule(f"[bold]Texto · {obra.meta['titulo']}")
            inicio = time.time()
            derivados = [textos.derivar_capitulo(llm, obra, cap, ajustes, avisar) for cap in obra.capitulos()]
            textos.guardar(obra, derivados)
            avisar(f"texto listo en {time.time() - inicio:.0f} s · {llm.resumen_uso()}")
        publicar.escribir_textos(obra, derivados)
        if con_video:
            from . import video

            video.dirigir(llm, obra, derivados, forzar or forzar_video, avisar)
    llm.descargar()


def etapa_audio(obras: list[Obra], ajustes: Ajustes, con_audio: bool, forzar: bool, con_video: bool) -> None:
    from . import audio

    with audio.Voz(ajustes, avisar) as voz:
        for obra in obras:
            consola.rule(f"[bold]Voz · {obra.meta['titulo']}")
            if con_audio:
                audio.producir(voz, obra, textos.cargar(obra) or [], forzar, avisar)
            if con_video:
                from . import video

                video.narrar(voz, obra, forzar, avisar)


def etapa_interactivos(obras: list[Obra]) -> None:
    from . import interactivo

    for obra in obras:
        consola.rule(f"[bold]Interactivos · {obra.meta['titulo']}")
        interactivo.producir(obra, textos.cargar(obra) or [], avisar)


def etapa_video(obras: list[Obra], ajustes: Ajustes, forzar: bool) -> None:
    from . import video

    for obra in obras:
        consola.rule(f"[bold]Video · {obra.meta['titulo']}")
        video.renderizar(obra, ajustes, forzar, avisar)


def generar(slugs: list[str], formatos: list[str], forzar: bool = False) -> None:
    config.preparar_carpetas()
    ajustes = config.cargar_ajustes()
    obras = [Obra.cargar(s) for s in slugs]
    con_video = "video" in formatos
    inicio = time.time()
    # El texto es la base de todo lo demás: si falta, se genera aunque no se pida.
    etapa_texto(obras, ajustes, forzar and "texto" in formatos, con_video, forzar and con_video)
    if "audio" in formatos or con_video:
        etapa_audio(obras, ajustes, "audio" in formatos, forzar, con_video)
    etapa_interactivos(obras)
    if con_video:
        etapa_video(obras, ajustes, forzar)
    from . import biblioteca

    biblioteca.construir()
    consola.rule(f"[bold green]Listo en {(time.time() - inicio) / 60:.1f} min")


def pendientes_de_entrada() -> list:
    ingeridos = set()
    for slug in listar_obras():
        ingeridos.add(Obra.cargar(slug).meta.get("archivo_original"))
    from .ingesta import FORMATOS as ACEPTADOS

    return [p for p in sorted(config.ENTRADA.iterdir()) if p.suffix.lower() in ACEPTADOS and p.name not in ingeridos]


def noche(formatos: list[str] | None = None) -> None:
    """Ingiere todo lo nuevo de 00_entrada y genera todos los formatos."""
    config.preparar_carpetas()
    nuevas = []
    for archivo in pendientes_de_entrada():
        consola.log(f"Ingiriendo {archivo.name}")
        try:
            nuevas.append(ingerir(archivo).slug)
        except Exception as e:  # un archivo dañado no detiene la cola
            consola.log(f"[red]No pude ingerir {archivo.name}: {e}")
    if nuevas:
        generar(nuevas, formatos or list(FORMATOS))
    else:
        consola.log("No hay archivos nuevos en 00_entrada.")
