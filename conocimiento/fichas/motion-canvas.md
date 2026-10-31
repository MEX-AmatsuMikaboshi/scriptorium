# Motion Canvas

```json
{
  "id": "motion-canvas",
  "nombre": "Motion Canvas",
  "tipo": "motor",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["composicion-video", "video-explicativo", "diagramas", "matematicas", "tipografia-cinetica", "morphing", "editor-visual", "sincronia-audio"],
  "resumen": "Animaciones vectoriales explicativas con TypeScript y generadores: el código describe la secuencia en orden y un editor muestra la línea de tiempo con el audio.",
  "lenguajes": ["TypeScript"],
  "exporta_video": "si",
  "web": "https://motion-canvas.io",
  "repo": "motion-canvas/motion-canvas",
  "paquetes": {"npm": ["@motion-canvas/core", "@motion-canvas/2d"]},
  "docs": ["https://motion-canvas.io/docs"],
  "licencia": "MIT",
  "agentes": "Sin skills oficiales; API pequeña y regular, apta para agentes.",
  "relacionados": ["revideo", "remotion", "manim", "motion-canvas-examples"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md", "bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Librería + editor (Vite) para animaciones explicativas. Las escenas son funciones generadoras: `yield* circle().scale(2, 0.6)` espera a que termine cada paso, así el código se lee como un guion. Tiene nodos 2D (Rect, Circle, Txt, Latex, Code, Line), señales reactivas y marcadores de tiempo sincronizables con la voz.

## Úsalo para
- Explicaciones paso a paso (diagramas que se construyen, código que se transforma, LaTeX).
- Cuando se quiere ajustar a mano el timing contra la narración en el editor.

## No lo uses para
- Render en servidor sin interfaz a gran escala (para eso existe Revideo).
- Plantillas parametrizadas desde datos: Remotion es más directo.

## Instalación
```bash
npm init @motion-canvas@latest
```

## Ejemplo mínimo
```ts
export default makeScene2D(function* (view) {
  const c = createRef<Circle>();
  view.add(<Circle ref={c} size={120} fill="#e13238" />);
  yield* c().scale(2, 0.6);
  yield* all(c().position.x(300, 1), c().fill('#e6a700', 1));
});
```

## Ventajas
- Código secuencial muy legible.
- Excelente para diagramas, código y matemáticas.
- MIT.

## Limitaciones
- El render a video normal pasa por el editor en el navegador.
- Ecosistema más chico que Remotion; los ejemplos oficiales no se actualizan desde 2024.

## En este equipo
No instalado. Alternativa a evaluar para escenas de diagramas; para no mezclar motores, preferir clips exportados que Remotion integra.
