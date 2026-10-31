# Remotion Bits

```json
{
  "id": "remotion-bits",
  "nombre": "Remotion Bits",
  "tipo": "libreria",
  "areas": ["motion-graphics", "video-explicativo"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["tipografia-cinetica", "transiciones", "datos-graficas", "escena-3d", "control-por-agente"],
  "resumen": "Componentes animados listos para Remotion (gráficas, transiciones, revelado de texto, 3D) con CLI de búsqueda y servidor MCP propio.",
  "lenguajes": ["TypeScript", "React"],
  "exporta_video": "si",
  "web": "https://remotion-bits.dev",
  "repo": "av/remotion-bits",
  "paquetes": {"npm": ["remotion-bits"]},
  "licencia": "El repositorio no declara licencia en GitHub (consultado 2026-10-31): verifica el paquete npm antes de copiar código.",
  "agentes": "CLI `npx remotion-bits find|fetch --json` y servidor MCP `npx remotion-bits mcp` (stdio).",
  "relacionados": ["remotion", "snapcn"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Colección de «bits» (componentes y utilidades) para Remotion. Se pueden instalar como paquete o traer uno por uno con su CLI, que busca por objetivo visual y etiquetas.

## Úsalo para
- Buscar un efecto ya resuelto antes de programarlo: `npx remotion-bits find "text reveal"`.
- Gráficas animadas y revelados de texto para escenas nuevas del kit.

## Instalación
```bash
npx remotion-bits find 3d cards        # buscar
npx remotion-bits fetch bit-fade-in --json   # traer uno
npm install remotion-bits             # como dependencia
```

## Ventajas
- Búsqueda por intención y MCP: cómodo para agentes.
- Componentes pequeños que se pueden leer y adaptar.

## Limitaciones
- Licencia por confirmar.
- Estética propia: hay que adaptarla al tema del kit.

## En este equipo
No instalado. Con `npx` corre en WSL sin tocar `video/node_modules`.
