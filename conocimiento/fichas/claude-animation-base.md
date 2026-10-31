# ClaudeAnimationBase

```json
{
  "id": "claude-animation-base",
  "nombre": "ClaudeAnimationBase",
  "tipo": "plantilla",
  "areas": ["motion-graphics", "personajes"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["estilo-dibujado", "personajes-2d", "easing-timing", "composicion-video"],
  "resumen": "Kit para animar personajes pintados a mano con un agente: p5.js + p5.brush, el personaje Clawd, 31 emociones actuadas y una guía de animación para el modelo. MIT.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "si",
  "repo": "JohnHeibel/ClaudeAnimationBase",
  "licencia": "MIT",
  "agentes": "«Read ANIMATION_GUIDE.md, then make a 15-second video…»: el modelo hace storyboard, construye toma por toma, revisa hojas de contacto y escribe out/video.mp4.",
  "requisitos": "Node.js, Google Chrome (o Chromium de Playwright) y ffmpeg. Sin GPU, los rellenos de acuarela son lentos (segundos por cuadro).",
  "relacionados": ["pdoom-video", "p5-brush", "p5js", "biblioteca-movimiento"],
  "fuentes": ["recetas/canvas2d/biblioteca-movimiento.html"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Versión general y con licencia MIT de lo aprendido en PDoomVideo: reglas de timing («lecturas»), resortes, arcos, animación en doses, línea que hierve con semilla por elemento y una lista de fallas típicas de la animación generada.

## Úsalo para
- Caricaturas cortas con un personaje (etapa futura del proyecto).
- Su ANIMATION_GUIDE.md como modelo de guía para agentes locales.

## Instalación
```bash
git clone https://github.com/JohnHeibel/ClaudeAnimationBase
node render.mjs --clip --out=out/video.mp4   # en Linux añade --soft-gl si no hay GPU
```

## Ventajas
- MIT: se puede adaptar.
- Flujo de autocrítica con hojas de contacto, útil para modelos locales.

## Limitaciones
- Pensado para Claude Opus; un modelo de 12–14B necesitará tomas más cortas y más guía.
- Render en Chrome; en WSL sin GPU usar --soft-gl (lento).

## En este equipo
No clonado. Candidato para el primer experimento de caricatura.
