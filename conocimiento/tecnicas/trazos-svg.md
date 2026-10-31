# Trazos y líneas que se dibujan

```json
{
  "id": "trazos-svg",
  "nombre": "Trazos y líneas que se dibujan",
  "tipo": "tecnica",
  "capacidades": ["trazo-svg", "iconos", "estilo-dibujado"],
  "herramientas": ["remotion", "kit-scriptorium", "lucide", "roughjs", "opentype-js", "gsap"],
  "resumen": "Hacer que un trazo SVG (ícono, flecha, subrayado, letra, ruta) aparezca como si se dibujara, con stroke-dasharray/offset.",
  "recetas": ["canvas2d/anotacion"]
}
```

## Qué es
Un trazo SVG se «dibuja» ocultando su longitud con `stroke-dasharray = L` y bajando `stroke-dashoffset` de `L` a 0. Sirve para íconos, flechas, subrayados, círculos a mano, rutas en mapas y letras.

## Cómo se hace en Remotion
```tsx
import {evolvePath} from '@remotion/paths';
const p = interpolate(f, [inicio, inicio + 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
const {strokeDasharray, strokeDashoffset} = evolvePath(p, d);
return <path d={d} fill="none" stroke={COLOR} strokeWidth={4} strokeLinecap="round" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />;
```
- El kit ya lo hace con `Pictograma` (`video/src/movimiento.tsx`) para los íconos Lucide del catálogo.
- Varios trazos: dibujarlos en orden, cada uno empieza cuando va por ~70 % el anterior.
- Duración proporcional a la longitud (`getLength(d)` de `@remotion/paths`), con un mínimo de ~0.4 s.
- Relleno: aparece con opacidad *después* de cerrar el contorno.

## Errores comunes
- Trazos con `fill` visible desde el principio: se ve la forma antes de dibujarse.
- Misma duración para un punto y una línea larga.
- Línea que tiembla en cada cuadro (si se quiere «a mano», cambiar la semilla 12 veces por segundo; ver [estilo-dibujado](estilo-dibujado.md)).
