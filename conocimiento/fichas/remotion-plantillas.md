# Plantillas oficiales de Remotion

```json
{
  "id": "remotion-plantillas",
  "nombre": "Plantillas oficiales de Remotion",
  "tipo": "plantilla",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["subtitulos-karaoke", "visualizacion-audio", "escena-3d", "tipografia-cinetica"],
  "resumen": "Plantillas de Remotion: audiograma (onda + subtítulos), subtítulos estilo TikTok con palabra activa, Code Hike (código animado), Three (R3F) y overlay.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "web": "https://www.remotion.dev/templates",
  "docs": ["https://github.com/remotion-dev/remotion/tree/main/packages/template-audiogram", "https://github.com/remotion-dev/remotion/tree/main/packages/template-tiktok", "https://github.com/remotion-dev/remotion/tree/main/packages/template-code-hike"],
  "licencia": "Las del monorepo de Remotion (Remotion License).",
  "agentes": "Proyectos completos que un agente puede leer como ejemplo.",
  "relacionados": ["remotion", "remotion-template-three"],
  "fuentes": ["awesome-code-video"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
Proyectos de ejemplo dentro del monorepo de Remotion; se crean con `npx create-video@latest` eligiendo la plantilla.

## Úsalo para
- Ver cómo resuelve Remotion los subtítulos con palabra activa y la onda de audio.
- Plantilla de partida para un formato nuevo (podcast con onda, clip vertical).

## Instalación
```bash
npx create-video@latest   # elegir audiogram, tiktok, code-hike, three…
```

## Limitaciones
- Algunas plantillas tienen términos propios (awesome-code-video los marca «por confirmar»).

## En este equipo
No instaladas. El kit ya resuelve karaoke con alineación forzada; útiles como referencia para el formato vertical 9:16 pendiente.
