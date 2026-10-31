# Biblioteca de conocimiento audiovisual

Todo lo que hace falta saber para **hacer video y animación con código**, guardado en un solo lugar y en un formato
que puedan consultar tanto los modelos locales (Ollama) como agentes grandes (Claude Code, Codex, Gemini CLI). Así no
hay que volver a investigar las mismas herramientas en cada tarea.

## Para qué es, por etapas

| Etapa | Qué | Prioridad en las fichas |
|---|---|---|
| 1. Ahora | Videos explicativos y motion graphics hechos con programación (el kit de Scriptorium en Remotion) | `ahora` |
| 2. Complemento | Meter modelos y escenas 2D/3D (Blender, VRoid, Three.js) dentro de esos videos | `complemento` |
| 3. Futuro | Caricaturas y anime: personajes que hablan, actúan y se mueven | `futuro` |

Las tres etapas comparten la misma biblioteca: una técnica como «cámara» o «sincronía con la voz» sirve para todas.

## Qué hay dentro (31 de octubre de 2026)

- **72 fichas** de herramientas, librerías, skills, MCP, aplicaciones y referencias. Sus metadatos (licencia,
  versión, último cambio, si está archivada o renombrada) salen de GitHub, npm y PyPI, y cada una dice qué tan
  verificada está y si ya está instalada en este equipo.
- **18 técnicas**: cómo lograr algo concreto, por ejemplo tipografía cinética, partículas, 3D en video, diagramas o
  sincronía con la voz.
- **12 principios** de diseño de movimiento y una **lista de control** para pasar de «funciona» a «se ve profesional».
- **6 flujos** de punta a punta: video de 30 s, escena nueva en el kit, modelo 3D en video, clip de Manim, personaje
  que habla y cómo agregar conocimiento.
- **27 recetas** de animación con código, más el motor base y el prompt para modelos locales (de la Biblioteca de
  Movimiento).
- Una **taxonomía de 35 capacidades** con sinónimos en español e inglés, para entender peticiones como «animar letras»
  aunque no se mencione ninguna librería.
- La **documentación oficial descargada** (README y llms.txt) de cada herramienta, también buscable. Está en `.cache/`
  y no se sube a git.

## Uso diario

En PowerShell o en Ubuntu:
```powershell
saber buscar "quiero que las letras entren una por una"
saber ver tipografia-cinetica            # una técnica, ficha, principio, flujo o receta (canvas2d/golpe)
saber ver remotion --breve
saber contexto "video explicativo de 30 s con una gráfica" --tokens 3000
saber capacidades
```
`saber` también funciona desde cualquier otro proyecto: el lanzador de Windows está en
`%LOCALAPPDATA%\Programs\scriptorium\saber.cmd` y el de Linux en `~/.local/bin/saber`.

## Agregar información (lo que vayas juntando)

1. Pega lo crudo (conversaciones, enlaces, notas) en `bandeja/AAAA-MM-DD-tema.md`.
2. Pide a un agente, local o grande, que **procese la bandeja**. El flujo `agregar-conocimiento` le dice cómo: no
   duplicar (`saber nuevo <url>` avisa si ya existe), no inventar (lo no comprobado se marca `por-verificar`), agregar
   sinónimos y pruebas, y luego `saber validar` y `saber probar`.
3. Las fichas también se pueden escribir a mano copiando `fichas/_plantilla.md`.

## Mantenimiento (bajo demanda; nada corre solo)

| Comando | Qué hace |
|---|---|
| `saber actualizar [--solo a,b]` | Versiones, licencias, estrellas, último cambio, archivados y renombrados (GitHub, npm, PyPI) → `catalogo/estado.json`. Además descarga README y llms.txt a la caché. Sin token, GitHub permite 60 consultas por hora; las respuestas sin cambios no gastan. Con `GITHUB_TOKEN` son 5000. |
| `saber enlaces` | Revisa que respondan todos los enlaces de fichas y documentos. |
| `saber validar` | Revisa formato, valores permitidos, ids y repositorios duplicados, y referencias y enlaces internos rotos. Después regenera `catalogo/recursos.json`. |
| `saber probar` | Corre las consultas de `catalogo/pruebas.json` y dice si encuentran lo esperado. |
| `saber bandeja` | Lista las notas pendientes. |

El historial de cambios queda en git; los cambios grandes se anotan también en `HISTORIAL.md`.

## Conectarla a otros proyectos y agentes

Ver [adaptadores/README.md](adaptadores/README.md). En resumen hay cuatro vías:

1. Una línea en el `AGENTS.md`, `CLAUDE.md` o `GEMINI.md` del proyecto.
2. La skill `saber-audiovisual`, que sirve para Claude Code y Codex.
3. El servidor MCP, sin dependencias.
4. Para modelos locales sin herramientas, `saber contexto` pegado en el prompt, o `import saber` desde Python.

## Decisiones de diseño

- **Archivos de texto como fuente de verdad.** Son Markdown con un bloque JSON de metadatos, versionados en git: se
  leen sin herramientas, un modelo local los puede escribir y no hay base de datos que se pierda.
- **Búsqueda sin servidores.** SQLite FTS5 (incluido en Python) con raíces en español e inglés, más la detección de
  capacidades por sinónimos, más un grafo ligero: la técnica que mejor responde recomienda sus herramientas en orden
  de preferencia y luego pesan lo instalado y lo prioritario. El índice se rehace solo cuando cambia algún archivo.
- **Sin base vectorial por ahora.** Las 23 consultas de prueba, en español e inglés y sin nombres de librerías,
  encuentran lo esperado. Si alguna falla y los sinónimos no lo resuelven, el siguiente paso es LanceDB con
  embeddings de Ollama (ver la ficha `lancedb`).
- **Documentación por referencia.** No se copian repositorios: se guarda la ficha y la caché baja el README o la
  llms.txt cuando hace falta.
- **Pensada para modelos chicos.** Resúmenes de una línea, `--breve`, `contexto` con presupuesto de tokens y
  catálogos cerrados.

## Lo que falta o no está verificado

- 6 fichas que salieron de awesome-code-video (hyperframes, video-shotcraft, lemo-opuscar, map-motion, pretext,
  awesome-video-as-code) no tienen todavía metadatos de GitHub, porque se agotó el límite de la API el 31 de
  octubre. Sus README ya están en la caché: de ahí salen las licencias de las cuatro primeras; pretext y
  awesome-video-as-code siguen sin licencia confirmada. Se completan con
  `saber actualizar --solo hyperframes,video-shotcraft,lemo-opuscar,map-motion,pretext,awesome-video-as-code`.
- Las fichas indican qué tan verificadas están: 57 verificadas, 14 parciales y 1 por verificar. Las parciales tienen
  metadatos reales, pero algún detalle (una licencia, un comando) no se comprobó.
- `saber enlaces` revisó 137 enlaces y salió un solo aviso: vroid.com responde 403 a los robots, aunque el sitio existe.
- La skill y el MCP no se han registrado todavía en ningún cliente. El protocolo del MCP sí se probó a mano.
- Ninguna herramienta nueva se instaló: las fichas dicen cómo, y conviene pedir autorización antes de instalar.
