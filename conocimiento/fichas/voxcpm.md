# VoxCPM2

```json
{
  "id": "voxcpm",
  "nombre": "VoxCPM2",
  "tipo": "modelo-ia",
  "areas": ["audio-voz"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["voz-tts"],
  "resumen": "TTS multilingüe sin tokenizador con clonación de voz; es la voz del narrador de Scriptorium (masculina, elegida en cata a ciegas).",
  "lenguajes": ["Python"],
  "exporta_video": "no-aplica",
  "web": "https://voxcpm.com",
  "repo": "OpenBMB/VoxCPM",
  "paquetes": {"pypi": ["voxcpm"]},
  "licencia": "Apache-2.0",
  "requisitos": "GPU con CUDA; en la GP100 ~2.4 s de cómputo por segundo de audio (bf16 emulado).",
  "relacionados": ["qwen3-tts", "kokoro", "wav2vec2-alineacion"],
  "fuentes": ["CLAUDE.md", "HANDOFF.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Modelo de voz que genera por parches de 160 ms y clona una referencia. Scriptorium lo corre en su propio venv como proceso trabajador (`src/scriptorium/voz_trabajador.py`).

## Úsalo para
- Narración de videos y audiolibros con la voz fijada `narrador` (`voces/voces.json`).

## No lo uses para
- Clonar un texto idéntico al de la referencia: el modo continuación lo recorta.

## Instalación
Ya instalado: `herramientas_wsl/voces_instalar.sh` (venv en `~/.local/share/scriptorium/voces/voxcpm`).

## Limitaciones
- Termina en `tanh`: con voz fuerte aplana picos (el trabajador la quita y se nivela con ganancia lineal).
- A veces para un parche antes de terminar la última palabra (`_ParadaTardia` lo corrige).
- Más de 5 GB de RAM al cargar.

## En este equipo
En uso (narrador). Detalles y defectos conocidos en CLAUDE.md y HANDOFF.md.
