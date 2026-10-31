# Video explicativo corto (30 s)

```json
{
  "id": "video-explicativo-30s",
  "nombre": "Video explicativo corto (30 s)",
  "tipo": "flujo",
  "prioridad": "ahora",
  "capacidades": ["video-explicativo", "composicion-video", "sincronia-audio"],
  "herramientas": ["kit-scriptorium", "remotion", "voxcpm", "wav2vec2-alineacion", "ffmpeg"],
  "resumen": "De un texto breve a un video de 30 s con voz, karaoke alineado y escenas del kit, con o sin el pipeline de Scriptorium."
}
```

## Medidas
- 30 s de narración en español ≈ 70–80 palabras (≈2.5 palabras/s con pausas).
- 4–6 escenas: portada (3–4 s), 3–4 escenas de contenido (5–7 s), cierre (3 s).
- 1080p, 60 fps → 1800 cuadros.

## Con Scriptorium (recomendado)
1. Escribe el texto como Markdown con cabecera (`titulo`, `autor`) y ponlo en `D:\Scriptorium\00_entrada`, o `scriptorium ingerir archivo.md`.
2. `scriptorium generar <slug> --formatos video`. El director LLM elige escenas del kit (`TIPOS` en `src/scriptorium/video.py`), la voz se genera con las voces fijadas, la alineación da los cuadros de cada palabra y Remotion renderiza.
3. Revisa cuadros con `herramientas_wsl/cuadros.sh <slug>` y la sincronía con `herramientas_wsl/medir_sincronia.sh`.

## Sin el pipeline (otro proyecto)
1. **Guion por escenas**: para cada una, la frase de voz, lo que se ve y la «lectura» que el espectador debe sacar.
2. **Voz** por escena (el TTS que haya) → WAV. Medir duración real.
3. **Alineación** (wav2vec2 o similar) → cuadros de cada palabra.
4. **Composición** en Remotion: `<Series>` o `<TransitionSeries>` con duración = voz + 0.5 s de respiro.
5. **Revisión** con stills (`npx remotion still … --frame=N`) al inicio, mitad y fin de cada escena; luego render.
6. Pasar la [lista-de-control](../principios/lista-de-control.md).

## Contexto para un modelo local
`saber contexto "video explicativo de 30 segundos sobre <tema>"` junta la técnica, las herramientas y la lista de control en ~3500 tokens.
