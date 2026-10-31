# opentoonz-mcp

```json
{
  "id": "opentoonz-mcp",
  "nombre": "opentoonz-mcp",
  "tipo": "mcp",
  "areas": ["2d", "anime"],
  "prioridad": "futuro",
  "estado_local": "no-instalado",
  "capacidades": ["control-por-agente", "animacion-tradicional"],
  "resumen": "Servidor MCP que automatiza OpenToonz sin interfaz: corre su motor de scripts en modo CLI y renderiza con tcomposer → PNG → ffmpeg → MP4.",
  "lenguajes": ["Python"],
  "exporta_video": "si",
  "repo": "c0d33ngr/opentoonz-mcp",
  "licencia": "MIT",
  "requisitos": "OpenToonz 1.x con tcomposer; en Linux funciona mejor un AppImage extraído.",
  "relacionados": ["opentoonz"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Herramientas como `opentoonz_health`, `opentoonz_doctor`, `opentoonz_render_batch` y `opentoonz_run_script` (JavaScript arbitrario de OpenToonz). Es lo más parecido al «OpenToonz Headless con JSON-RPC» que mencionaba ChatGPT (ese proyecto no se encontró).

## Úsalo para
- Render por lotes de escenas de OpenToonz desde un agente.

## Limitaciones
- Muy nuevo (1 estrella, octubre de 2026).
- Un MCP que ejecuta código dentro de la aplicación puede hacer cualquier cosa que haga un script: revisa el código antes de instalarlo y no lo expongas fuera de localhost.

## En este equipo
No instalado.
