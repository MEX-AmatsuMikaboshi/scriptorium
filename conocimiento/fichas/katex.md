# KaTeX

```json
{
  "id": "katex",
  "nombre": "KaTeX",
  "tipo": "libreria",
  "areas": ["video-explicativo"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["matematicas"],
  "resumen": "Composición tipográfica de fórmulas LaTeX en HTML, rápida y sin servidor: ecuaciones nítidas dentro de escenas de Remotion.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://katex.org",
  "repo": "KaTeX/KaTeX",
  "paquetes": {"npm": ["katex"]},
  "licencia": "MIT",
  "relacionados": ["manim", "motion-canvas"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`katex.renderToString('a^2+b^2=c^2')` devuelve HTML con sus fuentes; se anima como cualquier elemento (aparición por partes con CSS).

## Úsalo para
- Fórmulas estáticas o que aparecen por partes en el kit sin instalar LaTeX.

## No lo uses para
- Transformar una fórmula en otra símbolo por símbolo (eso lo hace Manim).

## Instalación
```bash
npm i katex
```

## Limitaciones
- Subconjunto de LaTeX (casi todo lo matemático común).

## En este equipo
No instalado.
