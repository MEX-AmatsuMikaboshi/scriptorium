# Animación procedural y ruido

```json
{
  "id": "procedural-y-ruido",
  "nombre": "Animación procedural y ruido",
  "tipo": "tecnica",
  "capacidades": ["arte-generativo", "particulas"],
  "herramientas": ["remotion", "p5js", "canvas-sketch", "lygia", "threejs"],
  "resumen": "Movimiento orgánico y patrones generativos a partir de ruido y azar con semilla, siempre como función del tiempo.",
  "recetas": ["canvas2d/boil", "canvas2d/pulso"]
}
```

## Qué es
En vez de keyframes, una fórmula: posición = f(semilla, tiempo). El ruido coherente (Perlin/Simplex) da movimiento suave que no se repite; el azar con semilla da variedad estable entre renders.

## Cómo se hace en Remotion
```tsx
import {noise2D} from '@remotion/noise';
import {random} from 'remotion';
const t = f / fps;
const x = base.x + noise2D('deriva-' + i, t * 0.25, 0) * 12;   // 0.25 Hz, ±12 px
const fase = random('fase-' + i) * Math.PI * 2;                 // estable entre cuadros y renders
```
- Campo de flujo: el ángulo en (x, y) es `noise3D(semilla, x * k, y * k, t * v) * 2π`; las partículas siguen ese ángulo (calcular su trayectoria como suma cerrada o pre-simular una vez y guardar).
- «Boil» de línea dibujada: cambiar la semilla en pasos de 1/12 s: `Math.floor(t * 12)`.
- Pulso común: `exp(-frac(t / BEAT) * 6)` vale 1 en cada beat y decae.

## Reglas
- Nunca `Math.random()` ni estado entre cuadros: Remotion renderiza en paralelo y en desorden.
- Frecuencias bajas (0.1–0.5 Hz) para cosas grandes; altas solo para detalles pequeños.
- Cada elemento con su propia semilla (evita que todo se mueva igual: «gemelos»).
