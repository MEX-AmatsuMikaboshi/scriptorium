# Scriptorium

Fábrica local de contenido de humanidades: convierte libros, presentaciones y
apuntes en audio, interactivos, texto y video, **sin alterar la esencia del
contenido** (da formato, no reescribe). Todo corre en esta PC: ningún contenido
sale de la máquina.

## Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Tus archivos y resultados | `D:\Scriptorium` |
| Archivos nuevos por procesar | `D:\Scriptorium\00_entrada` |
| Texto canónico con IDs (§capítulo.sección.párrafo) | `D:\Scriptorium\01_canonico\<obra>` |
| Productos (texto, audio, interactivos, video) | `D:\Scriptorium\02_derivados\<obra>` |
| **Biblioteca (ábrela en el navegador)** | `D:\Scriptorium\03_biblioteca\index.html` |
| Ajustes (modelo, voces, video) | `D:\Scriptorium\ajustes.json` |
| Código | Ubuntu (WSL): `/home/gaber/scriptorium` · desde Windows: `\\wsl.localhost\Ubuntu-24.04\home\gaber\scriptorium` |

## Uso diario (PowerShell de Windows)

```powershell
scriptorium noche                       # procesa todo lo nuevo de 00_entrada (todos los formatos)
scriptorium estado                      # obras, productos y pendientes
scriptorium biblioteca                  # reconstruye la página de la biblioteca
scriptorium ingerir "D:\libros\Kant.pdf" --titulo "Crítica de la razón pura" --autor "Immanuel Kant"
scriptorium generar kant --formatos texto,interactivo,audio,video
scriptorium generar kant --formatos audio --forzar   # rehace solo el audio
scriptorium voces                       # cata de voces para elegir narrador
scriptorium comparar balmes --modelos gemma4:12b,qwen3:14b   # prueba de fidelidad entre modelos
```

Formatos de entrada: PDF (digital o escaneado, con OCR en español), EPUB, DOCX,
PPTX, HTML, Markdown y TXT.

**Nombra los archivos así:** `Autor - Título - Parte.pdf` (por ejemplo
`Nietzsche - La genealogía de la moral - Tratado I.pdf`). De ahí salen el autor y el
título. En Markdown también puedes poner una cabecera:

```markdown
---
titulo: El criterio
autor: Jaime Balmes
fecha: 1845
---
# Capítulo I. ...
```

## Qué produce por obra

| Producto | Nivel |
|---|---|
| Lector con audio sincronizado y glosario al pasar el cursor | 0 literal |
| Audiolibro `.m4b` con capítulos (y `.mp3`) | 0 literal |
| Glosario con la definición del propio autor · citas clave · mazo de Anki | 1 estructural |
| Resumen con zoom (1 línea / 1 párrafo / 1 página) · esquema argumental · mapa mental · quiz | 2 explicativo fiel |
| Audio-guía · podcast a dos voces · repaso activo · píldoras de conceptos | 2 explicativo fiel |
| Video explicador de motion graphics (1080p, 60 fps, subtítulos, anclas a la fuente) | 2 explicativo fiel |
| Preguntas de reflexión | 3 didáctico (marcado) |
| Informe de fidelidad | — |

## Cómo se protege la fidelidad

- Cada párrafo tiene un ID estable; todo lo derivado apunta a sus párrafos de origen.
- Las citas y definiciones se comprueban **con código, carácter por carácter**; las que no existen en el original se descartan.
- Un juez local (LLM) clasifica cada oración parafraseada: literal, paráfrasis fiel, inferencia, añadido o contradicción. Lo marcado como añadido o contradicción aparece señalado con ⚠ en los productos y en `fidelidad.md`.
- En el video, una escena de «Cita» solo muestra texto que existe literalmente en la obra.

## Ajustes (`D:\Scriptorium\ajustes.json`)

- `modelo`: modelo de Ollama para texto y director de video (por defecto `gemma4:12b`).
- `voz_narrador`, `voz_anfitrion`: una voz fijada de `voces/voces.json` (`narrador` con VoxCPM2,
  `anfitriona` con Qwen3-TTS: las elegidas en la cata) o una voz de Kokoro (`em_alex`, `ef_dora`, `em_santa`).
- `velocidad_voz`: 1.0 normal, 0.9 más pausado (solo Kokoro).
- `video_hilos`: hilos de CPU para el render (8 por defecto; la PC tiene 16).
- `palabras_por_bloque`: tamaño de los trozos que lee el modelo en capítulos largos.

## Antes de dejarlo trabajando de noche

1. Ollama abierto (icono junto al reloj).
2. Disco `D:` conectado.
3. Cierra apps pesadas: la PC tiene 16 GB de RAM y Ollama los necesita.
4. Corre `scriptorium noche`.

## Arquitectura

- **Windows:** Ollama (LLM en la GPU). El Control inteligente de aplicaciones sigue activo.
- **Ubuntu en WSL2:** todo lo demás (Python con PyTorch 2.14 + CUDA 12.6 para la Quadro GP100,
  VoxCPM2 y Qwen3-TTS para la voz —cada uno en su propio entorno, como proceso aparte— con Kokoro
  de respaldo, Remotion + Chromium para el video, ffmpeg). El Control inteligente no
  aplica a los programas de Linux.
- Las etapas corren por lotes (LLM → voz → video) para que en la VRAM haya un solo modelo a la vez.
- Las respuestas del LLM y los audios se guardan en caché (`~/.cache/scriptorium`): si algo se
  interrumpe, al repetir no se rehace lo ya hecho.

## Problemas frecuentes

- **«El modelo … no está en Ollama»**: `ollama pull gemma4:12b` (o el que pongas en ajustes).
- **«Ollama falló …; reintento»**: falta RAM; cierra apps. Se recupera solo.
- **Contraseña de Linux**: tu usuario `gaber` no tiene contraseña. Para ponerle una:
  `wsl -u root passwd gaber`.
- **Kit de video**: para ver y ajustar las escenas en vivo, en Ubuntu:
  `cd ~/scriptorium/video && npx remotion studio src/index.ts`.
