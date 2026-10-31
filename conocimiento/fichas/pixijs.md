# PixiJS

```json
{
  "id": "pixijs",
  "nombre": "PixiJS",
  "tipo": "libreria",
  "areas": ["motion-graphics", "2d"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["particulas", "shaders", "geometria", "personajes-2d"],
  "resumen": "Motor 2D muy rápido sobre WebGL/WebGPU: miles de sprites, partículas, filtros y shaders 2D.",
  "lenguajes": ["JavaScript", "TypeScript"],
  "exporta_video": "indirecto",
  "web": "https://pixijs.com",
  "repo": "pixijs/pixijs",
  "paquetes": {"npm": ["pixi.js"]},
  "llms_txt": "https://pixijs.com/llms.txt",
  "licencia": "MIT",
  "agentes": "Publica llms.txt (se baja con `saber actualizar`).",
  "relacionados": ["threejs", "tsparticles"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Grafo de escena 2D acelerado por GPU: `Sprite`, `Graphics`, `Text`, `Container`, filtros (desenfoque, desplazamiento) y shaders propios. La versión 8 soporta WebGPU.

## Úsalo para
- Escenas 2D con muchos elementos (multitudes, partículas) que el DOM/SVG no aguanta.

## No lo uses para
- Escenas sencillas: React + SVG en Remotion basta.

## Instalación
```bash
npm i pixi.js
```

## Limitaciones
- Necesita un lienzo propio; integrarlo con Remotion requiere controlar su ticker manualmente.
- Sin GPU en WSL usa render por software.

## En este equipo
No instalado.
