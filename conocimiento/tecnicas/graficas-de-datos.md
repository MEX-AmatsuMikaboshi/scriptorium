# Gráficas, números y mapas animados

```json
{
  "id": "graficas-de-datos",
  "nombre": "Gráficas, números y mapas animados",
  "tipo": "tecnica",
  "capacidades": ["datos-graficas", "mapas-geograficos"],
  "herramientas": ["d3", "remotion", "remotion-bits", "map-motion"],
  "resumen": "Barras que crecen, líneas que se trazan, contadores y mapas con rutas: primero el marco, luego los datos, luego el dato importante.",
  "recetas": ["canvas2d/grafica"]
}
```

## Orden de lectura
1. Marco: ejes, título y unidades (aparecen rápido).
2. Datos: barras desde la línea base con escalonado de 3–6 cuadros; líneas que se dibujan con `evolvePath`.
3. Énfasis: el dato que importa cambia de color o crece; los demás bajan a 40 % de opacidad.
4. Etiqueta del valor: aparece cuando la barra ya llegó.

## Cómo se hace
- Escalas con `d3-scale` (`scaleLinear`, `scaleBand`, `scaleTime`) calculadas una vez; React dibuja los `<rect>`/`<path>`.
- Línea: `d3-shape` `line().curve(curveMonotoneX)` → `d` → `evolvePath(p, d)`.
- Contador: `Math.round(interpolate(f, [a, b], [0, valor], {easing: Easing.out(Easing.cubic)}))` con `Intl.NumberFormat('es-MX')`.
- Mapa: `d3-geo` (`geoNaturalEarth1`, `geoPath`) sobre GeoJSON de dominio público (Natural Earth); ruta con `evolvePath`; acercamiento con la cámara.

## Reglas
- Una gráfica = un mensaje; dilo en el título.
- No animes todo a la vez ni con la misma curva.
- Cuida la fuente de los datos y cítala en pantalla.
