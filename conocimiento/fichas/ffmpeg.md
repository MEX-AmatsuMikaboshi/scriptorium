# FFmpeg

```json
{
  "id": "ffmpeg",
  "nombre": "FFmpeg",
  "tipo": "herramienta",
  "areas": ["video-explicativo", "audio-voz"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["composicion-video", "sincronia-audio", "visualizacion-audio"],
  "resumen": "La navaja suiza de audio y video: convertir, recortar, unir, mezclar audio, cuadros a video, normalizar volumen, subtítulos incrustados.",
  "lenguajes": ["CLI"],
  "exporta_video": "si",
  "web": "https://ffmpeg.org",
  "repo": "FFmpeg/FFmpeg",
  "licencia": "LGPL-2.1+ (algunas compilaciones GPL)",
  "relacionados": ["remotion", "moviepy"],
  "fuentes": ["CLAUDE.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Herramienta de línea de comandos. Recetas útiles: `ffmpeg -framerate 60 -i cuadros/%05d.png -c:v libx264 -pix_fmt yuv420p salida.mp4` (cuadros → video); `-af loudnorm` (nivel); `-ss 10 -frames:v 1` (un cuadro).

## Úsalo para
- Toda conversión o unión de medios fuera de Remotion.
- Convertir secuencias PNG con alfa de Blender/Manim a clips para el kit (ProRes 4444 o WebM VP9 con alfa).

## Instalación
En WSL: `sudo apt install ffmpeg` (ya instalado). El ffmpeg de Windows está bloqueado por el Control inteligente de aplicaciones.

## Limitaciones
- Sintaxis densa: guardar recetas que funcionen.

## En este equipo
En uso en WSL.
