# Kit de escenas de Scriptorium

```json
{
  "id": "kit-scriptorium",
  "nombre": "Kit de escenas de Scriptorium",
  "tipo": "plantilla",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "en-uso",
  "capacidades": ["video-explicativo", "tipografia-cinetica", "subtitulos-karaoke", "sincronia-audio", "transiciones", "camara", "iconos", "composicion-video"],
  "resumen": "El kit propio en Remotion: 10 tipos de escena (Portada, Cita, Concepto, Lista, Contraste, Argumento, PalabraClave, Pregunta, Respiro, Cierre) con karaoke alineado a la voz.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "licencia": "Código propio (repo público sin licencia declarada todavía).",
  "agentes": "El director LLM solo elige escenas, textos y un pictograma por JSON; nunca escribe código. Un agente de desarrollo sí puede agregar escenas nuevas al kit.",
  "relacionados": ["remotion", "lucide", "wav2vec2-alineacion", "voxcpm", "qwen3-tts"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Escenas de motion graphics en `video/src/`: `escenas.tsx` (los 10 tipos), `comun.tsx` (Palabras, Fondo, Subtítulos, Insignia), `movimiento.tsx` (transiciones, cámara viva con ruido, pictogramas Lucide que se dibujan), `tema.ts` (colores, EB Garamond + Inter) y `tipos.ts` (contrato `Escena`). La composición `Explicador` recibe `{titulo, autor, capitulo, nivel, escenas[]}`.

## Úsalo para
- Videos explicativos de obras: el pipeline (`src/scriptorium/video.py`) genera el JSON y renderiza.
- Punto de partida para escenas nuevas (línea del tiempo, mapa de conceptos, imagen con Ken Burns): ver el flujo [escena-nueva-en-el-kit](../flujos/escena-nueva-en-el-kit.md).

## No lo uses para
- Cambiar la regla de sincronía: lo que se ilumina es exactamente lo que dice la voz, en el cuadro en que lo dice.

## Instalación
Ya instalado. Ver en vivo: `cd ~/scriptorium/video && npx remotion studio src/index.ts`. Cuadros de revisión: `herramientas_wsl/stills.sh` y `herramientas_wsl/cuadros.sh`.

## Ventajas
- Probado de punta a punta con voces fijadas y alineación forzada.
- Catálogo cerrado de pictogramas (`iconos.json`, 73) que comparten Python y TypeScript.

## Limitaciones
- Solo 10 tipos de escena; faltan gráficas, diagramas, imágenes y 3D.
- Estética única (fondo oscuro, serif); un estilo nuevo es trabajo de diseño, no de prompt.

## En este equipo
En uso. 1080p60, render en CPU (~5 min por 2 min de video).
