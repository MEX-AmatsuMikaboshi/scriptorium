# Movimiento de cámara

```json
{
  "id": "camara",
  "nombre": "Movimiento de cámara",
  "tipo": "tecnica",
  "capacidades": ["camara"],
  "herramientas": ["kit-scriptorium", "remotion", "remotion-motion-graphics-skill", "threejs"],
  "resumen": "Cámara viva y motivada: empujes lentos, deriva con ruido, paralaje, sacudidas que decaen y paneos látigo para cambiar de lugar.",
  "recetas": ["canvas2d/camara", "canvas2d/latigo"]
}
```

## Qué es
En 2D la «cámara» es una transformación sobre un contenedor (escala y traslación). Hace que una escena quieta respire y dirige la mirada.

## Movimientos y números
- **Empuje** (*push-in*): escala 1 → 1.06–1.15 a lo largo de la escena con `Easing.inOut`. Acerca al punto importante.
- **Deriva**: `noise2D(semilla, t * 0.15, 0)` × 0.5–1 % del ancho. El kit lo hace con `Camara` (`movimiento.tsx`) y una semilla por escena.
- **Paralaje**: capas a distintas velocidades (fondo 0.3×, medio 0.6×, frente 1×) = profundidad sin 3D.
- **Sacudida** en impactos: amplitud que decae a cero en ~0.3 s, cambiando de posición a 24 Hz.
- **Paneo látigo**: cruza en 0.2–0.3 s con *ease* fuerte, estela o desenfoque de movimiento; el corte ocurre a media velocidad.
- 3D: mover la cámara sobre una curva suave (no en línea recta) y mirar a un objetivo que también se mueve un poco.

## Reglas
- Toda cámara tiene un motivo: revelar, seguir, enfatizar.
- No mover cámara y texto con amplitudes grandes a la vez: el texto debe poder leerse.
- Una escena = un movimiento principal.
