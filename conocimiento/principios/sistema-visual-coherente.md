# Sistema visual coherente

```json
{
  "id": "sistema-visual-coherente",
  "nombre": "Sistema visual coherente",
  "tipo": "principio",
  "resumen": "Reglas escritas de tipografía, color, movimiento y transiciones que todo el video (y toda la serie) respeta: así se ve hecho por una sola mano."
}
```

## En la práctica
- **Escribe el estilo** antes de programarlo (como los `STYLE.md` de Lemo-Opuscar): paleta, fuentes, tamaños, curvas preferidas, duración estándar, transiciones permitidas, qué está prohibido.
- **Tokens en código**: colores, fuentes, duraciones y curvas en un solo archivo (`video/src/tema.ts`), nunca números sueltos en cada escena.
- **Componentes reutilizables**: una entrada de texto, una transición, un pictograma — siempre los mismos.
- **Catálogos cerrados** para el LLM (tipos de escena, íconos): el modelo elige, no inventa.
- **Serie**: misma portada, mismo cierre, misma insignia de nivel en todos los videos.

## Señal de un sistema sano
Si cambias el color de acento en un archivo, cambia en todo el video.
