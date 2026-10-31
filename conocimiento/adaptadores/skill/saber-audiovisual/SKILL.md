---
name: saber-audiovisual
description: Consulta la biblioteca local de conocimiento audiovisual antes de diseñar o programar una animación, un video explicativo, motion graphics, un efecto, una transición, una escena 3D o un personaje. Dice qué técnica, herramienta, receta de código y principios de diseño usar, qué ya está instalado en este equipo y qué licencias revisar.
---

# Biblioteca de conocimiento audiovisual

Antes de escribir código de animación o video, consulta la biblioteca. No inventes herramientas ni APIs que no
aparezcan en ella o en la documentación que señala.

## Cómo consultarla

En Linux/WSL (o macOS):
```bash
python3 /home/gaber/scriptorium/conocimiento/herramientas/saber.py buscar "<lo que se quiere lograr>"
python3 /home/gaber/scriptorium/conocimiento/herramientas/saber.py ver <id> [--breve]
python3 /home/gaber/scriptorium/conocimiento/herramientas/saber.py contexto "<petición>" --tokens 3500
```
Desde Windows (PowerShell), por WSL:
```powershell
& 'C:\Program Files\WSL\wsl.exe' -d Ubuntu-24.04 -u gaber -- /home/gaber/.local/bin/saber buscar "animar letras una por una"
# o, si está en el PATH de Windows: saber buscar "animar letras una por una"
```
Si la biblioteca está en otra ruta, usa `<ruta>/herramientas/saber.py`. Los archivos también se pueden leer
directamente: `fichas/`, `tecnicas/`, `principios/`, `flujos/`, `recetas/`.

## Pasos
1. `buscar` con la petición en lenguaje natural (no hace falta saber el nombre de la librería).
2. Lee la técnica principal (`ver <id-de-tecnica>`) y, si hay, el flujo.
3. Lee en breve las 2–3 herramientas sugeridas; prefiere las que dicen `en-uso` o `instalado`.
4. Implementa siguiendo las reglas de la técnica (determinismo: cada cuadro depende solo del tiempo).
5. Revisa con `ver lista-de-control` antes de renderizar.

## Reglas
- Si la biblioteca no cubre algo, dilo y propone agregarlo (flujo `agregar-conocimiento`); no lo inventes.
- Respeta las licencias anotadas en cada ficha (Remotion, GSAP, LYGIA y Live2D tienen condiciones).
- No instales dependencias globales ni ejecutes scripts remotos sin revisarlos.
