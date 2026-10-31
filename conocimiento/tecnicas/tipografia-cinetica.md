# Tipografía cinética

```json
{
  "id": "tipografia-cinetica",
  "nombre": "Tipografía cinética",
  "tipo": "tecnica",
  "capacidades": ["tipografia-cinetica", "subtitulos-karaoke"],
  "herramientas": ["kit-scriptorium", "remotion", "opentype-js", "snapcn", "remotion-bits", "gsap", "animejs"],
  "resumen": "Animar texto por letras, palabras o líneas con entradas escalonadas, golpes al ritmo y revelados, sin perder legibilidad.",
  "recetas": ["canvas2d/golpe", "canvas2d/karaoke", "canvas2d/gancho"]
}
```

## Qué es
Texto que se mueve con intención: cada unidad (letra, palabra, línea) entra con un pequeño retraso respecto a la anterior (escalonado o *stagger*), con una curva que rebasa y se asienta. El significado manda: se anima lo que la voz está diciendo o lo que hay que recordar.

## Cómo se hace en Remotion
```tsx
const f = useCurrentFrame();
const {fps} = useVideoConfig();
const palabras = texto.split(' ');
return <h1 style={{display: 'flex', flexWrap: 'wrap', gap: '0.25em', textWrap: 'balance'}}>
  {palabras.map((p, i) => {
    const s = spring({frame: f - i * 5, fps, config: {damping: 13, mass: 0.6}});   // 5 cuadros entre palabras
    return <span key={i} style={{opacity: s, transform: `translateY(${(1 - s) * 30}px)`, display: 'inline-block'}}>{p}</span>;
  })}
</h1>;
```
- Por letra: igual, con `Array.from(palabra)` y 1–3 cuadros de retraso (a 60 fps). Solo en títulos cortos.
- Máquina de escribir: `texto.slice(0, Math.floor(interpolate(f, [0, dur], [0, texto.length])))`.
- Revelado con máscara: `clipPath: inset(0 ${100 - p * 100}% 0 0)` sobre la línea.
- Letras que se dibujan: contorno de cada glifo con opentype.js → `evolvePath` de `@remotion/paths` (ver [trazos-svg](trazos-svg.md)).
- En Scriptorium, el karaoke usa los cuadros reales de cada palabra (`palabras` en `Escena`): la palabra se ilumina en el cuadro en que la voz la dice.

## Números que funcionan
- Entrada de una palabra: 10–18 cuadros a 60 fps con `spring` (damping 12–16) o `backOut` (s≈1.7–1.9).
- Golpe de palabra al ritmo: escala 2.2→1 en 0.18 s con `backOut`, rotación pequeña distinta por palabra (`random(i)`), una palabra por beat.
- Permanencia mínima: ~0.3 s por palabra + 1 s antes de que se vaya.

## Errores comunes
- Animar cada letra de un párrafo: se vuelve ilegible y lento.
- Todo entra al mismo tiempo o todo con la misma curva (mecánico).
- Rotaciones o desenfoques grandes en texto que hay que leer.
- `Math.random()` en el render: cambia en cada cuadro. Usar `random('semilla' + i)` de Remotion.

## Ver también
Principios [tipografia-y-legibilidad](../principios/tipografia-y-legibilidad.md) y [timing-y-spacing](../principios/timing-y-spacing.md).
