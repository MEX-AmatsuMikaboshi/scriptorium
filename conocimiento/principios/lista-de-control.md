# Lista de control: de funcional a profesional

```json
{
  "id": "lista-de-control",
  "nombre": "Lista de control: de funcional a profesional",
  "tipo": "principio",
  "resumen": "Preguntas para revisar cualquier animación antes de darla por buena; resume todos los principios."
}
```

## Antes de renderizar
1. ¿Qué debe entender el espectador en cada escena? ¿Una idea por escena?
2. ¿Cada elemento tiene un motivo para moverse?
3. ¿El foco de cada momento es obvio (tamaño, contraste, movimiento)?

## Revisando cuadros (stills al inicio, mitad y final de cada escena, y cada 0.1 s alrededor de cada golpe)
4. ¿Ningún movimiento es lineal salvo los mecánicos? ¿Entradas con ease-out y salidas con ease-in?
5. ¿Hay anticipación en las acciones grandes y asentamiento al llegar?
6. ¿Los elementos de un grupo entran escalonados y no en coro?
7. ¿El texto se puede leer completo antes de irse? ¿Contraste suficiente? ¿Márgenes respetados?
8. ¿Lo que se ilumina coincide con lo que dice la voz, en el cuadro en que lo dice?
9. ¿Cada costura tiene transición y ninguna transición funde dos textos?
10. ¿Colores, fuentes y curvas salen del tema, no de números sueltos?
11. ¿Nada tiembla sin querer (semillas por elemento) y todo es determinista (sin `Math.random`)?
12. ¿Hay respiro al final de cada idea y del video?

## Fallas típicas de la animación generada por IA
- Todo a la misma velocidad, eventos encimados, sin pausas.
- Momentos que terminan antes de entenderse.
- Caras o estados que cambian de golpe.
- Elementos en espejo perfecto (brazos, bailarines, columnas).
- Estética neón/glow/degradado cian-violeta, «glassmorphism».
- Objetos que flotan cerca de la mano en vez de tocarla.
