# Personajes 2D y 3D (etapa futura)

```json
{
  "id": "personajes",
  "nombre": "Personajes 2D y 3D (etapa futura)",
  "tipo": "tecnica",
  "capacidades": ["personajes-2d", "personajes-3d", "lip-sync", "movimiento-humano", "animacion-tradicional", "render-toon"],
  "herramientas": ["vroid-studio", "three-vrm", "vrm-addon-blender", "blender", "rhubarb-lip-sync", "claude-animation-base", "inochi2d", "live2d-cubism", "opentoonz", "mmd-tools", "hy-motion"],
  "resumen": "Rutas para tener personajes que hablan y actúan, ordenadas por lo que este equipo puede hacer hoy de forma local.",
  "recetas": ["canvas2d/salto", "canvas2d/take", "canvas2d/emociones", "canvas2d/inercia"]
}
```

## Las tres arquitecturas
| Ruta | Herramientas | Sirve para |
|---|---|---|
| A. Anime 2D tradicional | OpenToonz (+ opentoonz-mcp), Grease Pencil de Blender | Acción dibujada; requiere ilustrar y revisar cuadro por cuadro |
| B. Personaje 2D articulado | Inochi2D o Live2D + lip sync | Presentadores que hablan, parpadean y cambian de expresión |
| C. Anime 3D | VRoid → VRM → Blender o three-vrm, movimientos MMD, render toon | Cuerpo completo, cámaras, escenas complejas |

## Orden recomendado en este equipo
1. **Presentador que habla en los videos explicativos**: personaje de VRoid Studio (instalado) exportado a VRM → three-vrm dentro de Remotion. Boca con las expresiones `aa/ih/ou/ee/oh` derivadas de las vocales de la alineación wav2vec2 (ya tenemos tiempos por palabra). Flujo: [personaje-que-habla](../flujos/personaje-que-habla.md).
2. **Caricaturas cortas**: estilo ClaudeAnimationBase (p5.js + p5.brush, MIT) con las reglas de actuación de la Biblioteca de Movimiento (salto, take, emociones, inercia).
3. **Escenas de cuerpo completo**: Blender 5.2 con el VRM (VRM Add-on) y movimientos MMD existentes; render toon con material MToon/EEVEE; insertar como clip.

## Lo que no cabe hoy
HY-Motion (texto → movimiento) pide 24–26 GB de VRAM; la GP100 tiene 16 GB.

## Principios de actuación
Ojos primero, cuerpo después, accesorios al final; anticipación antes de cada acción; cambios de emoción con los ojos casi cerrados; nada sincronizado en espejo. Ver [anticipacion-y-seguimiento](../principios/anticipacion-y-seguimiento.md).
