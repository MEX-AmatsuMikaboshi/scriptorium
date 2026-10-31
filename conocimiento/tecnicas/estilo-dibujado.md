# Estilo dibujado a mano, papel y pincel

```json
{
  "id": "estilo-dibujado",
  "nombre": "Estilo dibujado a mano, papel y pincel",
  "tipo": "tecnica",
  "capacidades": ["estilo-dibujado", "trazo-svg"],
  "herramientas": ["roughjs", "p5-brush", "biblioteca-movimiento", "claude-animation-base"],
  "resumen": "Aspecto artesanal: trazos irregulares con semilla, línea que hierve a 12 fps, animación en doses y textura de papel.",
  "recetas": ["canvas2d/boil", "canvas2d/doses", "canvas2d/anotacion", "canvas2d/pincel"]
}
```

## Recursos
- **Rough.js**: formas «a mano» deterministas con `seed`. Para que hiervan, cambia la semilla cada 1/12 s: `seed = base + Math.floor(t * 12)`, y una semilla distinta por elemento.
- **En doses** (*on twos*): congelar la pose 2 cuadros (12 dibujos por segundo a 24 fps; a 60 fps, `Math.floor(t * 12) / 12`) da sensación hecha a mano.
- **Papel**: textura estática (SVG `feTurbulence` o una imagen) que no hierve; tinta casi negra (#26222E) sobre crema (#FFF8EA), nunca negro ni blanco puros.
- **Acuarela y pincel**: p5.brush (pesado sin GPU).

## Reglas
- Lo que no se mueve no debe temblar en cada cuadro (molesta); el hervor es sutil y uniforme.
- Mezclar estilo dibujado con tipografía limpia funciona; mezclar tres estilos no.
- Lista de fallas típicas de la animación generada: ver `ANIMATION_GUIDE.md` de ClaudeAnimationBase y la [lista-de-control](../principios/lista-de-control.md).
