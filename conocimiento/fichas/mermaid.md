# Mermaid

```json
{
  "id": "mermaid",
  "nombre": "Mermaid",
  "tipo": "libreria",
  "areas": ["video-explicativo"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["diagramas"],
  "resumen": "Diagramas desde texto tipo Markdown (flujo, secuencia, estados, línea del tiempo, mapas mentales) renderizados a SVG.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://mermaid.js.org",
  "repo": "mermaid-js/mermaid",
  "paquetes": {"npm": ["mermaid"]},
  "licencia": "MIT",
  "agentes": "Los modelos chicos escriben Mermaid muy bien: buen formato intermedio para que un LLM describa un diagrama.",
  "relacionados": ["d3", "markmap"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
El LLM escribe `graph TD; A-->B` y Mermaid lo dibuja. Para animar: renderizar a SVG y revelar nodos y aristas en orden.

## Úsalo para
- Que el director LLM describa un diagrama con texto validable en vez de coordenadas.

## Instalación
```bash
npm i mermaid
```

## Limitaciones
- El SVG final no está pensado para animarse: hay que identificar nodos por id.
- Diseño visual limitado sin CSS propio.

## En este equipo
No instalado. Interesante para escenas de esquema argumental.
