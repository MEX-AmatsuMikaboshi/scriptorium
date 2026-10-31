# Plantilla Remotion + React Three Fiber

```json
{
  "id": "remotion-template-three",
  "nombre": "Plantilla Remotion + React Three Fiber",
  "tipo": "plantilla",
  "areas": ["3d", "video-explicativo"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["escena-3d", "camara", "composicion-video"],
  "resumen": "Plantilla mínima oficial de Remotion con React Three Fiber: el punto de partida para meter objetos y modelos 3D en un video.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "web": "https://www.remotion.dev/templates/three",
  "repo": "remotion-dev/template-three",
  "paquetes": {"npm": ["@remotion/three"]},
  "licencia": "MIT",
  "agentes": "Ejemplo pequeño y legible.",
  "relacionados": ["remotion", "react-three-fiber", "threejs", "drei"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Proyecto base que usa `<ThreeCanvas>` de `@remotion/three` para que la escena de Three.js avance con `useCurrentFrame()` en vez del reloj del navegador.

## Úsalo para
- Modelos glTF/GLB exportados de Blender o VRoid dentro de una escena del kit.
- Objetos 3D simples (globo terráqueo, poliedros, maquetas) con cámara animada.

## Instalación
```bash
npx create-video@latest   # elige la plantilla «Three»
# o en un proyecto existente: @remotion/three + three + @react-three/fiber (misma versión que remotion)
```

## Limitaciones
- Render 3D en Chromium por software si no hay GPU en WSL: lento con escenas pesadas.
- Animar con el cuadro, nunca con `useFrame` ni el reloj.

## En este equipo
No instalado. Ver flujo [modelo-3d-en-video](../flujos/modelo-3d-en-video.md).
