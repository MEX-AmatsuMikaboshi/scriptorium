# Kokoro-82M

```json
{
  "id": "kokoro",
  "nombre": "Kokoro-82M",
  "tipo": "modelo-ia",
  "areas": ["audio-voz"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["voz-tts"],
  "resumen": "TTS ligero de 82M parámetros (~29× tiempo real en la GP100); voz de respaldo de Scriptorium (em_alex, ef_dora).",
  "lenguajes": ["Python"],
  "exporta_video": "no-aplica",
  "web": "https://hf.co/hexgrad/Kokoro-82M",
  "repo": "hexgrad/kokoro",
  "paquetes": {"pypi": ["kokoro"]},
  "licencia": "Apache-2.0",
  "relacionados": ["voxcpm", "qwen3-tts"],
  "fuentes": ["CLAUDE.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Modelo pequeño y rápido con voces predefinidas, acento es-419 disponible.

## Úsalo para
- Borradores rápidos de narración para probar el timing de un video.

## No lo uses para
- Versión final: al usuario le suena robótica.

## Instalación
Ya instalado en el venv de Scriptorium.

## Limitaciones
- Sin clonación; voces limitadas.

## En este equipo
En uso como respaldo.
