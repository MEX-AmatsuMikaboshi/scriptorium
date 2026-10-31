# Figuras geométricas y morphing

```json
{
  "id": "geometria-y-morphing",
  "nombre": "Figuras geométricas y morphing",
  "tipo": "tecnica",
  "capacidades": ["morphing", "geometria"],
  "herramientas": ["remotion", "flubber", "paperjs", "manim", "motion-canvas", "gsap"],
  "resumen": "Formas que aparecen, se combinan y se transforman unas en otras de manera suave y legible.",
  "recetas": ["canvas2d/curvas"]
}
```

## Qué es
Figuras simples (círculo, polígono, estrella, flecha) como lenguaje visual: aparecen, se dividen, se agrupan y se convierten en otras. El morphing interpola el contorno de A al de B.

## Cómo se hace en Remotion
- Figuras: `@remotion/shapes` (`makeCircle`, `makeRect`, `makeTriangle`, `makeStar`, `makePolygon`…) devuelve `{path, width, height}`.
- Morphing entre trazos con los mismos comandos: `interpolatePath(p, a, b)` de `@remotion/paths`.
- Morphing entre formas cualesquiera: `flubber.interpolate(a, b, {maxSegmentLength: 4})` → función `t → path`.
```tsx
const t = interpolate(f, [0, 36], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.quad)});
const d = morph(t);   // morph = flubber.interpolate(circulo, estrella) calculado una vez fuera del componente (useMemo)
```
- Matemáticas precisas (polígonos inscritos, transformaciones lineales): Manim (`Transform`, `ReplacementTransform`).

## Reglas
- Conserva el centro y el tamaño visual: si la forma B es más grande, escala después.
- Rota poco durante el morph (máx. 30–45°); el ojo debe seguir «la misma cosa».
- Un morph es una idea («esto se convierte en aquello»): dale pausa antes y después.

## Errores comunes
- Interpolar trazos con distinto número de puntos sin flubber: picos y cruces.
- Calcular el interpolador dentro de cada cuadro (lento): calcularlo una vez.
