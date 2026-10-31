# Anticipación, seguimiento y acción superpuesta

```json
{
  "id": "anticipacion-y-seguimiento",
  "nombre": "Anticipación, seguimiento y acción superpuesta",
  "tipo": "principio",
  "resumen": "Antes de una acción grande, un pequeño movimiento contrario; después, las partes sueltas siguen y se asientan; nada empieza ni termina a la vez.",
  "capacidades": ["easing-timing", "personajes-2d"]
}
```

## En la práctica
- **Anticipación**: 0.10–0.12 s en sentido contrario antes de cualquier acción grande (agacharse antes de saltar; un texto que retrocede 5 px antes de salir disparado).
- **Seguimiento** (*follow-through*): lo que cuelga (pelo, cola, una etiqueta) sigue moviéndose y se asienta con un resorte.
- **Acción superpuesta**: ojos primero, cabeza +0.05 s, cuerpo +0.1 s, accesorios al final.
- **Aplastar y estirar** conservando volumen: ancho `1 + s`, alto `1 − s`.
- **Arcos**: lo que se lanza o gira sigue curvas, no rectas.

## En motion graphics (sin personajes)
Una tarjeta que entra rebasa su posición 2–4 % y regresa; los elementos de una lista no aterrizan todos a la vez; un ícono que «hace clic» se encoge 5 % antes de crecer.

Fuente clásica: los 12 principios de animación de Disney (Thomas y Johnston, *The Illusion of Life*, 1981).
