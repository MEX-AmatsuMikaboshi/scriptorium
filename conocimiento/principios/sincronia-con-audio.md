# Sincronía con audio

```json
{
  "id": "sincronia-con-audio",
  "nombre": "Sincronía con audio",
  "tipo": "principio",
  "resumen": "La imagen confirma lo que se oye en el instante en que se oye; un desfase de más de ~100 ms ya se nota.",
  "capacidades": ["sincronia-audio", "subtitulos-karaoke"]
}
```

## En la práctica
- **Tiempos reales, no estimados**: alineación forzada para saber en qué cuadro se dice cada palabra (Scriptorium lo hace con wav2vec2).
- **Aparecer al nombrarse**: cada elemento entra cuando la voz lo menciona (2–4 cuadros antes se percibe sincrónico).
- **Golpes en el beat** si hay música; cortes en las pausas de la voz.
- **Silencio también es sonido**: dejar respirar la voz antes de un concepto importante.
- **Niveles**: voz a −20 dBFS RMS y pico −1 dBFS; música 15–20 dB por debajo; efectos breves y discretos.

Técnica completa: [sincronia-con-voz](../tecnicas/sincronia-con-voz.md).
