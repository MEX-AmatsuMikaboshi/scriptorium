# Revideo

```json
{
  "id": "revideo",
  "nombre": "Revideo",
  "tipo": "motor",
  "areas": ["video-explicativo", "motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["composicion-video", "video-explicativo", "tipografia-cinetica"],
  "resumen": "Derivado de Motion Canvas pensado para renderizar sin interfaz: escenas en TypeScript y `renderVideo()` desde código o CLI.",
  "lenguajes": ["TypeScript"],
  "exporta_video": "si",
  "web": "https://midrender.com/revideo",
  "repo": "midrender/revideo",
  "paquetes": {"npm": ["@revideo/core"]},
  "docs": ["https://docs.re.video"],
  "licencia": "MIT",
  "agentes": "API de render por código: fácil de llamar desde un pipeline.",
  "relacionados": ["motion-canvas", "remotion"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Motor de render para «videos en código»: se describe la escena en TypeScript (formas, texto, medios, animación) y Revideo produce el archivo. Es el motor detrás de Midrender. El repositorio se movió de redotvideo/revideo a midrender/revideo.

## Úsalo para
- Si se quiere el estilo de Motion Canvas pero renderizando en lote desde un script.

## Instalación
```bash
npm init @revideo@latest
```

## Limitaciones
- Comunidad pequeña; depende de la empresa que lo mantiene.
- Duplica lo que ya hace Remotion en este equipo.

## En este equipo
No instalado.
