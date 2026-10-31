# Rough.js

```json
{
  "id": "roughjs",
  "nombre": "Rough.js",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["estilo-dibujado", "geometria", "diagramas"],
  "resumen": "Formas con aspecto dibujado a mano (estilo Excalidraw) en SVG o Canvas: líneas, rectángulos, elipses, polígonos y trazos SVG.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "http://roughjs.com",
  "repo": "rough-stuff/rough",
  "paquetes": {"npm": ["roughjs"]},
  "licencia": "MIT",
  "relacionados": ["p5-brush", "remotion-motion-graphics-skill"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`rough.svg(svg).rectangle(x, y, w, h, {roughness, seed})` devuelve trazos irregulares; con `seed` fija el dibujo es estable entre cuadros.

## Úsalo para
- Diagramas y anotaciones tipo pizarrón en videos explicativos.
- Resaltador o círculo a mano sobre una cita (con trazo animado).

## Instalación
```bash
npm i roughjs
```

## Ejemplo mínimo
```ts
import rough from 'roughjs';
const gen = rough.generator();
const caja = gen.rectangle(10, 10, 200, 80, {roughness: 1.5, seed: 7, stroke: '#F2EEE6'});
const trazos = gen.toPaths(caja);   // [{d, stroke, strokeWidth, fill}] → <path> en React
```

## Ventajas
- Ligera, sin dependencias, determinista con `seed`.
- Encaja con SVG de Remotion y con @remotion/paths para animar el trazo.

## Limitaciones
- Sin cambios desde 2024-07: estable, pero sin mantenimiento activo.
- Para «línea que hierve» cambiar la semilla 12 veces por segundo, no en cada cuadro.

## En este equipo
No instalado. Buena candidata para una escena de diagrama del kit.
