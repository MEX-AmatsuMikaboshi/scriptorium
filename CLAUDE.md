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
ejecútalo**; nunca pases tuberías ni comillas anidadas en la línea de `wsl`:

```powershell
& 'C:\Program Files\WSL\wsl.exe' -d Ubuntu-24.04 -u gaber -- bash /mnt/c/Users/gaber/Documents/Scriptorium/herramientas_wsl/generar.sh balmes --formatos video --forzar
```

- Comando del usuario: `scriptorium <ingerir|generar|noche|biblioteca|voces|comparar|estado>`
  (en Windows: `%LOCALAPPDATA%\Programs\scriptorium\scriptorium.cmd`; en Linux: `~/.local/bin/scriptorium`).
- Python: `cd ~/scriptorium && uv run python ...` (con `UV_PROJECT_ENVIRONMENT` exportada; ya está en `~/.bashrc`).
- Remotion: `cd ~/scriptorium/video && npx remotion still|render src/index.ts Explicador ...`
  (`npx remotion studio src/index.ts` para ver el kit en vivo).
- Root en Linux sin contraseña: `wsl -d Ubuntu-24.04 -u root -- bash script.sh` (para `apt`).
- `herramientas_wsl/`: scripts útiles (`generar.sh`, `cuadros.sh` extrae cuadros del video
  para revisarlos, `stills.sh` renderiza cada escena del kit, `servidor.sh` sirve `D:\Scriptorium`
  en `localhost:8777` para revisar páginas en el navegador integrado).

## Hardware y versiones fijadas

- GPU **Quadro GP100** (Pascal, sm_60, 16 GB). Driver **582.78 (rama R580)**: no actualizar a 590+.
- **PyTorch 2.14.1 + cu126**, fijado en `pyproject.toml` con índice explícito: es la última
  combinación con soporte Pascal. Sin FlashAttention/FP8; usar fp32.
- CPU Ryzen 7 5700G (8 núcleos/16 hilos). **RAM 16 GB (justa)**: WSL limitado a 8 GB; Ollama ya
  se cayó una vez con `std::bad_alloc` → `llm.py` reintenta y cachea.
- Remotion 4.0.539, React 19, Node 26 (portable en `~/.local/node`), uv 0.13, Ollama 0.40.
- Modelos de Ollama: `gemma4:12b` (por defecto, ~25 tok/s efectivos), `qwen3:14b`.
- Voz: Kokoro-82M en la GPU, español latinoamericano (`es-419`), ~29× tiempo real.

## Código

- `src/scriptorium/`: `ingesta` (→ canónico con IDs), `llm` (Ollama con esquema JSON, reintentos,
  caché), `textos` (derivados + verificación), `verificacion` (citas literales por código + juez
  LLM), `publicar` (Markdown + manifiesto), `interactivo` (lector, textos, quiz, mapa, Anki),
  `audio` (Kokoro + ffmpeg), `video` (director LLM → voz → Remotion), `biblioteca`, `pipeline`,
  `cli`, `comparar`.
- `video/src/`: kit de escenas (`escenas.tsx`), elementos comunes (`comun.tsx`), tema y tipos.
  El LLM **nunca escribe código**: solo elige escenas del kit y textos breves (JSON).
- Convención de nombres de entrada: `Autor - Título - Parte.pdf`.
