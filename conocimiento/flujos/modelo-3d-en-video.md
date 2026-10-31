# Meter un modelo 3D en un video

```json
{
  "id": "modelo-3d-en-video",
  "nombre": "Meter un modelo 3D en un video",
  "tipo": "flujo",
  "prioridad": "complemento",
  "capacidades": ["escena-3d", "personajes-3d", "camara"],
  "herramientas": ["blender", "vroid-studio", "remotion-template-three", "react-three-fiber", "drei", "ffmpeg"],
  "resumen": "De Blender o VRoid a una escena del video: exportar glTF y animarlo en Remotion, o renderizar un clip con transparencia e insertarlo."
}
```

## 1. Preparar el modelo
- **Blender 5.2** (instalado): limpiar escala (1 unidad = 1 m), aplicar transformaciones, materiales PBR simples.
- **VRoid Studio** (instalado): exportar VRM; en Blender con el VRM Add-on si hay que posarlo o reanimarlo.
- Sin interfaz: `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b modelo.blend -P exportar.py` con `bpy.ops.export_scene.gltf(filepath=..., export_format='GLB')`.

## 2a. En vivo en Remotion
1. Paquetes `@remotion/three`, `three`, `@react-three/fiber`, `@react-three/drei` en la misma versión que pida Remotion (agregar con `npm_agregar.sh`).
2. `<ThreeCanvas>` + `useGLTF(staticFile('modelo.glb'))` + luces.
3. Cámara y rotaciones con `interpolate(useCurrentFrame(), …)`; animaciones del GLB con `AnimationMixer.setTime(f / fps)`.
4. Probar con `npx remotion still` (WebGL por software en WSL: vigilar tiempos).

## 2b. Clip prerenderizado
1. En Blender: cámara, luz, fondo transparente (Film → Transparent), salida PNG RGBA, 60 fps.
2. `ffmpeg -framerate 60 -i f_%04d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le clip.mov` (o VP9 con alfa en WebM).
3. En Remotion: `<OffthreadVideo src={staticFile('clip.mov')} transparent />` dentro de la escena.

## Licencias
Modelos descargados (Sketchfab, BOOTH, MMD): revisar uso permitido y crédito obligatorio.
