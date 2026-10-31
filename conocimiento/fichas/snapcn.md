# snapcn

```json
{
  "id": "snapcn",
  "nombre": "snapcn",
  "tipo": "libreria",
  "areas": ["motion-graphics", "video-explicativo"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["tipografia-cinetica", "subtitulos-karaoke", "interfaz-ui", "composicion-video"],
  "resumen": "Registro estilo shadcn de componentes Remotion para videos de producto: revelado de texto, marcos de dispositivo, terminal, logo y escenas completas.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "web": "https://snapcn.dev",
  "repo": "shadcn-labs/snapcn",
  "licencia": "MIT",
  "agentes": "Componentes que se copian al proyecto con el CLI de shadcn: el agente lee y modifica el código fuente directamente.",
  "relacionados": ["remotion", "remotion-bits"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Componentes de Remotion que se instalan como código fuente en tu repositorio (modelo shadcn: el código es tuyo). Está en el directorio de registros de shadcn, así que no requiere configuración.

## Úsalo para
- Titulares, subtítulos y marcos de dispositivo de calidad para copiar y adaptar.

## No lo uses para
- Si el proyecto no es Remotion 4 con React.

## Instalación
```bash
npx shadcn@latest add @snapcn/text-reveal
```

## Ventajas
- El código queda en tu repo: sin dependencia en tiempo de ejecución.
- MIT.

## Limitaciones
- Pensado para demos de producto (SaaS).

## En este equipo
No instalado. En `video/` usar con cuidado: el CLI de shadcn puede querer instalar dependencias con npm (ver regla de `npm_agregar.sh`).
