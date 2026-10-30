# Plan: fábrica local de contenido de humanidades — "Scriptorium"

> **Objetivo:** convertir libros, presentaciones y apuntes de filosofía, psicología y humanidades en formatos fáciles de consumir (video animado, audio, interactivos y texto), **100 % local**, sin APIs ni suscripciones, y **sin alterar la esencia del contenido**: dar formato, no reescribir.
>
> Fecha: 30 de octubre de 2026 · Máquina de trabajo: tu otra PC, con Ryzen 5600G + NVIDIA Quadro de 16 GB

---

## 0. Resumen en 30 segundos

- **Tú solo dejas archivos en una carpeta y eliges opciones** (voz, estilo, formatos). La fábrica la construyo yo, por fases.
- Todo corre en tu PC con GPU: un **LLM local** lee y estructura, un **TTS local** da voz, **Remotion** anima y renderiza el video, y un **sitio local** junta todo.
- **Video:** el estilo que quieres son *motion graphics hechos con código*: formas, texto, partículas y geometría, sin metraje ni personas. Para tu equipo es la mejor noticia posible, porque **no necesita GPU para generarse**: se programa y se renderiza a 60 fps. Yo construyo una sola vez una biblioteca visual de alta calidad, y el LLM local solo "dirige": elige escenas, textos y ritmo para cada capítulo. Las ilustraciones IA y los clips de video IA quedan como extras opcionales.
- **Fidelidad:** cada producto lleva una etiqueta de *nivel de intervención* (0 = literal … 3 = didáctico) y pasa por un verificador automático contra el texto original. Las citas se comprueban con código, carácter por carácter.
- **Costo:** solo la luz. Una noche de procesamiento consume ~2 kWh, ≈ $2–8 MXN según tu tarifa CFE.
- **Primer entregable real (semana 1):** un capítulo convertido en audiolibro, resumen, mapa mental y tarjetas Anki. El video completo llega entre la semana 2 y la 3. Antes de eso, un demo corto para confirmar el estilo.

---

## 1. Tu hardware: lo que importa

| Componente | Lo que dijiste | Lo que casi seguro es | Implicación |
|---|---|---|---|
| CPU | Ryzen 7 5600G | **Ryzen 5 5600G** (6 núcleos / 12 hilos); el Ryzen 7 equivalente es el 5700G | Suficiente; además es la que renderiza los videos. Su gráfica integrada sirve para conectar el monitor y dejar la Quadro 100 % libre para IA. |
| GPU | Quadro "GT100" de 16 GB | **Quadro GP100**: 16 GB HBM2, arquitectura Pascal, de 2016. No existe ninguna "GT100". | Funciona, con reglas especiales (abajo). |
| RAM | ? | — | Con 16 GB funciona cargando un modelo a la vez; con 32 GB vas más cómodo (opcional, no indispensable). |
| Disco | ? | — | Reserva ~150–200 GB, de preferencia en SSD (desde un disco duro, cargar un modelo tarda 4–9 min). |

**Verificación** (en la PC de la GPU, en PowerShell):

```powershell
nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv
```

Si aparece `Quadro GP100` con `6.0`, este plan aplica tal cual. Si aparece otra tarjeta (p. ej. RTX A4000 o RTX 5000), todo funciona igual pero más rápido, y se abren opciones extra (sección 9).

### Reglas de oro para una GP100 (Pascal)

1. **Driver:** quédate en la rama **R580** (NVIDIA RTX Enterprise 580.xx). Es la última que soporta Pascal; las ramas 590 en adelante ya no.
2. **PyTorch:** fija **torch 2.14 con CUDA 12.6 (`cu126`)** en *todos* los entornos. A partir de PyTorch 2.15 dejan de publicarse las builds cu126 y, con ellas, el soporte para Pascal; las builds cu128/cu130 tampoco la soportan. → No uses instaladores "portables" que traen la última versión de PyTorch sin revisarlos.
3. **Precisión:** en ComfyUI deja los cálculos en fp32, que es el modo por defecto. En una P100 (mismo chip), forzar fp16 resultó ~11 % más lento. Los modelos cuantizados (GGUF/int8) sí sirven para ahorrar VRAM.
4. **Lo que no tiene:** Tensor Cores, FlashAttention, SageAttention ni FP8 nativo. Cualquier herramienta que dependa de eso queda fuera.
5. **Un modelo a la vez:** 16 GB no alcanzan para tener cargados al mismo tiempo el LLM, el TTS y los modelos de imagen y video. El orquestador trabaja por etapas y descarga cada modelo al terminar.
6. **Ventaja:** la memoria HBM2 (732 GB/s) hace que los LLM locales generen texto rápido.

### Rendimiento medido en el mismo chip (Tesla P100 16 GB, ComfyUI)

| Tarea | Tiempo |
|---|---|
| Imagen 1024×1024 — FLUX.2 klein 4B, 4 pasos | ~25 s |
| Imagen — Z-Image Turbo 8 bits, 8 pasos | ~80 s |
| Video 5 s, 832×480 — Wan 2.1 1.3B destilado (4 pasos) | ~5 min |
| Video 2 s, 832×480 — Wan 2.2 5B (20 pasos) | ~8.7 min |
| Video 2 s, 1280×704 — Wan 2.2 5B (20 pasos) | ~24 min |

**Conclusión:** las ilustraciones son baratas y el video IA es caro. Con el estilo que elegiste (motion graphics hechos con código) esto casi deja de importar: la GPU se dedica a la voz y al texto, y el video se renderiza en la CPU.

---

## 2. Principio rector: fidelidad al texto

### Escalera de intervención (cada archivo producido lleva su etiqueta)

| Nivel | Nombre | Qué se permite | Ejemplos |
|---|---|---|---|
| **0** | Literal | Nada cambia: las mismas palabras en otro medio | Audiolibro, lector con audio sincronizado, video-lectura |
| **1** | Estructural | Las mismas palabras, extraídas o reorganizadas | Citas clave, glosario con las definiciones del autor, esquema, tarjetas de citas |
| **2** | Explicativo fiel | Paráfrasis, pero cada idea anclada a su párrafo de origen `[§3.2.14]` | Resúmenes, audio-guía, guion de video, podcast |
| **3** | Didáctico | Ejemplos, analogías o preguntas añadidas, **siempre marcadas** como añadido | Diálogo socrático, ejercicios, preguntas de reflexión |

### Mecanismos de control

- **Texto canónico con IDs:** al ingerir una obra, cada párrafo recibe un ID estable (capítulo.sección.párrafo). Todo lo derivado apunta a esos IDs, así que siempre puedes saltar al original.
- **Citas verificadas por código:** toda frase entre comillas debe existir literalmente en el original; si no existe, se rechaza. En este paso no interviene ninguna IA.
- **Juez de fidelidad (LLM local):** una segunda pasada clasifica cada oración del guion como *literal*, *paráfrasis fiel*, *inferencia*, *añadido* o *contradicción*. Lo marcado como "añadido" o "contradicción" se corrige o queda señalado.
- **Glosario congelado:** los términos técnicos del autor (*Dasein*, *voluntad de poder*, *inconsciente colectivo*, etc.) se conservan tal cual. Está prohibido sustituirlos por sinónimos.
- **Sin conocimiento externo** en los niveles 0 a 2. El contexto histórico solo entra en el nivel 3, etiquetado como "Nota de contexto".

---

## 3. Arquitectura general

```
 00_entrada/        PDF, PPTX, EPUB, DOCX, audios de clase
      │  ingesta (Docling / MarkItDown / OCR / Whisper)
      ▼
 01_canonico/<obra>/    texto.md + parrafos.jsonl (IDs) + meta.yaml
      │  LLM local (Ollama): análisis y guiones anclados a IDs + verificación
      ▼
 02_derivados/<obra>/
      ├─ texto/         resúmenes con zoom, glosario, citas, esquema
      ├─ interactivo/   mapa mental, grafo, Anki, quiz, línea del tiempo, lector
      ├─ audio/         audiolibro, audio-guía, podcast, píldoras, repaso
      └─ video/         guion → voz → lista de escenas (JSON) → render a 60 fps
      ▼
 03_biblioteca/     sitio local (en el navegador o en tu celular por el Wi-Fi de casa)
```

**Motor:** un programa en Python ("Scriptorium") que yo construyo, con comandos simples:

```powershell
scriptorium ingerir 00_entrada\Nietzsche_Genealogia.pdf
scriptorium generar genealogia --formatos audio,mapa,anki,video
scriptorium noche        # procesa la cola mientras duermes
scriptorium biblioteca   # publica el sitio local
```

Se comunica por HTTP local con Ollama (texto), el servidor de voz (TTS), Remotion (animación y render), ffmpeg (audio y video) y, solo si usas los extras opcionales, ComfyUI (imagen y video IA). Ejecuta las etapas en lotes —todo el LLM primero, luego la voz y al final el video— para que en la VRAM solo haya un modelo a la vez.

---

## 4. Stack de software (todo gratis, todo local)

| Función | Herramienta principal | Alternativa | Nota para la GP100 |
|---|---|---|---|
| Ingesta de PDF digital, PPTX y DOCX | Docling, MarkItDown | PyMuPDF4LLM, pandoc | CPU, sin problema |
| OCR (libros escaneados) | Tesseract (`spa`) / OCR de Docling | Surya | CPU o GPU |
| Transcripción de clases grabadas | faster-whisper large-v3-turbo | whisper.cpp | fp16/fp32 |
| LLM | Ollama | llama.cpp / LM Studio | ver la tabla de modelos abajo |
| Voz (TTS) | Kokoro (rápido) · Chatterbox Multilingual **es-MX/LatAm** · Qwen3-TTS 0.6B/1.7B | Piper (solo CPU) | fp32, sin FlashAttention |
| **Motion graphics (el núcleo del video)** y ensamble | Remotion (React) con SVG, Canvas y Three.js | Manim (diagramas), Motion Canvas | render en la CPU (Chromium); gratis para uso individual |
| Imágenes (opcional) | ComfyUI + FLUX.2 klein 4B | Z-Image Turbo, SDXL con LoRAs de estilo | cálculos en fp32, pesos int8/GGUF |
| Parallax 2.5D (opcional) | DepthFlow (con Depth Anything V2) | — | ligero |
| Video IA (opcional) | ComfyUI + Wan 2.1/2.2 (destilado a 4 pasos, imagen→video) | Wan2GP (hecho para GPUs modestas; por probar) | 480p, clips de 2–5 s |
| Fluidez a 60 fps de los clips IA (opcional) | RIFE (interpolación de cuadros) | FILM / GIMM-VFI | ligero |
| Música de fondo | Biblioteca libre (CC0) descargada una sola vez | ACE-Step 1.5 (opcional, por probar en Pascal) | — |
| Mapas mentales | Markmap | — | HTML sin conexión |
| Tarjetas de repaso | genanki → Anki (.apkg) | — | — |
| Chat con tu biblioteca | Open WebUI u Open Notebook + Ollama | AnythingLLM | — |
| Notas enlazadas | Bóveda de Obsidian generada | — | — |

### LLM sugeridos (se prueban 2 o 3 con un capítulo real en español)

| Modelo | Tamaño en 16 GB | Por qué |
|---|---|---|
| Gemma 4 26B-A4B (MoE) | ~14 GB (IQ4_XS) | Multilingüe (140+ idiomas) y rápido por ser MoE; queda justo de VRAM |
| Qwen3 14B | ~9 GB (Q4_K_M) | Deja espacio para contexto largo; sigue bien instrucciones y formato JSON |
| gpt-oss-20b | ~13 GB | Razonamiento sólido |

**Regla:** gana el que mejor respete el texto en la prueba de fidelidad, no el más "creativo". Como director de video, además, el que mejor elija escenas y produzca JSON válido.

---

## 5. Formatos que vas a recibir (por obra o capítulo)

### 5.1 Texto (la base de todo lo demás)

- **Resumen con zoom:** 1 línea → 1 párrafo → 1 página por capítulo (nivel 2).
- **Esquema argumental:** tesis → premisas → objeciones → conclusión (niveles 1–2).
- **Glosario** con la definición del propio autor y su párrafo de origen (nivel 1).
- **Citas clave verificadas** (nivel 1).
- **Ficha de la obra:** autor, época, contexto (solo el que el libro declara) y estructura.
- **Preguntas de reflexión** (nivel 3).

### 5.2 Audio

| Producto | Nivel | Duración | Para qué |
|---|---|---|---|
| Audiolibro literal (.m4b con capítulos) | 0 | completo | Escuchar el texto tal cual |
| Audio-guía por capítulo | 2 | 10–15 min | Entender antes o después de leer |
| Podcast a 2 voces (anfitrión curioso + especialista) | 2–3 | 15–25 min | Estilo NotebookLM, pero local |
| Píldoras por concepto | 2 | 2–4 min | Trayectos cortos |
| Repaso activo: pregunta → pausa → respuesta | 1–2 | 5–10 min | Memorizar |
| Diálogo socrático con las ideas del autor | 3 (marcado) | ~10 min | Pensar críticamente |

**Voces:** haremos una *cata de voces* (la misma página leída con Kokoro, con Chatterbox es-MX y con Qwen3-TTS) para que elijas. También puedes clonar tu propia voz o una que tengas derecho a usar.

### 5.3 Interactivos (sitio local "Biblioteca")

- **Lector enriquecido:** el texto original con audio sincronizado (se resalta lo que se está leyendo), glosario al pasar el cursor y enlaces a los resúmenes. Nivel 0.
- **Mapa mental** de cada capítulo y de la obra (Markmap): se expande con clics y cada nodo lleva al párrafo original.
- **Grafo de conceptos entre obras:** conceptos, autores y relaciones (*critica*, *retoma*, *se opone a*, *define*) a lo largo de toda tu biblioteca. Aquí aparecen las conexiones entre libros.
- **Línea del tiempo** de los autores, obras y eventos que se mencionan.
- **Quiz autocorregible** y preguntas abiertas.
- **Mapa de argumentos** navegable.
- **Mazo de Anki:** conceptos, citas en formato *cloze* y relaciones autor↔idea; repaso espaciado en el celular con AnkiDroid (gratis).
- **Chat con la biblioteca** (Open WebUI u Open Notebook): le preguntas al libro y responde citando el párrafo; incluye un modo de tutor socrático.
- **Bóveda de Obsidian:** una nota por concepto, enlazadas entre sí.

### 5.4 Video → sección 6

---

## 6. Video: motion graphics hechos con código

**Estilo confirmado:** el de las referencias que compartiste. Son animaciones hechas 100 % con código: formas, texto, partículas, geometría y diagramas que se dibujan solos, sin metraje, sin personas y sin imágenes generadas. La fluidez viene de animar a 60 fps con curvas de movimiento y física de resortes.

**Por qué es buena noticia para tu equipo:** estos videos no se "generan" con un modelo de video, se **programan y se renderizan**. No necesitan la GPU, no tienen límite de duración y siempre salen nítidos y consistentes.

**El reto, dicho con honestidad:** los ejemplos virales los escribe un modelo de frontera (Claude Opus 5.5) a la medida, video por video. Un LLM local de 14–26B no llega a ese nivel escribiendo código de animación desde cero: el resultado saldría torpe o con errores.

**La solución: kit visual + director local.**

- **El kit** lo construyo yo, una sola vez y con calidad de frontera: una biblioteca de escenas, efectos y transiciones en Remotion (React + SVG + Canvas + Three.js), probada y pulida.
- **El director** es el LLM local, y trabaja en cada capítulo: lee el guion fiel y decide qué escena usar, con qué texto, qué palabras resaltar y a qué ritmo. Solo produce un JSON y nunca escribe código, así que nada se rompe.
- **Variedad sin perder coherencia:** cada escena tiene parámetros (composición, color de acento, dirección del movimiento, semilla de partículas) para que los videos no se vean todos iguales.

### Catálogo inicial del kit (~25 piezas)

| Familia | Escenas |
|---|---|
| Tipografía cinética | `Cita` (el texto aparece al ritmo de la voz), `PalabraClave` (una palabra que crece y se transforma), `Lectura` (karaoke del texto original), `Pregunta` |
| Conceptos | `Concepto` (término + definición del autor), `Contraste` (A frente a B, p. ej. apolíneo / dionisíaco), `Lista`, `Analogia` |
| Argumentos | `Argumento` (premisas que se ensamblan en una conclusión), `CadenaCausal`, `Dialectica` (tesis ↔ antítesis → síntesis), `Objecion` |
| Estructuras | `MapaDeConceptos` (nodos que se conectan), `Arbol`, `LineaDelTiempo`, `Ciclo` |
| Geometría y partículas | `Campo` (partículas que se organizan en una idea), `Morfosis` (una forma que se transforma en otra), `Orbitas`, `Capas` (niveles, p. ej. consciente / inconsciente) |
| Autores e influencias | `TarjetaAutor`, `Escuela` (constelación de autores e influencias) |
| Personaje guía (opcional) | una figura abstracta de diseño propio que señala, reacciona y "explica" |
| Ritmo | `TransicionCapitulo`, `Respiro` (pausa visual), `Cierre` |

### Ensamble

```
guion por escena (texto anclado a IDs)
   ├─► voz (TTS) ──► duración exacta + tiempos por palabra (Whisper)
   ├─► LLM "director" ──► elige escenas del kit + parámetros (JSON)
   ├─► (opcional) ilustración → parallax (capa B)
   └─► (opcional) clip IA → RIFE (capa C)
          ▼
   Remotion renderiza todo a 60 fps + subtítulos + música suave → MP4 1080p
```

Cada escena dura exactamente lo que dura su voz, y las palabras en pantalla aparecen al mismo tiempo que se pronuncian, así que nada se desfasa.

### Tipos de video

| Tipo | Nivel | Duración | Con qué se hace |
|---|---|---|---|
| Video-lectura (texto original + voz + fondo animado) | 0 | capítulo completo | kit (`Lectura`) |
| Explicador de capítulo | 2 | 6–12 min | kit (+ capas B/C opcionales) |
| Concepto en 90 s (vertical 9:16, para el celular) | 2 | 1–2 min | kit |
| Mapa de la obra (recorrido animado por el grafo) | 1–2 | 3–5 min | kit |

### Capa B (opcional) — Ilustración animada en 2.5D

> Las capas B y C no forman parte del estilo que elegiste. Quedan disponibles por si algún tema las pide, por ejemplo una escena muy narrativa.

1. Para cada escena, el LLM redacta el prompt de imagen dentro de un **estilo fijo**: "tinta y grabado", "papel recortado", "acuarela minimalista", "siluetas geométricas", etc.
2. ComfyUI genera la ilustración con FLUX.2 klein (~25 s por imagen).
3. DepthFlow le da movimiento de cámara con profundidad (acercamiento, órbita, *dolly*) a 60 fps.
4. Consistencia visual: estilo fijo + semilla fija + (opcional) un LoRA de estilo.

### Capa C (opcional) — Clips de video IA

1. Una imagen de la capa B pasa por **imagen→video** con Wan: 480p, 2–5 s, destilado a 4 pasos (~5 min por clip).
2. RIFE la interpola a 48/60 fps y luego se escala.
3. Se usa como mucho para un clip cada 30–60 s, en momentos clave. Estos clips se generan de noche.

### Lo que no recomiendo en tu GPU

- Generar el video completo con IA: sale inconsistente y cuesta ~1 h por minuto de video.
- HunyuanVideo 1.5 o LTX-2.x: están pensados para GPUs modernas (bf16/FP8). Vale la pena probarlos solo si algún día cambias de tarjeta.
- Avatares realistas (no es lo que buscas).

---

## 7. Tiempos y costo estimados (por capítulo de ~30 páginas)

> Son estimaciones: la Fase 0 las confirma con mediciones reales en tu máquina.

| Etapa | Tiempo aproximado |
|---|---|
| Ingesta + IDs | 1–3 min |
| Derivados de texto + guiones + verificación (LLM) | 20–40 min |
| Audiolibro literal (~1 h de audio) | de ~10 min (Kokoro) a ~1 h (Chatterbox / Qwen3-TTS) |
| Audio-guía y podcast | 15–30 min |
| Interactivos | menos de 5 min |
| Video explicador de 8 min, solo motion graphics (render a 60 fps en la CPU) | ~20–60 min, sin ocupar la GPU |
| + 6 clips de video IA (opcional) | +30–40 min |

- **Por noche (8 h):** unos 3–5 capítulos completos con video, o 8–10 capítulos sin video. Mientras la CPU renderiza un video, la GPU puede ir generando la voz del siguiente capítulo.
- **Costo:** la PC completa consume ~250 W, así que 8 h ≈ 2 kWh por noche ≈ **$2–8 MXN** según tu escalón de tarifa CFE (más si estás en tarifa DAC). Cero APIs, cero suscripciones.

---

## 8. Hoja de ruta

### Antes de todo — Demo de estilo (se puede hacer ya, desde esta laptop)

- Un video corto (30–60 s) sobre un concepto, hecho con las primeras piezas del kit, para confirmar que es el estilo que buscas antes de instalar nada.
- No necesita GPU: se ve en el navegador.

### Fase 0 — Preparar la máquina (una tarde)

1. Correr `nvidia-smi` para confirmar GPU, VRAM y driver; revisar RAM y espacio en disco.
2. Conectar el monitor a la salida de video de la tarjeta madre (gráficos del 5600G), para que la VRAM quede libre para IA. Puede requerir activar la gráfica integrada en el BIOS.
3. Instalar el driver NVIDIA RTX Enterprise **R580** y no actualizar a 590 o posteriores.
4. Instalar Git, uv (Python 3.11), Node.js LTS, ffmpeg, Ollama y Anki.
5. Benchmark: 1 minuto de TTS, 1 respuesta del LLM y 1 render de prueba de Remotion, para tener tiempos reales.
6. (Solo si vas a usar los extras opcionales) ComfyUI con su propio entorno: **torch 2.14 + cu126**.

**Entregable:** un reporte de qué corre y cuánto tarda.

### Fase 1 — Texto e interactivos (semana 1)

- Ingesta y texto canónico con IDs.
- Resumen con zoom, glosario, citas verificadas y esquema.
- Mapa mental, mazo de Anki y lector (todavía sin audio).
- Prueba de fidelidad con 2–3 LLM → tú eliges uno.

**Entregable:** un capítulo de prueba completo en texto e interactivos.

### Fase 2 — Audio (semanas 1–2)

- Cata de voces → tú eliges.
- Audiolibro literal, audio-guía, podcast a 2 voces, píldoras y repaso.
- Lector con audio sincronizado.

### Fase 3 — Video con motion graphics (semanas 2–3)

- Kit visual: ~25 escenas, efectos y transiciones en Remotion, con 3 propuestas de estilo para que elijas.
- "Director" local: el LLM convierte el guion en una lista de escenas (JSON) sincronizada con la voz.
- **Primer explicador de 5–8 min** de un capítulo.

### Fase 4 — Modo nocturno y extras (semanas 3–4)

- Cola nocturna: dejas archivos en `00_entrada` y en la mañana está todo listo.
- (Opcional) Ilustraciones IA con parallax y clips de video IA, si algún tema los pide.

### Fase 5 — Biblioteca (semana 4 en adelante)

- Sitio local con todas tus obras, accesible desde el celular por el Wi-Fi de casa.
- Grafo entre obras, línea del tiempo global y chat con la biblioteca.

---

## 9. Formas de hacerlo (elige el ritmo)

| Ruta | Qué es | A favor | En contra |
|---|---|---|---|
| **1. Apps listas** | Instalar apps con interfaz gráfica (Pinokio, Open Notebook / Open WebUI, interfaces de TTS) y usarlas a mano | Empiezas hoy mismo, sin código | Manual y repetitivo; la fidelidad es difícil de controlar; no hay apps listas que hagan este estilo de video |
| **2. Fábrica automatizada** (Scriptorium) | El pipeline que construyo: entra un archivo y salen todos los formatos | Escala a toda tu biblioteca, controla la fidelidad, resultados consistentes | 3–4 semanas para tenerla completa |
| **3. Híbrida** ✅ recomendada | Usas apps listas para elegir voz mientras construimos la fábrica por fases | Resultados desde la semana 1 | — |

> Si algún día cambias de tarjeta (no es necesario), una RTX de 16–24 GB (Ampere o más nueva) haría la voz, el texto y los extras opcionales 3–5× más rápido.

---

## 10. Cómo trabajamos

- El pipeline corre **100 % en tu PC**. Yo (Claude) te ayudo a construirlo, pero no formo parte del proceso cuando está corriendo: ningún contenido sale de tu máquina.
- **La calidad visual se pone una vez, en el kit.** El modelo local solo dirige, así que la producción diaria sigue siendo local e ilimitada.
- **Piezas especiales (opcional):** si algún capítulo merece un video único hecho a la medida, como los de tus referencias, puedes pedírmelo aquí. Ten en cuenta que eso ya no es local: usa tu plan de Claude, no tu PC.
- **Lo ideal:** abrir Claude Code (la app de escritorio) en la PC de la GPU, dentro de una carpeta de proyecto (p. ej. `C:\Scriptorium`), para instalar, probar y ajustar directamente ahí. La laptop desde la que escribes ahora (i5, sin NVIDIA) no sirve para el procesamiento, pero sí para el demo de estilo.
- **Alternativa:** construyo el código aquí y tú lo copias a la otra PC.

---

## 11. Lo que necesito de ti para arrancar

1. La salida de `nvidia-smi`, la RAM y el espacio libre en disco de la PC de la GPU (y si tiene Windows 10 u 11).
2. ✅ Referencias de estilo: ya las compartiste. Opcional: dime cuál de ellas se acerca más a lo que quieres (más abstracta, más diagramas o más tipografía).
3. Un material de prueba (un capítulo o una presentación) y el formato del resto: ¿PDF digital, PDF escaneado, PPTX?
4. ¿Todo está en español? Si hay textos en otro idioma: ¿quieres el audio en el idioma original, traducido o ambos? (Traducir cuenta como nivel 2).
5. Preferencia de voz: femenina o masculina, acento mexicano, ¿clonar la tuya?
6. Qué formatos quieres primero.

---

## 12. Nota sobre derechos

Para uso personal de material que ya tienes, no hay problema. Si algún día quieres **publicar** videos derivados, revisa los derechos: las obras clásicas (Platón, Kant, Nietzsche…) son de dominio público, pero sus **traducciones recientes** pueden no serlo.

---

## Fuentes consultadas

- PyTorch — aviso de fin de las builds CUDA 12.6 y del soporte a Pascal: https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432
- R580, último driver con soporte para Pascal: https://www.phoronix.com/news/NVIDIA-580-Linux-Driver-Last-HW · https://hothardware.com/news/nvidia-ends-pascal-maxwell-driver-support
- Benchmarks de ComfyUI en Tesla P100 (mismo chip que la GP100): https://github.com/4claps/tesla-p100-comfyui-imagegen
- Modelos de video abiertos en 2026: https://www.thundercompute.com/blog/best-open-source-ai-video-generation-models · https://blog.ossium.in/what-s-the-best-open-source-ai-video-model-you-can-actually-run-8gb-24gb-vram
- TTS local: https://bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models · https://build.nvidia.com/resembleai/chatterbox-multilingual-tts/modelcard · https://github.com/groxaxo/Qwen3-TTS-Openai-Fastapi
- Open Notebook (alternativa local a NotebookLM): https://www.greptile.com/grepository/open-notebook
- LLM para 16 GB / Gemma 4: https://atomic.chat/blog/guides/best-local-llm-16gb · https://inference.readthedocs.io/en/latest/models/builtin/llm/gemma-4.html
- DepthFlow: https://github.com/BrokenSource/DepthFlow
- ACE-Step 1.5: https://huggingface.co/TTS-AGI/ACE-Step-1.5-Backup/blob/main/code/README.md
- Remotion, Motion Canvas y Manim para video generado: https://www.remotion.dev/docs/ai/generate · https://beginnersinai.org/remotion-vs-motion-canvas-vs-manim/

### Referencias de estilo (las que compartiste; no las verifiqué)

- Ejemplos y prompts de motion graphics con Canvas, SVG, Three.js y Remotion: https://aiidelist.com/blog/opus-5-5-motion-design
- Galería de prompts de motion graphics: https://carat.im/prompt-gallery/claude-opus-5-5
- Ejemplos en X: corto sobre la historia de la IA hecho 100 % en código (https://x.com/kimmonismus/status/2102844654169575547), demo reel de motion graphics (https://x.com/leonabboud/status/2103576084499358051), motion graphics abstracto (https://x.com/dirtman/status/2103686605517287620)
