# Ollama

```json
{
  "id": "ollama",
  "nombre": "Ollama",
  "tipo": "infraestructura",
  "areas": ["conocimiento"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["busqueda-conocimiento"],
  "resumen": "Servidor local de modelos (en Windows, alcanzado desde WSL en 127.0.0.1:11434): gemma4:12b por defecto y qwen3:14b; también sirve modelos de embeddings.",
  "web": "https://ollama.com",
  "repo": "ollama/ollama",
  "licencia": "MIT (cada modelo tiene su propia licencia).",
  "agentes": "Los agentes locales (OpenCode, Codex en modo local, Open WebUI) usan Ollama como proveedor.",
  "relacionados": ["sqlite-fts5", "lancedb"],
  "fuentes": ["CLAUDE.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
API HTTP local para chat, generación con esquema JSON y embeddings. Scriptorium la usa en `llm.py` con reintentos y caché.

## Úsalo para
- Todo lo que haga el «agente local»: el contexto de esta biblioteca (`saber contexto`) se pega en su prompt.

## Limitaciones
- RAM de 16 GB justa: ya se cayó una vez con std::bad_alloc.
- Modelos de 12–14B: necesitan contexto corto y preciso (por eso existen `--breve` y `contexto`).

## En este equipo
En uso: Ollama 0.40 en Windows.
