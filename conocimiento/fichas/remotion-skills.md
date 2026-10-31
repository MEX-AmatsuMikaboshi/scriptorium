# Remotion Agent Skills

```json
{
  "id": "remotion-skills",
  "nombre": "Remotion Agent Skills",
  "tipo": "skill",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["composicion-video", "control-por-agente"],
  "resumen": "Skills oficiales de Remotion (formato Agent Skills): buenas prácticas de markup, crear proyectos, abrir Studio, renderizar y actualizar.",
  "lenguajes": ["Markdown"],
  "exporta_video": "no-aplica",
  "repo": "remotion-dev/skills",
  "docs": ["https://www.remotion.dev/docs/ai/skills"],
  "licencia": "El repositorio no declara licencia (consultado 2026-10-31): léelo y úsalo, pero no copies su texto a otro proyecto público.",
  "agentes": "Claude Code, Codex, Cursor y otros compatibles con Agent Skills.",
  "relacionados": ["remotion", "remotion-motion-graphics-skill", "agent-skills"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Colección mantenida por Remotion con las skills `/remotion-best-practices` (engloba a las demás), `/remotion-create`, `/remotion-markup` (composiciones, animación, layout, tipografía, medios, efectos, audio, fuentes, timing), `/remotion-studio`, `/remotion-render` y una de actualización.

## Úsalo para
- Dar a un agente las reglas correctas de Remotion antes de escribir escenas.
- Referencia para un modelo local: sus reglas son Markdown legible.

## Instalación
```bash
npx skills add remotion-dev/skills
# o: gh skill install remotion-dev/skills
```
Revisa qué instala el asistente `skills` antes de aceptar (escribe en las carpetas de skills de tus agentes).

## Ventajas
- Oficial y al día con la versión de Remotion.
- Formato estándar: sirve para varios agentes.

## Limitaciones
- Pensadas para modelos grandes con herramientas; un modelo local de 12–14B necesita la parte relevante, no todas.
- Sin licencia declarada.

## En este equipo
No instalado. Para modelos locales conviene usar `saber contexto` y la llms.txt de Remotion (se baja con `saber actualizar`).
