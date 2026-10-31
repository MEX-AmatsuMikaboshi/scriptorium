# Personaje anime que habla en el video

```json
{
  "id": "personaje-que-habla",
  "nombre": "Personaje anime que habla en el video",
  "tipo": "flujo",
  "prioridad": "futuro",
  "capacidades": ["personajes-3d", "lip-sync", "render-toon"],
  "herramientas": ["vroid-studio", "three-vrm", "remotion-template-three", "wav2vec2-alineacion", "rhubarb-lip-sync"],
  "resumen": "Plan para un presentador anime: VRoid → VRM → three-vrm en Remotion, con boca, parpadeo y gestos sincronizados con la voz alineada."
}
```

## Plan (sin probar todavía)
1. **Personaje**: diseñarlo en VRoid Studio (instalado) y exportar VRM. Guardar sus términos de uso.
2. **Carga**: `GLTFLoader` + `VRMLoaderPlugin` de three-vrm dentro de `<ThreeCanvas>` (`@remotion/three`).
3. **Boca**: de la alineación wav2vec2 (tiempos por palabra; por carácter si se expone) derivar las vocales y mapearlas a las expresiones `aa`, `ih`, `ou`, `ee`, `oh` con transiciones de 2–3 cuadros; boca cerrada en silencios. Alternativa: Rhubarb Lip Sync (reconocedor fonético) → JSON de formas de boca.
4. **Vida**: parpadeo cada 2–6 s con `random(semilla)`, mirada que sigue al texto en pantalla, respiración (pecho 1 %), gestos de manos en palabras clave (poses predefinidas interpoladas).
5. **Física de pelo**: `vrm.update(1 / fps)` llamado desde el cuadro 0 hasta el actual (determinista) o desactivar resortes.
6. **Render**: plano medio fijo con deriva de cámara; el personaje en un tercio y el texto en el otro.

## Riesgos
Render WebGL por software en WSL (lento); valle inquietante si la boca no coincide: probar primero 10 s.
