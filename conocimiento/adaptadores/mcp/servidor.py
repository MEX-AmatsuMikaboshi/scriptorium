#!/usr/bin/env python3
"""Servidor MCP (stdio, JSON-RPC por líneas) de la biblioteca de conocimiento audiovisual.

Solo biblioteca estándar. Expone las mismas funciones que la CLI «saber»: buscar, ver, contexto y capacidades.
Registro (ejemplos en adaptadores/README.md):
    claude mcp add saber -- python3 /home/gaber/scriptorium/conocimiento/adaptadores/mcp/servidor.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "herramientas"))
import saber  # noqa: E402

VERSION_PROTOCOLO = "2025-06-18"
INSTRUCCIONES = ("Biblioteca local de conocimiento para hacer video y animación con código. Antes de diseñar o programar "
                 "una animación, llama a «buscar» con la petición en lenguaje natural; luego «ver» la técnica y las "
                 "herramientas sugeridas, o «contexto» para un paquete listo. No inventes herramientas que no aparezcan.")
HERRAMIENTAS = [
    {"name": "buscar",
     "description": "Busca técnicas, herramientas, flujos, recetas de código, principios de diseño y documentación local "
                    "para una petición de animación o video en lenguaje natural (español o inglés), aunque no se sepa el "
                    "nombre de ninguna librería. Ejemplo: «quiero animar letras una por una».",
     "inputSchema": {"type": "object", "properties": {
         "consulta": {"type": "string", "description": "Lo que se quiere lograr."},
         "limite": {"type": "integer", "description": "Resultados por grupo (5 por defecto)."}}, "required": ["consulta"]}},
    {"name": "ver",
     "description": "Devuelve un documento por su id (ficha de herramienta, técnica, principio, flujo o receta como canvas2d/golpe).",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string"},
         "breve": {"type": "boolean", "description": "Solo lo esencial (útil para modelos con poco contexto)."}}, "required": ["id"]}},
    {"name": "contexto",
     "description": "Arma un paquete de contexto en Markdown (flujo, técnica, herramientas, lista de control, recetas) "
                    "para una petición, sin pasarse de un presupuesto aproximado de tokens.",
     "inputSchema": {"type": "object", "properties": {
         "peticion": {"type": "string"},
         "tokens": {"type": "integer", "description": "Presupuesto aproximado (3500 por defecto)."}}, "required": ["peticion"]}},
    {"name": "capacidades",
     "description": "Lista la taxonomía de capacidades (qué se puede pedir) y cuántos recursos tiene cada una.",
     "inputSchema": {"type": "object", "properties": {}}},
]


def llamar(nombre: str, args: dict) -> str:
    if nombre == "buscar":
        return saber.formatear_busqueda(saber.buscar(str(args["consulta"]), int(args.get("limite") or 5)))
    if nombre == "ver":
        return saber.ver(str(args["id"]), bool(args.get("breve")))
    if nombre == "contexto":
        return saber.contexto(str(args["peticion"]), int(args.get("tokens") or 3500))
    if nombre == "capacidades":
        return saber.listar_capacidades()
    raise ValueError(f"herramienta desconocida: {nombre}")


def responder(ident, resultado=None, error=None) -> None:
    mensaje = {"jsonrpc": "2.0", "id": ident}
    if error is not None:
        mensaje["error"] = error
    else:
        mensaje["result"] = resultado
    sys.stdout.write(json.dumps(mensaje, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main() -> None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    for linea in sys.stdin:
        if not linea.strip():
            continue
        try:
            mensaje = json.loads(linea)
        except json.JSONDecodeError:
            responder(None, error={"code": -32700, "message": "JSON inválido"})
            continue
        metodo, ident = mensaje.get("method"), mensaje.get("id")
        if ident is None:  # notificaciones (initialized, cancelled): no llevan respuesta
            continue
        params = mensaje.get("params") or {}
        if metodo == "initialize":
            responder(ident, {"protocolVersion": params.get("protocolVersion", VERSION_PROTOCOLO),
                              "capabilities": {"tools": {}},
                              "serverInfo": {"name": "saber-audiovisual", "version": "1.0.0"},
                              "instructions": INSTRUCCIONES})
        elif metodo == "ping":
            responder(ident, {})
        elif metodo == "tools/list":
            responder(ident, {"tools": HERRAMIENTAS})
        elif metodo == "tools/call":
            try:
                texto = llamar(params.get("name", ""), params.get("arguments") or {})
                responder(ident, {"content": [{"type": "text", "text": texto}], "isError": False})
            except Exception as e:  # el error vuelve al modelo como texto, el servidor sigue vivo
                responder(ident, {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True})
        else:
            responder(ident, error={"code": -32601, "message": f"Método no soportado: {metodo}"})


if __name__ == "__main__":
    main()
