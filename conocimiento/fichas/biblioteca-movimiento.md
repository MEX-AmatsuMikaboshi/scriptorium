# Biblioteca de Movimiento (recetas Canvas 2D)

```json
{
  "id": "biblioteca-movimiento",
  "nombre": "Biblioteca de Movimiento (recetas Canvas 2D)",
  "tipo": "referencia",
  "areas": ["motion-graphics", "personajes"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["easing-timing", "transiciones", "tipografia-cinetica", "estilo-dibujado", "camara", "personajes-2d", "subtitulos-karaoke"],
  "resumen": "27 recetas de animación (Canvas 2D, funciones puras del tiempo) destiladas de PDoomVideo, ClaudeAnimationBase y videos virales; con motor base y prompt para modelos locales.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "licencia": "Página propia; las recetas citan su fuente y nivel de verificación (verificado, observado, inferido).",
  "agentes": "Escrita para modelos de 7–30B: prompt de sistema + motor de 180 líneas + recetas con código.",
  "relacionados": ["pdoom-video", "claude-animation-base", "p5-brush"],
  "fuentes": ["recetas/canvas2d/biblioteca-movimiento.html"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Página HTML con demos vivas (pausa, ¼×, cuadro a cuadro y carta de espaciado a 24 fps). Extraída a `recetas/canvas2d/`: `motor.js` (curvas, salto, take, resorte, arco, pulso, hervor de línea), `recetas.json` (las 27 con código) y `prompt-animador.md`.

## Úsalo para
- Fundamentos de timing con números concretos (anticipación 0.10–0.12 s, backOut s=1.9, resorte k=6 w=18).
- Transiciones artesanales: pincel, iris, papel rasgado, paneo látigo.
- Prompt listo para que un modelo local escriba animaciones Canvas 2D.

## No lo uses para
- Copiar las demos tal cual a un producto: son recreaciones didácticas de técnicas.

## Instalación
Nada que instalar: abre `recetas/canvas2d/biblioteca-movimiento.html` o consulta con `saber buscar` / `saber ver canvas2d/<id>`.

## Limitaciones
- Las recetas «inferidas» no están verificadas contra el video original (marcadas).
- Canvas 2D a 640×360 lógicos: para el kit hay que traducir la idea a Remotion.

## En este equipo
En la biblioteca. Para regenerar los archivos tras cambiar el HTML: `node herramientas/extraer_recetas.mjs`.
