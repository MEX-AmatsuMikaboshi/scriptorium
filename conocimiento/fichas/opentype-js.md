# opentype.js

```json
{
  "id": "opentype-js",
  "nombre": "opentype.js",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["tipografia-cinetica", "trazo-svg", "morphing"],
  "resumen": "Lee fuentes OpenType/TrueType en JavaScript y da el contorno de cada letra como trazo: base para letras que se dibujan o se deforman.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://opentype.js.org",
  "repo": "opentypejs/opentype.js",
  "paquetes": {"npm": ["opentype.js"]},
  "licencia": "MIT",
  "relacionados": ["gsap", "flubber"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`font.getPath(texto, x, y, tamaño).toPathData()` devuelve el SVG de la palabra; `font.charToGlyph()` da cada glifo con sus métricas.

## Úsalo para
- Escritura de letras trazo a trazo, letras que se transforman en otras, texto sobre trayectorias.

## Instalación
```bash
npm i opentype.js
```

## Limitaciones
- Las fuentes deben permitir incrustación (EB Garamond e Inter del kit son OFL).

## En este equipo
No instalado.
