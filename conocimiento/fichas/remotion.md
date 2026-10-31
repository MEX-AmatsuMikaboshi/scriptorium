# Remotion

```json
{
  "id": "remotion",
  "nombre": "Remotion",
  "tipo": "motor",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["composicion-video", "video-explicativo", "tipografia-cinetica", "transiciones", "subtitulos-karaoke", "sincronia-audio", "camara", "escena-3d", "lottie", "visualizacion-audio", "datos-graficas"],
  "resumen": "Videos con React: cada cuadro es una función del número de cuadro; render a MP4 sin cabeza. Es el motor del kit de Scriptorium.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "web": "https://www.remotion.dev",
  "repo": "remotion-dev/remotion",
  "paquetes": {"npm": ["remotion", "@remotion/cli", "@remotion/transitions", "@remotion/noise", "@remotion/paths", "@remotion/shapes", "@remotion/three", "@remotion/lottie", "@remotion/media-utils", "@remotion/captions"]},
  "docs": ["https://www.remotion.dev/docs", "https://www.remotion.dev/docs/ai/skills"],
  "llms_txt": "https://www.remotion.dev/llms.txt",
  "licencia": "Remotion License: gratis para personas, empresas con hasta 3 empleados, organizaciones sin fines de lucro y evaluación; las demás empresas necesitan Company License.",
  "agentes": "Skills oficiales (remotion-dev/skills), llms.txt y docs de IA. Plantillas y componentes listos (remotion-bits, snapcn).",
  "requisitos": "Node; Chromium sin cabeza (Remotion lo descarga). En este equipo corre en WSL con 8 hilos de CPU.",
  "relacionados": ["remotion-skills", "remotion-bits", "snapcn", "remotion-plantillas", "motion-canvas", "revideo", "hyperframes", "kit-scriptorium"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md", "bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Framework para escribir videos como componentes de React. `useCurrentFrame()` da el cuadro actual; `interpolate()` y `spring()` convierten el cuadro en posición, opacidad o escala. `<Sequence>` y `<Series>` ordenan escenas, `<Audio>`/`<Video>`/`<OffthreadVideo>` meten medios, y `npx remotion render` produce MP4/WebM/GIF o cuadros sueltos.

## Úsalo para
- Videos explicativos con voz, subtítulos y escenas parametrizadas desde JSON (lo que hace Scriptorium).
- Plantillas de datos: el mismo componente con distintos props genera muchos videos.
- Mezclar en un mismo video DOM, SVG, Canvas, Three.js (@remotion/three), Lottie (@remotion/lottie) y clips externos (Manim, Blender).

## No lo uses para
- Animación de personajes cuadro por cuadro (mejor Blender/OpenToonz y traer el clip).
- Edición manual de video sin código (usa un editor).

## Instalación
```bash
# Proyecto nuevo
npx create-video@latest
# En Scriptorium NO uses npm install dentro de video/: usa herramientas_wsl/npm_agregar.sh paquete@versión
```

## Ejemplo mínimo
```tsx
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
export const Titulo: React.FC<{texto: string}> = ({texto}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 14}});
  return <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
    <h1 style={{opacity: interpolate(f, [0, 12], [0, 1], {extrapolateRight: 'clamp'}), transform: `scale(${0.8 + 0.2 * s})`}}>{texto}</h1>
  </AbsoluteFill>;
};
```

## Ventajas
- Determinista: el cuadro N siempre se ve igual; se puede renderizar en paralelo y reanudar.
- Todo el ecosistema web (CSS, SVG, fuentes, React) sirve tal cual.
- Paquetes oficiales para transiciones, ruido, trazos SVG, 3D, Lottie, audio y subtítulos.
- El mejor soporte para agentes: skills oficiales y llms.txt.

## Limitaciones
- Licencia comercial para empresas de más de 3 personas.
- Render en CPU con Chromium: lento para 1080p60 largos (en este equipo ~5 min por 2 min de video).
- Nada de `Math.random()` ni estado entre cuadros: usar `random(semilla)` de Remotion.

## En este equipo
En uso: Remotion 4.0.539 en `video/` (enlace a node_modules en Linux), con @remotion/transitions y @remotion/noise. Render con `npx remotion render src/index.ts Explicador`. Ver [kit-scriptorium](kit-scriptorium.md).
