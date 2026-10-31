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

## Video: más movimiento (30 oct., tarde)

Pedido del usuario: «más movimiento, más animaciones». Hecho sin que el LLM escriba código:
transiciones `@remotion/transitions` (deslizar/barrido; sin fundidos entre escenas con texto porque
dos textos encimados se leen sucios), cámara viva (acercamiento + deriva con `@remotion/noise`),
luces de color por escena en el fondo, pictogramas Lucide que se dibujan trazo a trazo (el director
elige uno de 73 de `video/src/iconos.json`, restringido por esquema JSON), premisas que giran en 3D,
comillas y signo de pregunta que se mueven. Ideas para seguir: más tipos de escena (línea del
tiempo, mapa de conceptos), Lottie, imágenes de dominio público con efecto Ken Burns.

## Biblioteca de conocimiento audiovisual (31 oct.)

El usuario quiere juntar desde ya todo lo necesario para hacer video con código. El orden de prioridades es:
videos explicativos ahora, modelos 2D/3D dentro de los videos después, caricaturas y anime al final. El trabajo lo
harán sobre todo modelos locales, con mínima intervención de IAs grandes.

- Se creó `conocimiento/`: 72 fichas verificadas (GitHub, npm, PyPI), 18 técnicas, 12 principios, 6 flujos, 27 recetas
  Canvas 2D y 35 capacidades con sinónimos.
- La consulta va por la CLI `saber`, que solo usa la biblioteca estándar: FTS5, capacidades y recomendación por
  técnica. También hay una skill y un servidor MCP.
- Las 23 consultas de prueba pasan.
- `biblioteca-movimiento.html` (estaba suelta en la raíz) se movió a `conocimiento/recetas/canvas2d/`.
- En el equipo hay Blender 5.2.2, Unity 6000.6 y 2022.3, y VRoid Studio 2.14. VRoid es probablemente el «otro
  modelador» que el usuario no recordaba.
- Pendiente: completar los metadatos de 6 fichas cuando se renueve el límite de la API de GitHub (comando en
  `conocimiento/README.md`). Registrar la skill y el MCP en los agentes que use el usuario. Primeras escenas nuevas del
  kit sugeridas por la biblioteca: línea del tiempo y mapa de conceptos (técnica `diagramas-y-mapas`).

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
4. ~~Sincronía estimada~~ resuelto: alineación forzada real (`alineacion.py`, wav2vec2 español,
   confianza ~0.99 por palabra). Antes los subtítulos iban 192 ms desfasados en promedio (máx. 757) y
   el texto en pantalla no era lo que decía la voz (citas parafraseadas; definiciones iluminadas a
   ritmo fijo). Ahora: karaoke solo de lo que se dice y cuando se dice, citas leídas literal, listas/
   premisas/contrastes aparecen al mencionarse, subtítulos por frases. La misma pasada transcribe la
   voz y avisa si se come palabras (Kokoro no lo hacía: el problema era el diseño del kit).
5. Las capturas con Chromium headless no funcionaron; para revisar HTML usar el navegador integrado
   con `herramientas_wsl/servidor.sh` (ese servidor no admite saltos dentro del audio).

## Pendiente (en orden sugerido)

1. ~~`scriptorium generar balmes`~~ hecho. Primero falló porque la sesión cortada dejó un `.npy`
   vacío en la caché de voz; ahora las cachés de voz y de LLM se escriben de forma atómica y un
   archivo truncado se regenera solo.
2. ~~Arreglar la ingesta de PDF~~ hecho (punto 3 de arriba). Falta probarla con un PDF real del
   usuario (libro maquetado con títulos corridos y números de página).
3. **Voz (lo que más le importa al usuario: Kokoro le suena robótica).** Cata a ciegas en
   `D:\Scriptorium\03_biblioteca\cata\index.html` (5 motores × masculina/femenina; los MP3 se le
   mandaron por el chat porque estaba por control remoto). **Eligió**: H = Qwen3-TTS femenina («más la
   parte después de la pausa», la lectura: «más nítido») y G = VoxCPM2 masculina, pero «algo saturada,
   duele un poco en los oídos». Las demás (Kokoro, Chatterbox, OmniVoice) no le gustaron.
   - La saturación era real: el decodificador de VoxCPM2 termina en `tanh` y la voz sale ~3× por
     encima del rango (pico crudo 2.8–3.2), así que tanh aplanaba cada pico (a -13 LUFS, 7 dB más
     fuerte que las demás). Arreglo: el trabajador sustituye la tanh por identidad y se nivela con
     ganancia lineal. La toma original se restauró con `arctanh` (es la referencia del narrador).
   - Integrado: voces fijadas en `voces/voces.json` (+ `narrador.wav`, `anfitriona.wav`), trabajadores
     por motor (`voz_trabajador.py`), control con el alineador y reintento con otra semilla, nivel común.
   - En la prueba, clonar el mismo texto de la referencia salía recortado (31–33 % sin oírse): es el
     modo continuación de VoxCPM2, no pasa con textos distintos. Qwen3 clonado: 0 % sin oírse.
   - Velocidad VoxCPM2 en la GP100 (s de cómputo por s de audio): bf16 ~2.5, fp16 ~1.9 (sin NaN en
     la prueba, pero no se ha escuchado), fp32 ~6. Se queda bf16, la precisión nativa. RAM: al cargar
     pasa de 5 GB (se libera con `malloc_trim`); por eso hay un solo motor cargado a la vez y
     `Voz.preparar` agrupa por voz todo lo que se va a decir (el podcast alterna voces).
   - Cap. I regenerado con las dos voces (65 min de punta a punta; el video, a -21.9 LUFS, se le mandó
     en 720p). Dos defectos que salieron al revisarlo, ya arreglados:
     - VoxCPM2 genera por parches de 160 ms y a veces para uno antes de acabar la última palabra
       («su profe-»; 3 de 123 trozos). El trabajador lo deja seguir 2 parches tras pedir parar
       (`_ParadaTardia`): si ya había acabado sale silencio, que se recorta, así que lo ya generado
       sigue valiendo. Además `audio._termina_de_golpe` marca una toma que acaba con la voz a pleno
       y se repite con otra semilla.
     - `para_voz` leía «V. A todos…» como «Nonecinco» (grupo opcional en `None`) y no convertía
       «Capítulo I» a media frase («Repaso. Capítulo I…» se leía «i»).
   - 30 oct., noche: cap. II (`balmes-el-criterio`) regenerándose con las dos voces. En su registro
     salió un falso positivo del control: el reconocedor oye «por qué» como «porque» y eso contaba
     como dos palabras perdidas (3 tomas gastadas). `palabras_perdidas` ya no cuenta un cambio que
     solo mueve espacios. Pulido del kit: renglones equilibrados (`text-wrap: balance`), el subtítulo
     se oculta mientras el mismo texto se ilumina en grande (citas, conceptos), y una lista sin
     titular ya no toma de titular un fragmento cortado de la narración.
   - Cap. II listo (72 min de punta a punta; video 2:12, render 5.3 min). Video: las 13 escenas con
     todas las palabras alineadas (confianza 0.95–1.00, ≤ 8 % sin oírse). Un aviso real: en las
     píldoras, la definición literal empieza a media frase («es siempre ligero, superficial…») y
     VoxCPM2 arranca flojo: el reconocedor oye «en simpre» (confianza 0.50 en «es») en las 3 tomas.
     Sin escucharlo no se sabe si se nota; posible arreglo: que la píldora diga término y definición
     en una sola frase para el narrador, o más semillas para trozos que empiezan en minúscula.
     Detalle del director: en pantalla «llegar a él», la voz dice «llegar a ella» (la verdad).
   - Al revisar el cap. II, `_ParadaTardia` sin tope dejó 2 de 106 trozos con ~1 s de silencio y un
     chasquido al final (suelto, VoxCPM2 a veces ya no vuelve a pedir parar). Ahora: 2 parches
     obligatorios y como máximo 4 tras la primera petición. Probado en las tomas de «su profesión»
     (completas, conf. 1.00; la que ya estaba bien sale idéntica). Se borraron esos 2 trozos de la
     caché y se rehízo el cap. II.
   - La entrada de Balmes, cap. I, §1.4.1, dice «relativas a la practicada su profesión» y «en todas
     las profesiones ea cada cual»: parecen erratas del texto fuente («a la práctica de su», «es cada
     cual»). No se tocan (dar formato, no reescribir); preguntarle al usuario.
4. `scriptorium comparar balmes` (Gemma 4 12B vs Qwen3 14B) para elegir modelo.
5. ~~Primer commit~~ hecho y subido a `github.com/MEX-AmatsuMikaboshi/scriptorium` (público, sin
   licencia todavía: preguntar al usuario si quiere MIT u otra).
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
