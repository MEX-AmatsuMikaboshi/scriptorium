# Flubber

```json
{
  "id": "flubber",
  "nombre": "Flubber",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["morphing", "geometria"],
  "resumen": "Interpolación suave entre dos formas SVG cualesquiera (incluso con distinto número de puntos): el morphing «que se ve bien».",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "repo": "veltman/flubber",
  "paquetes": {"npm": ["flubber"]},
  "licencia": "MIT",
  "relacionados": ["paperjs", "gsap"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`interpolate(pathA, pathB)` devuelve una función t→path; también `separate`/`combine` para pasar de una forma a varias.

## Úsalo para
- Que un círculo se convierta en una estrella, un ícono en otro, un mapa en otro.

## Instalación
```bash
npm i flubber
```

## Ejemplo mínimo
```ts
import {interpolate} from 'flubber';
const f = interpolate(circuloD, estrellaD, {maxSegmentLength: 4});
// en Remotion: <path d={f(interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'}))} />
```

## Limitaciones
- Sin cambios desde 2022-11: pequeña y estable, pero abandonada.

## En este equipo
No instalado.
