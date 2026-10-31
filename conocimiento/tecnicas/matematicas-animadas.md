# Matemáticas animadas

```json
{
  "id": "matematicas-animadas",
  "nombre": "Matemáticas animadas",
  "tipo": "tecnica",
  "capacidades": ["matematicas"],
  "herramientas": ["manim", "katex", "motion-canvas"],
  "resumen": "Ecuaciones y figuras matemáticas: KaTeX para mostrarlas en el kit, Manim para transformarlas y demostrarlas."
}
```

## Opciones
- **Mostrar** una fórmula que aparece por partes: KaTeX dentro de Remotion (HTML), revelando términos con opacidad.
- **Transformar** una fórmula en otra (despejar, sustituir) o animar geometría y funciones: Manim (`TransformMatchingTex`, `Create`, `axes.plot`), renderizado como clip e insertado en el video ([clip-de-manim-en-remotion](../flujos/clip-de-manim-en-remotion.md)).
- **Diagramas con LaTeX** en un editor con línea de tiempo: Motion Canvas (`Latex`).

## Reglas
- Una transformación por paso, con pausa para leer el resultado.
- Colorear el término que cambia igual en la fórmula y en la figura.
- Acentos en Manim: `Text` (Pango) para español; `Tex` necesita configuración de babel/UTF-8.
