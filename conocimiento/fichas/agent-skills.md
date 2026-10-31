# Agent Skills (estándar)

```json
{
  "id": "agent-skills",
  "nombre": "Agent Skills (estándar)",
  "tipo": "referencia",
  "areas": ["conocimiento"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["control-por-agente"],
  "resumen": "Formato abierto de skills: una carpeta con SKILL.md (name + description en el encabezado) que el agente carga solo cuando la necesita.",
  "web": "https://agentskills.io",
  "docs": ["https://developers.openai.com/codex/skills", "https://code.claude.com/docs/en/skills"],
  "licencia": "Especificación abierta.",
  "agentes": "Claude Code (`.claude/skills/`), Codex (`.agents/skills/` en el repo), OpenCode, Cursor y otros. Gemini CLI usa GEMINI.md (puede importar AGENTS.md con @).",
  "relacionados": ["remotion-skills", "scenario-skills"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
Una skill es un directorio con `SKILL.md`; el agente ve al inicio solo nombre y descripción y lee el resto cuando decide usarla. La biblioteca trae una en `adaptadores/skill/saber-audiovisual/`.

## Úsalo para
- Conectar esta biblioteca a Claude Code o Codex en cualquier proyecto.

## Limitaciones
- Las rutas de usuario varían por agente (Codex documenta oficialmente `.agents/skills` del repo; la ruta global no quedó confirmada).

## En este equipo
Skill propia en `adaptadores/skill/` (ver README de la biblioteca).
