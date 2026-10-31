# tsParticles

```json
{
  "id": "tsparticles",
  "nombre": "tsParticles",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["particulas"],
  "resumen": "Partículas configurables por JSON: confeti, fuegos artificiales, nieve, enlaces entre puntos, fondos animados.",
  "lenguajes": ["TypeScript", "JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://particles.js.org",
  "repo": "tsparticles/tsparticles",
  "paquetes": {"npm": ["@tsparticles/engine"]},
  "licencia": "MIT",
  "relacionados": ["pixijs", "threejs"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Motor de partículas con presets y plugins, para páginas web.

## Úsalo para
- Fondos de partículas en páginas web.

## No lo uses para
- Video determinista: simula con física paso a paso y su propio reloj. Para video, partículas como función del tiempo (ver técnica de partículas).

## Instalación
```bash
npm i @tsparticles/engine
```

## Limitaciones
- No determinista: no apto para render cuadro por cuadro sin trabajo extra.

## En este equipo
No instalado.
