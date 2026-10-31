# Diagramas, esquemas y mapas conceptuales

```json
{
  "id": "diagramas-y-mapas",
  "nombre": "Diagramas, esquemas y mapas conceptuales",
  "tipo": "tecnica",
  "capacidades": ["diagramas", "video-explicativo"],
  "herramientas": ["kit-scriptorium", "mermaid", "d3", "roughjs", "markmap", "motion-canvas"],
  "resumen": "Construir un esquema en el orden en que se explica: cada nodo aparece cuando la voz lo nombra y cada flecha se dibuja de origen a destino."
}
```

## Idea
Un diagrama explicativo no aparece completo: se construye al ritmo de la narración. Es la escena que más le falta al kit (esquema argumental, línea del tiempo, mapa de conceptos).

## Cómo se hace
- **Estructura** la describe el LLM como datos (nodos, aristas, etiquetas; Mermaid es un buen formato intermedio porque es fácil de validar). **Nunca** coordenadas.
- **Disposición** la calcula el código una sola vez: `d3-hierarchy` (árboles), un layout por capas (flujos) o `d3-scale` de tiempo (línea del tiempo).
- **Aparición**: nodo con `spring` cuando la alineación dice que la voz lo menciona (`aparece` del contrato `Escena`); arista con `evolvePath` desde el borde del nodo origen.
- **Foco**: la cámara se acerca al nodo activo; los demás bajan de opacidad.
- **Estilo**: limpio (SVG) o a mano (rough.js con semilla fija).

## Reglas
- Máximo 5–7 nodos visibles a la vez; si hay más, dividir en escenas.
- Las flechas significan algo (causa, oposición, parte de): usar 2–3 tipos con estilos distintos.
- Las etiquetas se leen horizontales.
- Flujo para agregarlo al kit: [escena-nueva-en-el-kit](../flujos/escena-nueva-en-el-kit.md).
