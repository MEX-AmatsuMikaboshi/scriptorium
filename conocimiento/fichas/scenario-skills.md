# Scenario Agent Skills

```json
{
  "id": "scenario-skills",
  "nombre": "Scenario Agent Skills",
  "tipo": "skill",
  "areas": ["3d", "personajes", "anime"],
  "prioridad": "futuro",
  "estado_local": "no-instalado",
  "capacidades": ["control-por-agente", "personajes-3d", "movimiento-humano", "animacion-tradicional", "render-toon", "lip-sync"],
  "resumen": "Skills de Scenario: la mayoría usan su servicio de generación (de pago), pero las «expert tools» para Blender (animación, rigging, Grease Pencil, iluminación…) solo necesitan la aplicación.",
  "lenguajes": ["Markdown", "Python"],
  "exporta_video": "no-aplica",
  "web": "https://www.skills.sh/scenario-labs/skills",
  "repo": "scenario-labs/skills",
  "licencia": "MIT",
  "agentes": "Formato Agent Skills; Claude Code, Cursor, Codex, Copilot y más de 70 agentes.",
  "relacionados": ["blender", "blender-mcp", "agent-skills"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Familia experta de Blender: `scenario-blender-expert` (líder: Python sin interfaz o por puente MCP, ciclo de revisión), `-animation` (ciclos, saltos, actuación y lip sync, de bloqueo escalonado a curvas, timing y spacing), `-rigging` (Rigify, pesos, IK/FK), `-grease-pencil` (2D y 2.5D, cuadro por cuadro y recortes), `-lighting-rendering`, `-texturing-shading`, `-sculpting`, `-retopology`, `-hair`, `-hard-surface`, `-blockout`, `-export` (glTF/FBX/USDZ para motores y three.js). También hay familias para ZBrush, Maya, Unreal, Unity, Godot y Roblox.

## Úsalo para
- Dar a un agente conocimiento experto de Blender sin usar el servicio de Scenario.

## No lo uses para
- Las skills `scenario-*` sin «blender»: requieren el servidor MCP de Scenario (servicio de pago).

## Instalación
```bash
npx skills add scenario-labs/skills   # en el menú, elegir el grupo «Expert tools» de Blender
```
Una familia se instala completa porque sus especialistas importan los scripts del líder. Para fijar una versión revisada, usar el commit de un release.

## Limitaciones
- Escritas para Blender 5.x y modelos grandes.
- El instalador baja la última versión de `main`: revisar antes.

## En este equipo
No instalado. Blender 5.2.2 ya está; cuando se empiece con 3D, instalar solo la familia de Blender.
