# Animación de interfaces

```json
{
  "id": "animacion-de-interfaces",
  "nombre": "Animación de interfaces",
  "tipo": "tecnica",
  "capacidades": ["interfaz-ui"],
  "herramientas": ["motion", "gsap", "snapcn", "remotion"],
  "resumen": "Microinteracciones y transiciones de páginas web (biblioteca, lector) y maquetas de pantallas dentro de videos."
}
```

## En páginas web (biblioteca, lector, interactivos)
- Duraciones cortas: 150–300 ms para estados, 300–500 ms para cambios de vista.
- `ease-out` al entrar, `ease-in` al salir; respetar `prefers-reduced-motion`.
- CSS basta casi siempre; Motion (React) o GSAP para secuencias más complejas.

## En videos
- Maquetas de pantalla con marcos de dispositivo (snapcn) y cursor animado que sigue arcos, no rectas.
- Los clics se marcan con un pulso breve; el contenido cambia después del clic, no al mismo tiempo.

## Reglas
- La animación explica un cambio de estado; si no explica nada, sobra.
