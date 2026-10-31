# MCP for Blender

```json
{
  "id": "blender-mcp",
  "nombre": "MCP for Blender",
  "tipo": "mcp",
  "areas": ["3d", "personajes"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["control-por-agente", "escena-3d"],
  "resumen": "Servidor MCP comunitario que deja a un agente leer la escena de Blender y ejecutar Python dentro de ella (objetos, materiales, render).",
  "lenguajes": ["Python"],
  "exporta_video": "no-aplica",
  "web": "https://www.mcp-for-blender.com/",
  "repo": "ahujasid/mcp-for-blender",
  "paquetes": {"pypi": ["mcp-for-blender"]},
  "licencia": "MIT",
  "agentes": "Su instalador detecta Claude Desktop, Claude Code, Codex, Cursor, VS Code, Windsurf, OpenCode y Antigravity. Cualquier cliente MCP con un modelo local (p. ej. OpenCode + Ollama) también sirve.",
  "requisitos": "uv; Blender con el complemento activado y el servidor iniciado (panel N → MCP for Blender → Start MCP Server).",
  "relacionados": ["blender", "scenario-skills"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Complemento de Blender + servidor MCP. El paquete PyPI se llamaba `blender-mcp` y ahora es `mcp-for-blender` (el nombre viejo sigue funcionando). No está afiliado a la Blender Foundation.

## Úsalo para
- Que un agente prepare escenas, materiales y renders en Blender mientras tú miras.
- Probar si un modelo local puede manejar Blender por herramientas.

## Instalación
```powershell
winget install --id=astral-sh.uv -e
uvx mcp-for-blender setup          # elige qué clientes configurar
# manual: uvx mcp-for-blender install-addon ; claude mcp add blender uvx mcp-for-blender
```
El README ofrece también `irm …/install.ps1 | iex`: no ejecutes scripts remotos sin leerlos.

## Limitaciones
- Un MCP que ejecuta código dentro de la aplicación puede hacer cualquier cosa que haga un script: revisa el código antes de instalarlo y no lo expongas fuera de localhost.
- Los modelos locales chicos fallan más al encadenar llamadas de herramientas; empezar con tareas acotadas.

## En este equipo
No instalado. uv existe en WSL; en Windows habría que instalarlo (winget). Pedir autorización antes.
