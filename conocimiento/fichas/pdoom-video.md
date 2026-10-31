# PDoomVideo

```json
{
  "id": "pdoom-video",
  "nombre": "PDoomVideo",
  "tipo": "referencia",
  "areas": ["motion-graphics", "personajes"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["estilo-dibujado", "easing-timing", "subtitulos-karaoke", "transiciones", "personajes-2d"],
  "resumen": "Código del video musical en acuarela hecho por Claude Opus 5.5 con p5.js + p5.brush (1920×1080, 156.6 s, 88 BPM); incluye la ANIMATION_GUIDE que coordinó a los subagentes.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "si",
  "repo": "JohnHeibel/PDoomVideo",
  "licencia": "Sin licencia declarada (consultado 2026-10-31): todos los derechos reservados. Leer y aprender sí; no copiar código.",
  "agentes": "ANIMATION_GUIDE.md y STORYBOARD.md escritos por el modelo para sus subagentes.",
  "relacionados": ["claude-animation-base", "p5-brush", "biblioteca-movimiento"],
  "fuentes": ["recetas/canvas2d/biblioteca-movimiento.html"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`studio.html` pinta cada cuadro con p5.js y p5.brush; `render.mjs` renderiza en Chrome sin cabeza (reanudable, varios trabajadores) y codifica con ffmpeg junto con la canción.

## Úsalo para
- Estudiar cómo un agente organiza un video largo: guía de estilo, storyboard, render por cuadros.

## No lo uses para
- Reutilizar su código en un proyecto: no tiene licencia.

## Instalación
```bash
node render.mjs --frames=0:156.6 --workers=4
node render.mjs --encode --out=out/pdoom.mp4
```

## Limitaciones
- Sin licencia.
- Render lento sin GPU (acuarela de p5.brush).

## En este equipo
No clonado. Sus técnicas ya están en la Biblioteca de Movimiento.
