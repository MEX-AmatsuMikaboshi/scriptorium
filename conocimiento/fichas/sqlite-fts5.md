# SQLite FTS5

```json
{
  "id": "sqlite-fts5",
  "nombre": "SQLite FTS5",
  "tipo": "infraestructura",
  "areas": ["conocimiento"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["busqueda-conocimiento"],
  "resumen": "Búsqueda de texto completo integrada en SQLite (y en Python estándar): el índice de esta biblioteca, sin servidores ni dependencias.",
  "web": "https://www.sqlite.org/fts5.html",
  "licencia": "Dominio público.",
  "relacionados": ["lancedb", "ollama"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md", "bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Tablas virtuales con índice invertido y ranking BM25. `saber.py` guarda fichas, técnicas, recetas y documentación descargada en `.cache/indice.sqlite` con raíces en español e inglés.

## Úsalo para
- Búsqueda por palabras y capacidades, rápida y verificable.

## Limitaciones
- No entiende sinónimos por sí sola: por eso existe `catalogo/capacidades.json`.

## En este equipo
En uso (Python 3.12, SQLite 3.45.1 en WSL).
