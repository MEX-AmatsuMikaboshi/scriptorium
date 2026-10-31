# Imágenes y fotos animadas (Ken Burns y 2.5D)

```json
{
  "id": "imagenes-ken-burns",
  "nombre": "Imágenes y fotos animadas (Ken Burns y 2.5D)",
  "tipo": "tecnica",
  "capacidades": ["imagenes", "camara"],
  "herramientas": ["remotion", "ffmpeg", "kit-scriptorium"],
  "resumen": "Dar vida a pinturas, fotos y grabados con acercamientos lentos hacia el detalle y paralaje por capas."
}
```

## Ken Burns
```tsx
const p = interpolate(f, [0, dur], [0, 1], {easing: Easing.inOut(Easing.quad)});
<Img src={staticFile(src)} style={{transform: `scale(${1 + 0.1 * p}) translate(${-foco.x * 4 * p}%, ${-foco.y * 4 * p}%)`}} />
```
- Escala 1 → 1.08–1.15 en 4–8 s, moviéndose hacia el detalle que menciona la voz.
- No ampliar más allá de la resolución original (se pixela): partir de una imagen ≥ 1.5× el cuadro.

## 2.5D
Recortar la figura del fondo (capas PNG) y mover las capas con paralaje distinto. Rellenar el hueco detrás de la figura.

## Reglas
- La imagen es contenido: título, autor, fecha y fuente en pantalla.
- Marcar con un círculo o subrayado a mano el detalle del que se habla ([trazos-svg](trazos-svg.md)).
- Licencias: ver [lottie-y-recursos](lottie-y-recursos.md).
