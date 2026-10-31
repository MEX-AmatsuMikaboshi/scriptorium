# Sincronía con la voz, subtítulos y música

```json
{
  "id": "sincronia-con-voz",
  "nombre": "Sincronía con la voz, subtítulos y música",
  "tipo": "tecnica",
  "capacidades": ["sincronia-audio", "subtitulos-karaoke", "voz-tts", "visualizacion-audio"],
  "herramientas": ["kit-scriptorium", "wav2vec2-alineacion", "voxcpm", "qwen3-tts", "remotion", "ffmpeg"],
  "resumen": "Que lo que se ve ocurra cuando se dice: alineación forzada palabra por palabra, karaoke, aparición al mencionarse, subtítulos por frase y pulso musical.",
  "recetas": ["canvas2d/karaoke", "canvas2d/pulso"]
}
```

## La regla de Scriptorium
Lo que se ilumina palabra por palabra es **exactamente** lo que dice la voz, en el cuadro en que lo dice. Una cita en pantalla se lee literal; el texto que la voz no dice tal cual aparece completo, sin iluminarse.

## Cómo se logra
1. Voz por escena (VoxCPM2 / Qwen3-TTS, voces fijadas) → WAV.
2. Alineación forzada (wav2vec2 CTC español) → `[palabra, cuadro_inicio, cuadro_fin]` (`palabras` en `Escena`).
3. Karaoke: cada palabra cambia de color en su cuadro; subtítulos agrupados en frases (`subtitulos`).
4. Aparición: listas, premisas y contrastes entran cuando la voz los empieza a decir (`aparece`).
5. Medir: `herramientas_wsl/medir_sincronia.sh` (desfase voz-pantalla).

## Música y pulso
- Si hay música, rejilla de beats (`BEAT = 60 / BPM`): golpes de texto, cortes y rebotes caen en el beat.
- Música bajo la voz: 15–20 dB por debajo; nivel final de la voz −20 dBFS RMS, pico −1 dBFS (lo hace `audio.nivelar`).

## Visualizar audio
`@remotion/media-utils`: `useAudioData` + `visualizeAudio` dan amplitudes por frecuencia en cada cuadro (barras, onda).
