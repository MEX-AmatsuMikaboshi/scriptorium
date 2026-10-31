# p5.js

```json
{
  "id": "p5js",
  "nombre": "p5.js",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["arte-generativo", "particulas", "geometria", "estilo-dibujado"],
  "resumen": "La librería de creative coding de Processing en JavaScript: dibujo inmediato en Canvas o WebGL con setup()/draw(); ideal para arte generativo.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://p5js.org",
  "repo": "processing/p5.js",
  "paquetes": {"npm": ["p5"]},
  "licencia": "LGPL-2.1",
  "agentes": "Muy presente en datos de entrenamiento: los modelos chicos la escriben bien.",
  "relacionados": ["p5-brush", "canvas-sketch", "claude-animation-base"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Modo inmediato: en cada `draw()` se borra y se vuelve a dibujar. Formas, color, ruido de Perlin (`noise()`), tipografía, imágenes, WebGL básico.

## Úsalo para
- Arte generativo, campos de flujo, partículas simples, ilustración con trazos.
- Prototipos rápidos de una idea visual antes de pasarla al kit.

## No lo uses para
- Composición de video con audio y escenas (usar Remotion y meter el Canvas).

## Instalación
```bash
npm i p5   # o un <script> desde CDN
```

## Ventajas
- Enorme comunidad y ejemplos.
- Ruido, color y formas listos.

## Limitaciones
- `draw()` depende del reloj y `random()` del azar: para video determinista usa `randomSeed`/`noiseSeed` y calcula todo desde el número de cuadro.
- LGPL: al distribuir una versión modificada de p5 hay obligaciones.

## En este equipo
No instalado. Para exportar video: render por cuadros con Chrome sin cabeza (como ClaudeAnimationBase) o dentro de Remotion.
