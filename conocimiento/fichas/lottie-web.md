# Lottie Web

```json
{
  "id": "lottie-web",
  "nombre": "Lottie Web",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["lottie", "iconos"],
  "resumen": "Reproduce en la web animaciones de After Effects exportadas como JSON (Bodymovin/Lottie); en Remotion se usa con @remotion/lottie.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://airbnb.io/lottie/",
  "repo": "airbnb/lottie-web",
  "paquetes": {"npm": ["lottie-web", "@remotion/lottie"]},
  "licencia": "MIT (el reproductor; cada animación tiene su propia licencia)",
  "relacionados": ["remotion"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Reproductor de archivos Lottie (JSON vectorial). `@remotion/lottie` lo sincroniza con el cuadro actual.

## Úsalo para
- Íconos animados o pequeñas ilustraciones hechas por otros (revisar licencia de cada archivo).

## No lo uses para
- Crear animaciones: Lottie es un formato de salida; hacerlas requiere After Effects u otra herramienta.

## Instalación
```bash
npm i @remotion/lottie lottie-web
```

## Limitaciones
- Último cambio 2025-09: mantenimiento lento.
- Muchas animaciones gratuitas de LottieFiles tienen licencia propia: verificar antes de usar.

## En este equipo
No instalado.
