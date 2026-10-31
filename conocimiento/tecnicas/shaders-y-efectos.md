# Shaders y efectos visuales

```json
{
  "id": "shaders-y-efectos",
  "nombre": "Shaders y efectos visuales",
  "tipo": "tecnica",
  "capacidades": ["shaders", "arte-generativo"],
  "herramientas": ["threejs", "react-three-fiber", "book-of-shaders", "lygia", "pixijs"],
  "resumen": "Gradientes vivos, distorsión, grano y brillos calculados por píxel en la GPU, o con filtros SVG/CSS si basta."
}
```

## Qué es
Un *fragment shader* calcula el color de cada píxel con una fórmula (GLSL). Con un uniforme de tiempo `uTime = frame / fps` el efecto es determinista.

## Opciones de menor a mayor costo
1. **CSS/SVG**: `filter: blur()`, `mix-blend-mode`, gradientes animados con `interpolate`; textura de papel o grano con `<feTurbulence>` (estático) y distorsión con `<feDisplacementMap>`.
2. **Shader en Remotion**: `@remotion/three` + `<mesh><planeGeometry/><shaderMaterial uniforms={{uTime: {value: f / fps}}} .../></mesh>`.
3. **Efectos de Three.js** (`EffectComposer`, bloom) para escenas 3D.

## Reglas
- En este equipo Chromium corre en WSL y puede renderizar WebGL por software: probar con `npx remotion still` antes de un render largo.
- Un efecto debe servir al contenido (separar planos, marcar un cambio), no decorar todo.
- Evitar la estética neón/glow genérica (ver [lista-de-control](../principios/lista-de-control.md)).

## Para aprender
The Book of Shaders (libro, en español). LYGIA da funciones listas pero su licencia restringe el uso comercial.
