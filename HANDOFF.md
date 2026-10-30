# Handoff — Scriptorium (30 de octubre de 2026)

Resumen para continuar en un chat nuevo. Guía técnica: `CLAUDE.md`. Plan original: `docs/PLAN.md`.

## Qué funciona hoy (verificado)

Pipeline completo de punta a punta sobre *El criterio*, de Jaime Balmes (cap. I, 1 348 palabras,
dominio público):

| Etapa | Resultado | Tiempo |
|---|---|---|
| Ingesta (MD/TXT/PDF/DOCX/PPTX/EPUB, OCR `spa`) | 10 párrafos con IDs `§1.1.1` … | segundos |
| Texto (LLM `gemma4:12b`, 17 llamadas) | resumen con zoom, glosario, citas, esquema, mapa, quiz, preguntas, 3 guiones | ~8 min (con caché: segundos) |
| Fidelidad | citas 6/6 y definiciones 4/4 verificadas por código; juez: 14 literal · 42 paráfrasis fiel · 3 inferencia · 3 añadido (señalados) | ~3 min |
| Audio (Kokoro, GPU) | audiolibro `.m4b` 8:21 con 7 capítulos, audio-guía 3:18, podcast 3:24, repaso, píldoras | ~2 min |
| Interactivos | lector con audio sincronizado y glosario, textos, quiz, mapa (markmap), mazo de Anki (14 tarjetas) | segundos |
| Video | explicador 1080p60 de 2:16 con 13 escenas, subtítulos, anclas a la fuente | render 5.5 min (CPU, 8 hilos) |
| Biblioteca | `D:\Scriptorium\03_biblioteca\index.html` | — |

También se probó con un **PDF real** (Wikisource, cap. II, obra `balmes-el-criterio`), reingerido
con la ingesta corregida: 9 párrafos, 861 palabras, título «Capítulo II», secciones I–IV = `§1.1`–`§1.4`.
Todo regenerado en 13.9 min: citas 6/6, definiciones 3/4 (el código rechazó una con «éstes» por
«éstos»), juez 12 literal · 51 paráfrasis · 1 inferencia · 1 añadido; video 2:08 (render 5.2 min).
Quiz revisado a mano: 6/6 correctas, aunque en la 3 un distractor («divagan por las tenebrosas
regiones de adentro») también es cierto de los ensimismados.
`scriptorium generar <slug>` con el slug exacto procesa solo esa obra (antes `balmes-el-criterio`
arrastraba también a `jaime-balmes-el-criterio`).

## Decisiones tomadas (y por qué)

- **WSL2 en vez de desactivar el Control inteligente de aplicaciones**: el usuario no quiso
  desactivarlo y, con la actualización KB5127648 (oct. 2026), podría no poder reactivarlo.
- **Ollama se queda en Windows** (ya tenía modelos y funciona con SAC); Linux lo usa por localhost.
- **Kokoro** como voz por defecto (`em_alex` narrador, `ef_dora` anfitriona), acento `es-419`.
- **Juez sin modo de razonamiento**: con «thinking» no acertó más y tarda el doble.
- **Datos en el disco USB D:**; código, entornos y modelos en el SSD.
- El usuario autorizó trabajar de forma autónoma («resuelve tú, no me vuelvas a preguntar»).

## Limitaciones conocidas (sé honesto con el usuario sobre esto)

1. **El juez local no detecta errores lógicos sutiles.** Ejemplo real: la pregunta 6 del quiz
   asocia «añadir lo que no hay» con el «vidrio de ilusión» (en Balmes eso es el error; añadir es el
   «espejo mal azogado»). Las 4 configuraciones probadas (Gemma/Qwen × con/sin razonamiento) la
   aceptaron. Detecta bien información añadida, no confusiones de relación.
2. Al juzgar el quiz por lotes, el juez **descartó 2 preguntas correctas** (ruido); probadas de forma
   aislada salen fieles. Posible mejora: lotes más chicos para el quiz.
3. **Ingesta del PDF** (corregida, falta probar con un libro real): no se pierde texto. Ahora
   pymupdf4llm omite encabezados y pies de página (`header=False, footer=False`), se quitan
   etiquetas HTML, la navegación de Wikisource («< Obra», «… >») y su pie «Obtenido de «URL»», y un
   título tipo subpágina («El criterio/02») se sustituye por la «Parte» del nombre de archivo
   («Capitulo II» → «Capítulo II»). Los títulos corridos y números de página de un libro escaneado
   o maquetado no se han probado todavía.
4. La sincronía palabra-voz en el video es **estimada por longitud de palabra** (no hay alineación
   real); la cita sí se ilumina en la ventana correcta de la narración.
5. Las capturas con Chromium headless no funcionaron; para revisar HTML usar el navegador integrado
   con `herramientas_wsl/servidor.sh` (ese servidor no admite saltos dentro del audio).

## Pendiente (en orden sugerido)

1. ~~`scriptorium generar balmes`~~ hecho. Primero falló porque la sesión cortada dejó un `.npy`
   vacío en la caché de voz; ahora las cachés de voz y de LLM se escriben de forma atómica y un
   archivo truncado se regenera solo.
2. ~~Arreglar la ingesta de PDF~~ hecho (punto 3 de arriba). Falta probarla con un PDF real del
   usuario (libro maquetado con títulos corridos y números de página).
3. `scriptorium voces` (cata de voces) y que el usuario elija voz. Opcional: Chatterbox
   Multilingual / Qwen3-TTS (más naturales, más lentos).
4. `scriptorium comparar balmes` (Gemma 4 12B vs Qwen3 14B) para elegir modelo.
5. Primer commit de git (el repo está iniciado, sin commits; no se hizo sin permiso).
6. Del plan, aún no hecho: transcripción de clases (faster-whisper), video vertical 9:16, grafo
   de conceptos entre obras, línea del tiempo, chat con la biblioteca (Open WebUI), bóveda de
   Obsidian, acceso desde el celular por Wi-Fi, programar `scriptorium noche` en el Programador
   de tareas, unir capítulos de un mismo libro en una sola obra.
7. Limpieza: `~/scriptorium.antiguo` en Linux (copia vieja con su venv, ~6 GB) se puede borrar;
   ffmpeg de Windows (winget `Gyan.FFmpeg`) quedó instalado pero bloqueado por SAC.

## Hardware (para recomendaciones)

- RAM: 1×16 GB DDR4-3200 (ADATA AX4U320016G16A) corriendo a 2667 MHz, **un solo canal**.
  XMP en BIOS Biostar B450MHP: `Supr` al arrancar → **Tweaker → Memory Clock Mode → XMP1** →
  Save & Exit. Si no arranca: jumper **JCMOS1** en 2-3 por 5 s. Mejor mejora: un segundo
  módulo igual (doble canal, 32 GB). El usuario lo tiene «en veremos».
- La B450MHP **no tiene ranura M.2** (4×SATA). Disco del sistema: SSD SATA Kingston A400 480 GB
  (~120 GB libres). Datos: HDD USB 1 TB (D:).
- Windows 11 Pro 25H2 (build 26200.9711), monitor en la gráfica integrada (VRAM libre para IA).
