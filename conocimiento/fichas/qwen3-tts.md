# Qwen3-TTS

```json
{
  "id": "qwen3-tts",
  "nombre": "Qwen3-TTS",
  "tipo": "modelo-ia",
  "areas": ["audio-voz"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["voz-tts"],
  "resumen": "Serie de TTS de Qwen (Alibaba) con clonación y streaming; el modelo 1.7B Base es la voz de la anfitriona de Scriptorium.",
  "lenguajes": ["Python"],
  "exporta_video": "no-aplica",
  "repo": "QwenLM/Qwen3-TTS",
  "licencia": "Apache-2.0",
  "requisitos": "GPU con CUDA; fp16 en la GP100.",
  "relacionados": ["voxcpm", "kokoro"],
  "fuentes": ["CLAUDE.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Modelo de voz expresivo; en Scriptorium se clona la referencia `anfitriona.wav` en cada segmento para que la voz no cambie.

## Úsalo para
- Segunda voz (podcast a dos voces, preguntas).

## Instalación
Ya instalado con `herramientas_wsl/voces_instalar.sh`.

## Limitaciones
- Un motor cargado a la vez por la RAM (16 GB).

## En este equipo
En uso (anfitriona).
