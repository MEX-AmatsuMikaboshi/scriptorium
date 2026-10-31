# Scriptorium — guía para Claude

Fábrica local de contenido de humanidades: libros/apuntes → texto canónico con IDs → texto
derivado, interactivos, audio y video de motion graphics. **Principio rector: dar formato, no
reescribir.** Todo lo derivado se ancla a párrafos `§capítulo.sección.párrafo` y pasa por
verificación. El usuario habla español (México); responde en español.

Contexto completo y estado actual: `HANDOFF.md`. Plan original: `docs/PLAN.md`. Manual: `README.md`.

## Arquitectura (importante)

- **Windows 11** tiene el *Control inteligente de aplicaciones* (Smart App Control) **activo**: bloquea
  binarios sin firma (ffmpeg de Windows, DLL de numpy, binarios de Remotion…). No propongas
  desactivarlo (el usuario no quiere, y con KB5127648 podría no poder reactivarlo).
- Por eso **todo corre en Ubuntu 24.04 (WSL2)**, salvo **Ollama**, que corre en Windows
  (firmado) y se alcanza desde Linux en `127.0.0.1:11434` (red `mirrored` en `~/.wslconfig`).
- Código: esta carpeta (`C:\Users\gaber\Documents\Scriptorium`), enlazada en Linux como
  `~/scriptorium` → `/mnt/c/Users/gaber/Documents/Scriptorium`.
- Entornos pesados en el disco de Linux (no en esta carpeta):
  - Python: `~/.local/share/scriptorium/venv` (variable `UV_PROJECT_ENVIRONMENT`).
  - Node del kit de video: `~/.local/share/scriptorium/video/node_modules`, enlazado como
    `video/node_modules` (el enlace no se ve desde Windows; está en `.gitignore`).
- Datos y productos: `D:\Scriptorium` (disco USB) = `/mnt/d/Scriptorium`.
- Cachés: `~/.cache/scriptorium/{llm,tts,video}`. La caché del LLM se indexa por prompt: si
  cambias un prompt se regenera solo; para forzar, borra `~/.cache/scriptorium/llm`.

## Cómo ejecutar cosas

PowerShell 5.1 deforma las comillas al pasar comandos a `wsl`. **Escribe un script `.sh` y
ejecútalo**; nunca pases tuberías ni comillas anidadas en la línea de `wsl`. La herramienta Bash
de Claude Code (Git Bash) no arranca en esta máquina (sale con código 2 sin mensaje): usa PowerShell.

```powershell
& 'C:\Program Files\WSL\wsl.exe' -d Ubuntu-24.04 -u gaber -- bash /mnt/c/Users/gaber/Documents/Scriptorium/herramientas_wsl/generar.sh balmes --formatos video --forzar
```

- Comando del usuario: `scriptorium <ingerir|generar|noche|biblioteca|voces|comparar|estado>`
  (en Windows: `%LOCALAPPDATA%\Programs\scriptorium\scriptorium.cmd`; en Linux: `~/.local/bin/scriptorium`).
- Python: `cd ~/scriptorium && uv run python ...` (con `UV_PROJECT_ENVIRONMENT` exportada; ya está en `~/.bashrc`).
- Remotion: `cd ~/scriptorium/video && npx remotion still|render src/index.ts Explicador ...`
  (`npx remotion studio src/index.ts` para ver el kit en vivo).
- Root en Linux sin contraseña: `wsl -d Ubuntu-24.04 -u root -- bash script.sh` (para `apt`).
- `herramientas_wsl/`: scripts útiles (`generar.sh`, `cuadros.sh [slug] [cap]` extrae un
  cuadro a la mitad de cada escena del video para revisarlo, `stills.sh` renderiza cada escena del kit, `servidor.sh` sirve `D:\Scriptorium`
  en `localhost:8777` para revisar páginas en el navegador integrado, `medir_sincronia.sh` mide
  con alineación forzada el desfase voz-pantalla de un video).
- **Git**: el SAC bloquea el `libcurl` de Git para Windows (no hay `git push` por HTTPS desde Windows).
  Sube con `herramientas_wsl/git_push.sh` (git de Linux + el administrador de credenciales de Windows).
  Repo público: `MEX-AmatsuMikaboshi/scriptorium`; correo de commits: el noreply de esa cuenta (config local).
- **npm**: nunca `npm install` dentro de `video/` (borra el enlace `node_modules` e instala en C:).
  Usa `herramientas_wsl/npm_agregar.sh paquete@versión` (instala en Linux y copia los manifiestos).
- **Motores de voz** (cada uno en su venv, `~/.local/share/scriptorium/voces/<motor>`, torch 2.11+cu126):
  `voces_instalar.sh`, `cata_voces.sh` (genera muestras) y `cata_pagina.sh` (página a ciegas en
  `D:\Scriptorium\03_biblioteca\cata`). Triton/`torch.compile` no soporta Pascal: desactivarlo (`optimize=False`).
  `audio.Voz` los lanza como procesos trabajadores (`src/scriptorium/voz_trabajador.py`, JSON por
  stdin/stdout, audio por `.npy`); su registro queda en `~/.cache/scriptorium/voz_<motor>.log`.

## Hardware y versiones fijadas

- GPU **Quadro GP100** (Pascal, sm_60, 16 GB). Driver **582.78 (rama R580)**: no actualizar a 590+.
- **PyTorch 2.14.1 + cu126**, fijado en `pyproject.toml` con índice explícito: es la última
  combinación con soporte Pascal. Sin FlashAttention/FP8; usar fp32.
- CPU Ryzen 7 5700G (8 núcleos/16 hilos). **RAM 16 GB (justa)**: WSL limitado a 8 GB; Ollama ya
  se cayó una vez con `std::bad_alloc` → `llm.py` reintenta y cachea.
- Remotion 4.0.539, React 19, Node 26 (portable en `~/.local/node`), uv 0.13, Ollama 0.40.
- Modelos de Ollama: `gemma4:12b` (por defecto, ~25 tok/s efectivos), `qwen3:14b`.
- Voz (elegida por el usuario en la cata a ciegas): **narrador = VoxCPM2** (masculina, ~2.4 s de cómputo
  por segundo de audio, bf16 emulado) y **anfitriona = Qwen3-TTS 1.7B Base** (femenina, fp16). Son
  *voces fijadas* (`voces/voces.json` + `.wav`): una referencia sintética que el motor clona en cada
  segmento para que la voz no cambie. Kokoro-82M (~29× tiempo real) queda como respaldo (`em_alex`).
  - VoxCPM2 termina en `tanh`: con la voz fuerte aplana los picos (la «saturación» que el usuario
    notó). El trabajador la quita y `audio.nivelar` aplica ganancia lineal (-20 dBFS RMS, pico -1 dBFS).
  - No clones un texto igual al de la referencia (el modo continuación lo recorta): sale incompleto.
  - Cada trozo se escucha con el alineador; si no se oye > 8 % del texto se repite (3 tomas, la mejor).
  - VoxCPM2 a veces para un parche (160 ms) antes de acabar la última palabra: el trabajador lo deja
    seguir 2 parches tras pedir parar y lo para a los 4 (`_ParadaTardia`; sin tope, a veces sigue en
    silencio y empieza otro sonido). Una toma que aún acaba de golpe se repite.

## Código

- `src/scriptorium/`: `ingesta` (→ canónico con IDs), `llm` (Ollama con esquema JSON, reintentos,
  caché), `textos` (derivados + verificación), `verificacion` (citas literales por código + juez
  LLM), `publicar` (Markdown + manifiesto), `interactivo` (lector, textos, quiz, mapa, Anki),
  `audio` (voces fijadas o Kokoro, nivel, control + ffmpeg), `voz_trabajador` (corre en el venv de
  cada motor; no importa nada del proyecto), `video` (director LLM → voz → alineación → Remotion), `alineacion`
  (wav2vec2 CTC en español: tiempos reales de cada palabra y transcripción de control de la voz),
  `biblioteca`, `pipeline`, `cli`, `comparar`.
- `video/src/`: kit de escenas (`escenas.tsx`), elementos comunes (`comun.tsx`), movimiento
  (`movimiento.tsx`: transiciones, cámara viva, pictogramas Lucide que se dibujan), catálogo de
  pictogramas (`iconos.json`, compartido con Python), tema y tipos.
  El LLM **nunca escribe código**: solo elige escenas del kit, textos breves y un pictograma del catálogo (JSON).
- **Regla de sincronía**: lo que se ilumina palabra por palabra es exactamente lo que dice la voz, en el
  cuadro en que lo dice (alineación forzada). Una cita en pantalla se lee literal; el texto que la voz
  no dice tal cual aparece completo, sin iluminarse.
- Convención de nombres de entrada: `Autor - Título - Parte.pdf`.
