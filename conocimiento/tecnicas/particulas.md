# Partículas

```json
{
  "id": "particulas",
  "nombre": "Partículas",
  "tipo": "tecnica",
  "capacidades": ["particulas"],
  "herramientas": ["remotion", "threejs", "pixijs", "p5js", "tsparticles"],
  "resumen": "Confeti, polvo, chispas o nieve deterministas: cada partícula es una fórmula de su índice y del tiempo.",
  "recetas": ["canvas2d/sfx"]
}
```

## Qué es
Muchos elementos pequeños con vida corta. Para video no se simula paso a paso: cada partícula `i` nace en `t0(i)`, tiene velocidad y color de `random(semilla + i)`, y su posición se calcula directamente con la edad `a = t - t0`.

## Cómo se hace en Remotion
```tsx
const N = 120;
return <AbsoluteFill>{Array.from({length: N}, (_, i) => {
  const t0 = i * 0.03, a = f / fps - t0, vida = 1.6;
  if (a < 0 || a > vida) return null;
  const ang = random('a' + i) * Math.PI * 2, v = 150 + random('v' + i) * 250;
  const x = 960 + Math.cos(ang) * v * a, y = 540 + Math.sin(ang) * v * a + 0.5 * 600 * a * a;  // gravedad 600 px/s²
  const o = 1 - Math.max(0, (a - vida + 0.4) / 0.4);                                           // se desvanece al final
  return <div key={i} style={{position: 'absolute', left: x, top: y, width: 8, height: 8, borderRadius: 4, opacity: o, background: COLORES[i % COLORES.length]}} />;
})}</AbsoluteFill>;
```
- Hasta ~300 partículas: DOM o SVG. Miles: un `<canvas>` dibujado en cada cuadro. Decenas de miles: Three.js `Points` con la fórmula en un shader.
- tsParticles y similares simulan con su reloj: no sirven para render determinista sin trabajo extra.

## Reglas
- Las partículas acompañan, no protagonizan: menos opacidad y tamaño que el texto.
- Variar tamaño, velocidad y vida (no todas iguales).
- Que nazcan de algo (un golpe, un objeto) y no de la nada.
