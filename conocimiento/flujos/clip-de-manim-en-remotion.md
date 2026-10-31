# Clip de Manim dentro de un video de Remotion

```json
{
  "id": "clip-de-manim-en-remotion",
  "nombre": "Clip de Manim dentro de un video de Remotion",
  "tipo": "flujo",
  "prioridad": "complemento",
  "capacidades": ["matematicas", "composicion-video"],
  "herramientas": ["manim", "remotion", "ffmpeg"],
  "resumen": "Animar una demostración o ecuación en Manim, renderizarla con fondo transparente y montarla en una escena del kit."
}
```

## Pasos
1. **Instalar Manim** en un venv propio en WSL (ver la ficha `manim`; no en el venv de Scriptorium).
2. **Escena** con los colores y la fuente del kit (`config.background_color`, `Text(..., font='EB Garamond')`).
3. **Duración**: igualar la duración de cada `self.play` a lo que dura la frase de la voz (la alineación da los tiempos; pasarlos a Manim como `run_time`).
4. **Render** transparente: `manim -qh --transparent --format=mov escena.py Clase` (o PNG con `--format=png`).
5. **Montaje**: copiar a `video/public/` y usar `<OffthreadVideo transparent>` en la escena; comprobar que empieza en el cuadro correcto.

## Cuándo no vale la pena
Fórmulas que solo aparecen (sin transformarse): KaTeX dentro de Remotion es más simple.
