# Three.js

```json
{
  "id": "threejs",
  "nombre": "Three.js",
  "tipo": "libreria",
  "areas": ["3d", "motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["escena-3d", "camara", "shaders", "particulas"],
  "resumen": "La librería 3D estándar de la web (WebGL/WebGPU): escenas, cámaras, luces, materiales, modelos glTF, sombras y postprocesado.",
  "lenguajes": ["JavaScript", "TypeScript"],
  "exporta_video": "indirecto",
  "web": "https://threejs.org",
  "repo": "mrdoob/three.js",
  "paquetes": {"npm": ["three"]},
  "docs": ["https://threejs.org/docs", "https://threejs.org/examples"],
  "licencia": "MIT",
  "agentes": "Muy conocida por los modelos; cuidado con APIs viejas (cambia en cada versión r1xx).",
  "relacionados": ["react-three-fiber", "drei", "remotion-template-three", "three-vrm"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md", "bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Grafo de escena con `Scene`, `PerspectiveCamera`, `Mesh` (geometría + material), luces, `GLTFLoader` para modelos, `ShaderMaterial` para GLSL propio y `EffectComposer` para postprocesado.

## Úsalo para
- Objetos y modelos 3D dentro de videos (vía @remotion/three).
- Partículas en GPU y efectos con shaders.

## No lo uses para
- Animación de personajes compleja hecha a mano (mejor en Blender y exportar glTF con la animación).

## Instalación
```bash
npm i three
```

## Ventajas
- Estándar de facto, ejemplos para casi todo.
- glTF como formato de intercambio con Blender y VRoid.

## Limitaciones
- API cambia entre versiones: fijar versión.
- En Chromium sin GPU (WSL) el render es por software: lento con sombras o postprocesado.

## En este equipo
No instalado. Se usaría con la misma versión que pida @remotion/three.
