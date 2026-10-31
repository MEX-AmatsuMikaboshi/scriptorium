# Instrucciones para agentes: biblioteca de conocimiento audiovisual

Esta carpeta es una biblioteca de conocimiento para **hacer video y animación con código**: qué técnica usar, con qué
herramienta, cómo, con qué licencia y qué ya está instalado en este equipo. La usan modelos locales (Ollama) y
agentes como Claude Code, Codex, Gemini CLI u OpenCode. Idioma de trabajo: español.

## Regla principal
**Antes de diseñar o programar una animación o un video, consulta la biblioteca.** No inventes librerías, APIs ni
comandos: si algo no está aquí ni en la documentación que la biblioteca señala, dilo.

## Cómo consultarla
```bash
saber buscar "<lo que se quiere lograr, en lenguaje natural>"   # técnicas, herramientas, flujos, recetas, principios, docs
saber ver <id>              # documento completo (ficha, técnica, principio, flujo o receta: canvas2d/golpe)
saber ver <id> --breve      # solo lo esencial
saber contexto "<petición>" --tokens 3500    # paquete listo para pegar en el prompt de un modelo
saber capacidades           # qué se puede pedir
```
- `saber` es `python3 <esta carpeta>/herramientas/saber.py` (solo biblioteca estándar de Python 3.10+).
- En Windows: `saber …` (lanzador en `%LOCALAPPDATA%\Programs\scriptorium`) o
  `wsl -d Ubuntu-24.04 -u gaber -- /home/gaber/.local/bin/saber …`.
- Sin poder ejecutar nada: lee los archivos. `catalogo/recursos.json` tiene todas las fichas en un solo JSON.

## Pasos para una petición de animación
1. `saber buscar "<petición>"` → mira las capacidades detectadas y la técnica de arriba.
2. Si hay un **flujo** que coincide, síguelo (son recetas de punta a punta).
3. Lee la **técnica** (`saber ver <id>`): trae el cómo, números que funcionan y errores comunes.
4. Elige herramienta: primero `en-uso` o `instalado`, luego `prioridad: ahora`. Lee su ficha en breve (licencia,
   instalación, limitaciones).
5. Si hay **recetas** (Canvas 2D), úsalas como referencia de timing; traduce la idea al motor del proyecto.
6. Implementa con código **determinista**: cada cuadro depende solo del tiempo (sin `Math.random()`, sin estado entre
   cuadros, sin relojes de librerías).
7. Revisa con `saber ver lista-de-control` antes de renderizar.

## Reglas del equipo (no las rompas)
- Windows 11 con Control inteligente de aplicaciones activo: los binarios sin firma no corren en Windows; todo corre en
  Ubuntu (WSL2). Blender 5.2, Unity y VRoid Studio sí están instalados en Windows.
- GPU Quadro GP100 (16 GB, Pascal): nada que pida más de 16 GB de VRAM ni FlashAttention/FP8. RAM 16 GB (justa).
- En Scriptorium: el LLM del pipeline **nunca escribe código**, solo elige escenas del kit y textos por esquema JSON.
  Nunca `npm install` dentro de `video/` (usar `herramientas_wsl/npm_agregar.sh`).
- Herramientas locales y gratuitas antes que servicios de pago. Revisa la licencia en la ficha antes de copiar código
  (Remotion, GSAP, LYGIA, Live2D y los repositorios sin licencia tienen condiciones).
- No instales dependencias globales; entornos aislados por proyecto. No ejecutes scripts remotos sin leerlos.
- Pide autorización antes de instalaciones grandes o de cambiar configuraciones.

## Cómo agregar conocimiento
Sigue el flujo `agregar-conocimiento` (`saber ver agregar-conocimiento`): lo crudo va a `bandeja/`; cada recurso se
vuelve una ficha (`saber nuevo <url-de-github>` evita duplicados y trae datos reales); lo no comprobado se marca
`"confianza": "por-verificar"`. Después: `saber validar` y `saber probar`.

## Mapa
| Carpeta | Qué hay |
|---|---|
| `fichas/` | Una ficha por herramienta, librería, skill, MCP, aplicación o referencia (Markdown + bloque JSON) |
| `tecnicas/` | Cómo lograr algo (tipografía cinética, partículas, transiciones, 3D…) |
| `principios/` | Diseño de movimiento (timing, easing, composición…) y la lista de control |
| `flujos/` | Recetas de punta a punta (video de 30 s, escena nueva en el kit, modelo 3D en video…) |
| `recetas/canvas2d/` | 27 recetas de animación con código, motor base y prompt para modelos locales |
| `catalogo/` | `capacidades.json` (taxonomía y sinónimos), `estado.json` (mantenimiento), `recursos.json` (todo junto), `pruebas.json` |
| `bandeja/` | Información cruda por procesar |
| `adaptadores/` | Skill (Agent Skills) y servidor MCP |
| `herramientas/` | `saber.py` y `extraer_recetas.mjs` |
| `.cache/` | Índice y documentación descargada (no se sube a git; `saber actualizar` la rehace) |
