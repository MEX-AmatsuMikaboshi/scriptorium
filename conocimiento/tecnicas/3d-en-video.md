# Objetos y modelos 3D dentro del video

```json
{
  "id": "3d-en-video",
  "nombre": "Objetos y modelos 3D dentro del video",
  "tipo": "tecnica",
  "capacidades": ["escena-3d", "camara", "personajes-3d"],
  "herramientas": ["remotion-template-three", "react-three-fiber", "threejs", "drei", "blender", "three-vrm"],
  "resumen": "Dos caminos: 3D en vivo dentro de Remotion (Three.js) o un clip prerenderizado en Blender que se inserta como video con transparencia."
}
```

## Camino A: 3D en vivo en Remotion
- `@remotion/three` → `<ThreeCanvas width height>` con React Three Fiber dentro; modelos glTF/GLB con `useGLTF` (drei).
- Todo se anima con `useCurrentFrame()`: cámara, rotaciones, luces. Las animaciones que trae el glTF se posicionan con `mixer.setTime(f / fps)`; nunca `useFrame` ni `clock`.
- Ventaja: cambiar texto, colores o cámara es cambiar props. Desventaja: Chromium sin GPU en WSL es lento con sombras y postprocesado.

## Camino B: clip prerenderizado
- Blender (o Unity) renderiza una secuencia PNG con canal alfa; ffmpeg la convierte (`-c:v prores_ks -profile:v 4444` o `-c:v libvpx-vp9 -pix_fmt yuva420p`) y Remotion la inserta con `<OffthreadVideo transparent>` o una secuencia de `<Img>`.
- Ventaja: calidad de render de Blender (EEVEE/Cycles, toon). Desventaja: cualquier cambio exige volver a renderizar.

## Cuál elegir
- Objetos simples, diagramas 3D, globo terráqueo, maquetas → A.
- Personajes con rig, ropa, pelo, iluminación cuidada → B.

## Reglas
- Iluminación de tres puntos simple y fondo coherente con el tema del kit.
- Cámara lenta y motivada (ver [camara](camara.md)); un objeto 3D girando sin parar no explica nada.
- Flujo completo: [modelo-3d-en-video](../flujos/modelo-3d-en-video.md).
