# p5.brush

```json
{
  "id": "p5-brush",
  "nombre": "p5.brush",
  "tipo": "libreria",
  "areas": ["motion-graphics", "personajes"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["estilo-dibujado"],
  "resumen": "Pinceles naturales, rellenos tipo acuarela y achurado para p5.js: la textura de los videos de PDoomVideo y ClaudeAnimationBase.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://p5-brush.cargo.site/",
  "repo": "acamposuribe/p5.brush",
  "paquetes": {"npm": ["p5.brush"]},
  "licencia": "MIT",
  "relacionados": ["p5js", "pdoom-video", "claude-animation-base", "roughjs"],
  "fuentes": ["recetas/canvas2d/biblioteca-movimiento.html"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Extensión de p5.js con pinceles personalizados (lápiz, carbón, marcador…), rellenos con bordes naturales y achurados.

## Úsalo para
- Estilo acuarela o dibujado a mano de calidad.

## Instalación
```bash
npm i p5.brush p5
```

## Limitaciones
- Los rellenos de acuarela son pesados: segundos por cuadro sin GPU.
- Necesita el modo WebGL de p5.

## En este equipo
No instalado. En WSL sin GPU el render sería lento; para el kit, rough.js o SVG con filtros es más ligero.
