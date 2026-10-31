# Agregar información nueva a la biblioteca

```json
{
  "id": "agregar-conocimiento",
  "nombre": "Agregar información nueva a la biblioteca",
  "tipo": "flujo",
  "prioridad": "ahora",
  "capacidades": ["busqueda-conocimiento"],
  "herramientas": ["sqlite-fts5"],
  "resumen": "Cómo procesar lo que se va juntando (notas, conversaciones, enlaces) para convertirlo en fichas verificadas sin duplicar ni inventar."
}
```

## 1. Guardar lo crudo
Pega la nota, la conversación o la lista de enlaces en `bandeja/AAAA-MM-DD-tema.md`, tal cual. Es la fuente original: no se edita después.

## 2. Procesar (lo puede hacer un modelo local o grande)
1. `saber bandeja` → notas pendientes.
2. Por cada herramienta o repositorio mencionado:
   - `saber buscar "<nombre o para qué sirve>"`: ¿ya existe? Si sí, actualizar esa ficha.
   - Si es de GitHub y no existe: `saber nuevo <url-del-repositorio>` (crea el esqueleto con datos reales de la API).
   - Completar la ficha: tipo, áreas, prioridad (ahora / complemento / futuro), capacidades (de `catalogo/capacidades.json`), resumen ≤ 220 caracteres, secciones.
   - **No inventar**: lo que no se pudo comprobar va con `"confianza": "por-verificar"` o dice «por verificar» en el texto.
3. Si aparece una forma nueva de pedir algo («quiero que el texto tiemble»), agregar el sinónimo a la capacidad correspondiente.
4. Agregar 1–2 consultas de prueba a `catalogo/pruebas.json` con lo que debería encontrarse.
5. `saber actualizar --solo id1,id2` (metadatos + README a la caché), `saber validar`, `saber probar`.
6. Marcar la nota: primera línea `<!-- procesado: AAAA-MM-DD → fichas: a, b, c -->`.
7. Una línea en `HISTORIAL.md`.

## Mantenimiento periódico (bajo demanda)
`saber actualizar` (versiones, licencias, archivados, renombrados, abandono), `saber enlaces` (enlaces rotos), `saber validar` (duplicados y referencias). La historia queda en git.
