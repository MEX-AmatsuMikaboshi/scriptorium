# LanceDB

```json
{
  "id": "lancedb",
  "nombre": "LanceDB",
  "tipo": "infraestructura",
  "areas": ["conocimiento"],
  "prioridad": "futuro",
  "estado_local": "no-instalado",
  "capacidades": ["busqueda-conocimiento"],
  "resumen": "Base vectorial embebida (sin servidor) con búsqueda híbrida texto + vectores; candidata si algún día hace falta búsqueda semántica.",
  "lenguajes": ["Python", "Rust"],
  "web": "https://lancedb.com/docs",
  "repo": "lancedb/lancedb",
  "paquetes": {"pypi": ["lancedb"]},
  "licencia": "Apache-2.0",
  "relacionados": ["sqlite-fts5", "ollama"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Archivos locales en formato Lance; combina búsqueda vectorial y de texto completo.

## Úsalo para
- Solo si las pruebas de consulta (`saber probar`) muestran fallos que los sinónimos no resuelven.

## Limitaciones
- Una dependencia más y embeddings que calcular con Ollama.

## En este equipo
No instalado: hoy la búsqueda por palabras + capacidades pasa las pruebas.
