# Lottie, íconos, fuentes e imágenes de terceros

```json
{
  "id": "lottie-y-recursos",
  "nombre": "Lottie, íconos, fuentes e imágenes de terceros",
  "tipo": "tecnica",
  "capacidades": ["lottie", "iconos", "imagenes"],
  "herramientas": ["lottie-web", "lucide", "remotion"],
  "resumen": "Usar animaciones, íconos, fuentes e imágenes hechas por otros sin romper licencias ni la sincronía."
}
```

## Lottie en Remotion
```tsx
import {Lottie} from '@remotion/lottie';
<Lottie animationData={datos} />   // avanza con el cuadro de Remotion
```
Cada archivo Lottie tiene su licencia (LottieFiles usa la suya): anotarla junto al archivo.

## Íconos
Lucide (ISC) ya está en el kit con un catálogo cerrado (`iconos.json`). Para agregar íconos: añadirlos al catálogo para que el director LLM pueda elegirlos.

## Fuentes
Solo fuentes con licencia que permita incrustarlas (SIL Open Font License): el kit usa EB Garamond e Inter vía `@fontsource`.

## Imágenes
- Preferir dominio público o CC0 (colecciones de museos con acceso abierto, Wikimedia Commons revisando cada archivo).
- Guardar fuente y licencia en un JSON junto a la imagen y mostrar el crédito si la licencia lo pide.
- Ver [imagenes-ken-burns](imagenes-ken-burns.md).
