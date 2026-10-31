# Motion (antes Framer Motion)

```json
{
  "id": "motion",
  "nombre": "Motion (antes Framer Motion)",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["interfaz-ui", "easing-timing", "tipografia-cinetica"],
  "resumen": "Animación para React y JavaScript: transiciones de interfaz, resortes, gestos, layout animado y scroll.",
  "lenguajes": ["TypeScript", "React", "JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://motion.dev",
  "repo": "motiondivision/motion",
  "paquetes": {"npm": ["motion"]},
  "llms_txt": "https://motion.dev/llms.txt",
  "licencia": "MIT",
  "relacionados": ["gsap", "animejs"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`<motion.div animate={{...}}>` en React o `animate()` en JS puro, con resortes físicos y animación de layout.

## Úsalo para
- Interfaces web animadas (la página de la biblioteca, el lector).

## No lo uses para
- Video en Remotion: depende del tiempo real. Usar `spring()`/`interpolate()` de Remotion.

## Instalación
```bash
npm i motion
```

## Limitaciones
- Pensada para interacción en vivo, no para render cuadro por cuadro.

## En este equipo
No instalado.
