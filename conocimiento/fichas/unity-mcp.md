# Unity MCP

```json
{
  "id": "unity-mcp",
  "nombre": "Unity MCP",
  "tipo": "mcp",
  "areas": ["3d"],
  "prioridad": "futuro",
  "estado_local": "no-instalado",
  "capacidades": ["control-por-agente", "escena-3d"],
  "resumen": "Puente MCP entre agentes y el editor de Unity: gestionar assets, controlar escenas, editar scripts y automatizar tareas.",
  "lenguajes": ["C#", "Python"],
  "exporta_video": "no-aplica",
  "web": "https://coplaydev.github.io/unity-mcp/",
  "repo": "CoplayDev/unity-mcp",
  "licencia": "MIT",
  "agentes": "Cualquier cliente MCP (Claude Desktop y Code, Cursor, VS Code, Windsurf, Cline, Gemini CLI…).",
  "requisitos": "Unity 2021.3 LTS a 6.x; Python 3.10+ con uv.",
  "relacionados": ["unity"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Paquete de Unity + servidor MCP en Python.

## Úsalo para
- Automatizar una escena de Unity desde un agente.

## Instalación
Unity → Package Manager → Add package from git URL (la URL está en su README).

## Limitaciones
- Un MCP que ejecuta código dentro de la aplicación puede hacer cualquier cosa que haga un script: revisa el código antes de instalarlo y no lo expongas fuera de localhost.

## En este equipo
No instalado. Compatible con las dos versiones de Unity del equipo.
