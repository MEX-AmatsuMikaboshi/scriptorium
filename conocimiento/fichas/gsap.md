# GSAP

```json
{
  "id": "gsap",
  "nombre": "GSAP",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["tipografia-cinetica", "morphing", "trazo-svg", "easing-timing", "interfaz-ui"],
  "resumen": "Librería de animación JavaScript con línea de tiempo y plugins (SplitText, MorphSVG, DrawSVG, MotionPath), hoy gratuita incluso para uso comercial.",
  "lenguajes": ["JavaScript"],
  "exporta_video": "indirecto",
  "web": "https://gsap.com",
  "repo": "greensock/GSAP",
  "paquetes": {"npm": ["gsap"]},
  "llms_txt": "https://gsap.com/llms.txt",
  "licencia": "Standard «no charge» License: uso comercial y todos los plugins sin costo; prohibido usarla en constructores visuales sin código que compitan con Webflow. No es software libre.",
  "agentes": "Publica llms.txt; API muy conocida por los modelos.",
  "relacionados": ["animejs", "motion", "flubber", "opentype-js"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Tweens y `gsap.timeline()` con easings ricos; plugins para partir texto en letras/palabras (SplitText), transformar formas SVG (MorphSVG), dibujar trazos (DrawSVG) y seguir trayectorias (MotionPath).

## Úsalo para
- Tipografía cinética letra por letra y morphing de SVG de alta calidad.
- Animación de interfaces web.

## No lo uses para
- Dentro de Remotion sin control: GSAP corre con su propio reloj. Si se usa, pausar la timeline y llamar `tl.seek(frame / fps)` en cada cuadro.

## Instalación
```bash
npm i gsap   # los plugins vienen incluidos: import {SplitText} from 'gsap/SplitText'
```

## Ventajas
- Los mejores plugins de texto y morphing.
- Documentación y llms.txt.

## Limitaciones
- Licencia propietaria con restricción (no es OSS).
- Su reloj interno choca con el render determinista si no se controla con seek().

## En este equipo
No instalado. Para el kit, considerar primero @remotion/paths y opentype.js (sin restricciones).
