# Transiciones entre escenas

```json
{
  "id": "transiciones",
  "nombre": "Transiciones entre escenas",
  "tipo": "tecnica",
  "capacidades": ["transiciones", "composicion-video"],
  "herramientas": ["remotion", "kit-scriptorium", "biblioteca-movimiento"],
  "resumen": "Unir escenas sin cortes secos: deslizamientos, barridos, iris y transiciones artesanales que cubren el corte.",
  "recetas": ["canvas2d/pincel", "canvas2d/iris", "canvas2d/rasgado", "canvas2d/latigo"]
}
```

## Cómo se hace en Remotion
```tsx
import {TransitionSeries, springTiming, linearTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={180}><EscenaA /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={slide({direction: 'from-right'})} timing={springTiming({config: {damping: 200}, durationInFrames: 24})} />
  <TransitionSeries.Sequence durationInFrames={200}><EscenaB /></TransitionSeries.Sequence>
</TransitionSeries>
```
- Presentaciones incluidas: `fade`, `slide`, `wipe`, `flip`, `clockWipe`, `iris`, `none`; se pueden escribir propias.
- El kit usa deslizar y barrido, y **no** funde escenas con texto: dos textos encimados se leen sucios.
- Artesanales (Canvas 2D, en la Biblioteca de Movimiento): barrido de pincel, iris con forma, papel rasgado, paneo látigo.

## Números
- Cambio dentro de un mismo tema: 12–24 cuadros a 60 fps (0.2–0.4 s).
- Cambio de capítulo o de idea grande: 30–45 cuadros, con una transición distinta y reconocible.
- En una transición que tapa la pantalla, el corte ocurre cuando está cubierta al 100 %.

## Reglas
- La dirección de la transición sigue la lógica (adelante = derecha a izquierda).
- Pocas transiciones distintas en un video (2–3) usadas con criterio: forman parte del sistema visual.
- Ver [transiciones-entre-escenas](../principios/transiciones-entre-escenas.md).
