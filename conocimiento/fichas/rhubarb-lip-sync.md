# Rhubarb Lip Sync

```json
{
  "id": "rhubarb-lip-sync",
  "nombre": "Rhubarb Lip Sync",
  "tipo": "herramienta",
  "areas": ["personajes", "2d", "audio-voz"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["lip-sync", "personajes-2d"],
  "resumen": "CLI que genera la animación de boca 2D a partir de una grabación de voz: posiciones de boca con tiempos en JSON, XML o TSV.",
  "lenguajes": ["CLI"],
  "exporta_video": "no-aplica",
  "repo": "DanielSWolf/rhubarb-lip-sync",
  "licencia": "por verificar (GitHub no reconoce el archivo de licencia).",
  "agentes": "CLI con salida JSON: muy fácil de integrar en un pipeline.",
  "relacionados": ["wav2vec2-alineacion", "live2d-cubism", "inochi2d", "three-vrm"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "parcial"
}
```

## Qué es
Analiza el audio (y opcionalmente el guion) y devuelve una secuencia de formas de boca al estilo Hanna-Barbera/Preston Blair (A–F más extras) con sus tiempos.

## Úsalo para
- Personajes 2D que hablan con la voz del narrador (etapa de caricaturas).

## Instalación
Binarios para Windows, macOS y Linux en las «Releases» de GitHub (descarga manual; el de Windows podría bloquearlo el Control inteligente: usar el de Linux en WSL).

## Limitaciones
- Su reconocedor por defecto está pensado para inglés; para español usar el reconocedor fonético o derivar visemas de nuestra alineación (por verificar).

## En este equipo
No instalado. Alternativa local: mapear las vocales de la alineación wav2vec2 a formas de boca.
