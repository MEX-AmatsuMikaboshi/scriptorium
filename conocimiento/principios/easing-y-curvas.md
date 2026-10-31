# Easing y curvas de movimiento

```json
{
  "id": "easing-y-curvas",
  "nombre": "Easing y curvas de movimiento",
  "tipo": "principio",
  "resumen": "Nada en el mundo se mueve a velocidad constante: entradas con ease-out, salidas con ease-in, ida y vuelta con ease-in-out, rebotes con resortes.",
  "capacidades": ["easing-timing"]
}
```

## Qué curva usar
| Situación | Curva | En Remotion |
|---|---|---|
| Algo entra y se asienta | ease-out (cúbica) o resorte | `Easing.out(Easing.cubic)`, `spring({damping: 14})` |
| Algo sale o cae | ease-in | `Easing.in(Easing.cubic)` |
| Va de A a B en pantalla | ease-in-out | `Easing.inOut(Easing.cubic)` |
| Aparición con rebote | back-out (rebasa y regresa) | `Easing.out(Easing.back(1.7))` |
| Cosas ligeras, colgantes | resorte amortiguado | `spring({damping: 8, mass: 0.5})` |

## Reglas
- Nunca interpolación lineal sobre el tiempo para movimientos (sí para cosas mecánicas: un reloj, una barra de progreso).
- `spring()` de Remotion depende de `fps`: siempre pásale `useVideoConfig().fps`.
- `extrapolateLeft/Right: 'clamp'` en casi todo `interpolate`, para que no se pase de largo.
- Curvas de la Biblioteca de Movimiento con números: `backOut` s=1.9, resorte `e^(−6t)·sin(18t)`.
