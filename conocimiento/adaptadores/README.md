# Conectar la biblioteca a un agente o a otro proyecto

Rutas en este equipo:

- Linux/WSL: `/home/gaber/scriptorium/conocimiento`, que es lo mismo que `/mnt/c/Users/gaber/Documents/Scriptorium/conocimiento`.
- Windows: `C:\Users\gaber\Documents\Scriptorium\conocimiento`.

Hay cuatro maneras de conectarla. No son excluyentes: la primera sirve para todos los agentes.

## 1. Una línea en las instrucciones del proyecto (cualquier agente)
Agrega esto al `AGENTS.md` (Codex, OpenCode y otros), al `CLAUDE.md` o al `GEMINI.md` del proyecto:

```markdown
## Animación y video
Antes de diseñar o programar animaciones o video, consulta la biblioteca de conocimiento audiovisual:
`saber buscar "<petición>"` (en Windows `saber.cmd`; en Linux `~/.local/bin/saber`). Instrucciones completas:
/home/gaber/scriptorium/conocimiento/AGENTS.md
```
- Claude Code también admite importarla entera con `@/home/gaber/scriptorium/conocimiento/AGENTS.md` (o la ruta de
  Windows), aunque eso carga unas 60 líneas en cada sesión.
- Gemini CLI también importa archivos con `@ruta` dentro de `GEMINI.md`, o lee `AGENTS.md` si en `settings.json` pones
  `"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}`.

## 2. Skill (formato Agent Skills)
Copia la carpeta `skill/saber-audiovisual/`:

- **Claude Code**: a `~/.claude/skills/` (para todos los proyectos) o a `<proyecto>/.claude/skills/`.
- **Codex**: a `<repo>/.agents/skills/`. Es la ruta que documenta OpenAI; la ruta global no quedó confirmada.
- **Otros con Agent Skills** (OpenCode, Cursor…): en su carpeta de skills.

La skill solo dice cuándo consultar y con qué comandos; el conocimiento sigue viviendo aquí.

## 3. Servidor MCP (herramientas `buscar`, `ver`, `contexto`, `capacidades`)
`mcp/servidor.py` es un servidor stdio sin dependencias. Su protocolo se probó con mensajes JSON-RPC directos
(`initialize`, `tools/list`, `tools/call`); todavía no se registró en ningún cliente de este equipo.

| Cliente | Registro |
|---|---|
| Claude Code (Linux/WSL) | `claude mcp add -s user saber -- python3 /home/gaber/scriptorium/conocimiento/adaptadores/mcp/servidor.py` |
| Claude Code (Windows) | `claude mcp add -s user saber -- "C:\Program Files\WSL\wsl.exe" -d Ubuntu-24.04 -u gaber -- python3 /home/gaber/scriptorium/conocimiento/adaptadores/mcp/servidor.py` |
| Codex (`~/.codex/config.toml`) | `[mcp_servers.saber]` con `command = "python3"` y `args = ["/home/gaber/scriptorium/conocimiento/adaptadores/mcp/servidor.py"]` |
| Gemini CLI (`~/.gemini/settings.json`) | `"mcpServers": {"saber": {"command": "python3", "args": ["/home/gaber/…/servidor.py"]}}` |
| OpenCode, LM Studio, Open WebUI | Cada uno tiene su archivo de MCP: usar el mismo comando (por verificar con su documentación) |

Con modelos locales chicos, el MCP ayuda si el cliente maneja bien las llamadas a herramientas. Si no, es más fiable
la opción 4.

## 4. Sin herramientas: contexto en el prompt (modelos locales)
Para un modelo de Ollama sin herramientas (como el director de Scriptorium), arma el contexto antes y pégalo:
```bash
saber contexto "escena de línea del tiempo con fechas que aparecen al nombrarse" --tokens 3000 > /tmp/contexto.md
```
Desde Python, en cualquier proyecto:
```python
import sys; sys.path.insert(0, "/home/gaber/scriptorium/conocimiento/herramientas")
import saber
texto = saber.contexto("partículas que salen de un golpe", tokens=2500)
resultado = saber.buscar("partículas")   # dict con capacidades y grupos
```
