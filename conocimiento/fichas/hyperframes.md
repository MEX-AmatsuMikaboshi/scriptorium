# HyperFrames

```json
{
  "id": "hyperframes",
  "nombre": "HyperFrames",
  "tipo": "motor",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["composicion-video", "control-por-agente"],
  "resumen": "Composición y render de video a partir de HTML (Chromium sin cabeza + FFmpeg), pensada para escenas escritas por agentes.",
  "lenguajes": ["HTML", "JavaScript"],
  "exporta_video": "si",
  "repo": "heygen-com/hyperframes",
  "licencia": "Apache-2.0 (según el README; metadatos de GitHub por actualizar)",
  "agentes": "Diseñado para escenas generadas por agentes (según awesome-code-video).",
  "relacionados": ["remotion", "awesome-code-video"],
  "fuentes": ["awesome-code-video"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
Marco de HeyGen para componer video con HTML. Aparece en awesome-code-video junto con html-video (nexu-io/html-video), una capa HTML→MP4 local que usa HyperFrames como motor.

## Úsalo para
- Evaluar si un modelo local escribe mejor HTML plano que componentes de React.

## Limitaciones
- No revisado a fondo: mantenimiento y API por verificar con `saber actualizar --solo hyperframes`.
- Su README habla de empaquetarlo como plugin para Codex: pensado para agentes grandes.

## En este equipo
No instalado.
