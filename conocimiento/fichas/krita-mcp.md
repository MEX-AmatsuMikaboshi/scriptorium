# Krita MCP (krita-cli)

```json
{
  "id": "krita-mcp",
  "nombre": "Krita MCP (krita-cli)",
  "tipo": "mcp",
  "areas": ["2d"],
  "prioridad": "futuro",
  "estado_local": "no-instalado",
  "capacidades": ["control-por-agente", "estilo-dibujado"],
  "resumen": "CLI y servidor MCP (50+ herramientas) para que un agente pinte en Krita: capas, trazos, rellenos y formas mediante un complemento con servidor HTTP local.",
  "lenguajes": ["Python"],
  "exporta_video": "no",
  "repo": "edithatogo/krita-cli",
  "paquetes": {"pypi": ["krita-cli"]},
  "licencia": "MIT",
  "relacionados": ["opentoonz"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
Complemento de Krita (servidor en localhost:5678) + servidor FastMCP + CLI `krita`. Otra opción: krita-codex-mcp (orientado a Codex en Windows).

## Úsalo para
- Preparar o revisar ilustraciones por capas para personajes 2D.

## No lo uses para
- Sustituir a un ilustrador: sirve para tareas acotadas.

## Instalación
```bash
uv tool install krita-cli   # además, activar el complemento en Krita y reiniciarlo
```

## Limitaciones
- Proyecto pequeño (9 estrellas).
- Krita no está instalado en el equipo.
- Un MCP que ejecuta código dentro de la aplicación puede hacer cualquier cosa que haga un script: revisa el código antes de instalarlo y no lo expongas fuera de localhost.

## En este equipo
No instalado.
