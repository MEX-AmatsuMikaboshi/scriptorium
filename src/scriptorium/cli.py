"""Comandos de Scriptorium.

    scriptorium ingerir <archivo> [--titulo T] [--autor A]
    scriptorium generar <obra|todo> [--formatos texto,interactivo,audio,video] [--forzar]
    scriptorium noche
    scriptorium biblioteca
    scriptorium voces
    scriptorium estado
    scriptorium saber <buscar|ver|contexto|…>   (biblioteca de conocimiento audiovisual: conocimiento/)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from rich.table import Table

from . import config
from .ingesta import Obra, ingerir, listar_obras
from .pipeline import FORMATOS, consola, generar, noche, pendientes_de_entrada


def _obras(nombre: str) -> list[str]:
    todas = listar_obras()
    if nombre == "todo":
        return todas
    if nombre.lower() in todas:  # el slug exacto gana: «balmes-el-criterio» no arrastra a «jaime-balmes-…»
        return [nombre.lower()]
    coincidencias = [s for s in todas if nombre.lower() in s]
    if not coincidencias:
        consola.print(f"[red]No encontré la obra «{nombre}». Obras: {', '.join(todas) or '(ninguna)'}")
        sys.exit(1)
    return coincidencias


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["saber"]:  # la biblioteca es independiente (solo biblioteca estándar): se le pasan los argumentos tal cual
        saber = Path(__file__).resolve().parents[2] / "conocimiento" / "herramientas" / "saber.py"
        sys.exit(subprocess.run([sys.executable, str(saber), *argv[1:]]).returncode)
    p = argparse.ArgumentParser(prog="scriptorium", description="Fábrica local de contenido de humanidades.")
    sub = p.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("ingerir", help="Convierte un archivo en texto canónico con IDs.")
    s.add_argument("archivo")
    s.add_argument("--titulo")
    s.add_argument("--autor")

    s = sub.add_parser("generar", help="Genera los formatos de una obra.")
    s.add_argument("obra", help="slug (o parte) de la obra, o «todo»")
    s.add_argument("--formatos", default=",".join(FORMATOS))
    s.add_argument("--forzar", action="store_true", help="rehace aunque ya exista")

    sub.add_parser("noche", help="Procesa todo lo nuevo de 00_entrada.")
    sub.add_parser("biblioteca", help="Reconstruye el sitio de la biblioteca.")
    sub.add_parser("voces", help="Genera la cata de voces.")
    sub.add_parser("estado", help="Muestra obras y productos.")
    s = sub.add_parser("comparar", help="Prueba de fidelidad entre modelos de Ollama.")
    s.add_argument("obra")
    s.add_argument("--modelos", default="gemma4:12b,qwen3:14b")
    sub.add_parser("saber", help="Biblioteca de conocimiento audiovisual (scriptorium saber --help).")

    a = p.parse_args(argv)
    config.preparar_carpetas()

    if a.comando == "ingerir":
        obra = ingerir(config.ruta_desde_windows(a.archivo), a.titulo, a.autor)
        consola.print(f"[green]Obra «{obra.meta['titulo']}» → {obra.slug} ({obra.meta['parrafos']} párrafos, {obra.meta['palabras']} palabras)")
    elif a.comando == "generar":
        formatos = [f.strip() for f in a.formatos.split(",") if f.strip()]
        desconocidos = set(formatos) - set(FORMATOS)
        if desconocidos:
            consola.print(f"[red]Formatos desconocidos: {', '.join(desconocidos)}. Usa: {', '.join(FORMATOS)}")
            sys.exit(1)
        generar(_obras(a.obra), formatos, a.forzar)
    elif a.comando == "noche":
        noche()
    elif a.comando == "biblioteca":
        from . import biblioteca

        consola.print(f"[green]Biblioteca: {config.ruta_para_windows(biblioteca.construir())}")
    elif a.comando == "voces":
        from . import audio

        consola.print(f"[green]Cata de voces: {config.ruta_para_windows(audio.cata_de_voces(config.cargar_ajustes()))}")
    elif a.comando == "comparar":
        from .comparar import comparar
        from .pipeline import avisar

        destino = comparar(_obras(a.obra)[0], [m.strip() for m in a.modelos.split(",")], avisar)
        consola.print(destino.read_text(encoding="utf-8"))
    elif a.comando == "estado":
        tabla = Table("obra", "título", "párrafos", "productos")
        for slug in listar_obras():
            obra = Obra.cargar(slug)
            from .publicar import manifiesto

            tabla.add_row(slug, obra.meta["titulo"], str(obra.meta["parrafos"]), str(len(manifiesto(obra)["productos"])))
        consola.print(tabla)
        pendientes = pendientes_de_entrada()
        if pendientes:
            consola.print(f"Pendientes en 00_entrada: {', '.join(x.name for x in pendientes)}")


if __name__ == "__main__":
    main()
