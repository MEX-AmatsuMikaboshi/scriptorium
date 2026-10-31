# Blender

```json
{
  "id": "blender",
  "nombre": "Blender",
  "tipo": "aplicacion",
  "areas": ["3d", "personajes", "anime"],
  "prioridad": "complemento",
  "estado_local": "instalado",
  "capacidades": ["escena-3d", "personajes-3d", "movimiento-humano", "animacion-tradicional", "render-toon", "camara", "control-por-agente"],
  "resumen": "Suite 3D libre (modelado, rigging, animación, Grease Pencil 2D, render EEVEE/Cycles) con API de Python; instalada la 5.2.2.",
  "lenguajes": ["Python"],
  "exporta_video": "si",
  "web": "https://www.blender.org",
  "repo": "blender/blender",
  "docs": ["https://docs.blender.org/api/current/", "https://docs.blender.org/manual/en/latest/"],
  "licencia": "GPL-2.0-or-later (lo que tú creas con Blender es tuyo).",
  "agentes": "API `bpy` completa; scripts sin interfaz con `blender -b archivo.blend -P script.py`; MCP comunitario (blender-mcp) y skills expertas (scenario-skills).",
  "relacionados": ["blender-mcp", "scenario-skills", "vrm-addon-blender", "mmd-tools", "remotion-template-three"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Todo el ciclo 3D y también 2D con Grease Pencil. Se automatiza por completo con Python, con o sin interfaz.

## Úsalo para
- Crear o preparar modelos y exportarlos a glTF/GLB para Three.js/Remotion.
- Renderizar clips (PNG con alfa) de personajes u objetos para insertarlos en el video.
- Animación 2D/2.5D con Grease Pencil (etapa de caricaturas).

## No lo uses para
- Motion graphics de texto y diagramas: más rápido en Remotion.

## Instalación
Instalada en Windows: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` (firmada, el Control inteligente la permite).
Sin interfaz: `blender.exe -b escena.blend -P script.py -- argumentos`.

## Ventajas
- Libre, completo y automatizable.
- Exporta glTF, FBX, USD, video y secuencias de imágenes.

## Limitaciones
- Curva de aprendizaje alta; la calidad depende de modelos, rigs y dirección de arte, no del código.
- Render Cycles lento; EEVEE usa la GPU.

## En este equipo
Instalada 5.2.2 en Windows. Desde WSL se puede invocar el .exe por interoperabilidad (por probar).
