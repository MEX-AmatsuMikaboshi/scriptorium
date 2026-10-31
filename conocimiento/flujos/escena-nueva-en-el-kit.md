# Agregar un tipo de escena al kit de Scriptorium

```json
{
  "id": "escena-nueva-en-el-kit",
  "nombre": "Agregar un tipo de escena al kit de Scriptorium",
  "tipo": "flujo",
  "prioridad": "ahora",
  "capacidades": ["video-explicativo", "composicion-video", "diagramas"],
  "herramientas": ["kit-scriptorium", "remotion"],
  "resumen": "Pasos para que un agente de desarrollo agregue una escena (línea del tiempo, mapa de conceptos, imagen) sin romper la regla de que el LLM del pipeline solo elige datos."
}
```

## Regla
El LLM del pipeline **nunca escribe código**: solo elige el tipo de escena y llena campos de texto validados por esquema JSON. Una escena nueva es código que escribe un agente de desarrollo (o una persona), una sola vez.

## Pasos
1. **Diseño en papel**: qué explica, qué campos necesita (p. ej., línea del tiempo: `items` = «año — hecho»), cómo se sincroniza con la voz (cada ítem aparece al nombrarse) y cómo se ve en 1920×1080. Consulta la técnica correspondiente (`saber buscar "<idea>"`).
2. **Tipos** (`video/src/tipos.ts`): añadir el nombre a `TipoEscena`; reutilizar campos existentes de `Escena` (`titular`, `cuerpo`, `items`, `izquierda`, `derecha`, `resaltar`, `aparece`) antes de crear nuevos.
3. **Componente** (`video/src/escenas.tsx`): una función más dentro de `EscenaKit`, usando `Palabras`, `Pictograma`, `Camara` y los colores de `tema.ts`. Animar solo con `useCurrentFrame()`, `interpolate`, `spring`, `random(semilla)`.
4. **Director** (`src/scriptorium/video.py`): añadir el tipo a `TIPOS`, describirlo en el prompt de sistema con límites de palabras, y en la normalización (límites, valores por defecto). Si el texto en pantalla no es lo que dice la voz, que aparezca completo sin iluminarse.
5. **Probar**: `herramientas_wsl/stills.sh` (cada escena del kit) y una obra real con `scriptorium generar <slug> --formatos video --forzar`; revisar con `cuadros.sh`.
6. **Documentar**: actualizar la ficha `kit-scriptorium` en esta biblioteca.

## Dependencias
Agregar paquetes npm solo con `herramientas_wsl/npm_agregar.sh paquete@versión` (nunca `npm install` dentro de `video/`).
