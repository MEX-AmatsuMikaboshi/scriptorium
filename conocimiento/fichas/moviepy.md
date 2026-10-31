# MoviePy

```json
{
  "id": "moviepy",
  "nombre": "MoviePy",
  "tipo": "libreria",
  "areas": ["video-explicativo"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["composicion-video"],
  "resumen": "Edición de video en Python: cortar, concatenar, superponer texto e imágenes y componer clips sobre FFmpeg.",
  "lenguajes": ["Python"],
  "exporta_video": "si",
  "web": "https://zulko.github.io/moviepy/",
  "repo": "Zulko/moviepy",
  "paquetes": {"pypi": ["moviepy"]},
  "licencia": "MIT",
  "relacionados": ["ffmpeg"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`VideoFileClip`, `ImageClip`, `TextClip`, `CompositeVideoClip`, `concatenate_videoclips`; cada clip puede tener una función de tiempo.

## Úsalo para
- Montajes simples desde Python (unir clips de Manim con audio) sin pasar por Node.

## No lo uses para
- Motion graphics elaborados (Remotion es mucho mejor).

## Instalación
```bash
uv pip install moviepy
```

## Limitaciones
- Versión 2 rompió la API de la 1: los modelos suelen escribir la vieja.

## En este equipo
No instalado.
