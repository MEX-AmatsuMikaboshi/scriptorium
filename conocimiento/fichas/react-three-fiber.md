# React Three Fiber

```json
{
  "id": "react-three-fiber",
  "nombre": "React Three Fiber",
  "tipo": "libreria",
  "areas": ["3d"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["escena-3d", "camara"],
  "resumen": "Renderizador de React para Three.js: escenas 3D como componentes JSX; es lo que usa @remotion/three.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "indirecto",
  "web": "https://docs.pmnd.rs/react-three-fiber",
  "repo": "pmndrs/react-three-fiber",
  "paquetes": {"npm": ["@react-three/fiber"]},
  "licencia": "MIT",
  "relacionados": ["threejs", "drei", "remotion-template-three"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`<Canvas>` con `<mesh>`, `<boxGeometry>`, `<meshStandardMaterial>`… como JSX. En Remotion se usa `<ThreeCanvas>` y se anima con `useCurrentFrame()`, no con `useFrame`.

## Úsalo para
- 3D dentro del kit de Remotion con la misma forma de escribir que el resto de escenas.

## Instalación
```bash
npm i three @react-three/fiber
```

## Limitaciones
- Versión mayor ligada a la de React (React 19 → fiber 9).

## En este equipo
No instalado. El kit usa React 19.3.1.
