# wav2vec2 español (alineación forzada)

```json
{
  "id": "wav2vec2-alineacion",
  "nombre": "wav2vec2 español (alineación forzada)",
  "tipo": "modelo-ia",
  "areas": ["audio-voz", "video-explicativo"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["sincronia-audio", "subtitulos-karaoke"],
  "resumen": "Modelo CTC jonatasgrosman/wav2vec2-large-xlsr-53-spanish: da el tiempo real de cada palabra dicha (karaoke, subtítulos) y una transcripción de control.",
  "lenguajes": ["Python"],
  "exporta_video": "no-aplica",
  "web": "https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-spanish",
  "licencia": "Apache-2.0 según su tarjeta en Hugging Face (verificar).",
  "relacionados": ["voxcpm", "kit-scriptorium", "rhubarb-lip-sync"],
  "fuentes": ["CLAUDE.md"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
`src/scriptorium/alineacion.py` alinea el texto con el audio por CTC (confianza ~0.99 por palabra) y transcribe para detectar palabras que la voz se comió.

## Úsalo para
- Toda sincronía voz-pantalla del kit.
- Base posible para sincronía labial: los tiempos por carácter dan las vocales.

## Instalación
Ya instalado (se descarga de Hugging Face la primera vez).

## Limitaciones
- Oye «por qué» como «porque»: el control ya ignora cambios que solo mueven espacios.

## En este equipo
En uso. Medir desfase con `herramientas_wsl/medir_sincronia.sh`.
