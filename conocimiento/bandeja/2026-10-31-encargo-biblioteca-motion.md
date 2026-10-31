<!-- procesado: 2026-10-31 → estructura de la biblioteca, saber.py, capacidades.json, 72 fichas, 18 técnicas, 12 principios, 6 flujos, adaptadores (AGENTS.md, skill, MCP). -->
<!-- Encargo que el usuario pegó en el chat el 2026-10-31 (venía duplicado; se guarda una vez). Texto original sin editar. -->

Crear biblioteca de Motion Graphics y Animación Programática para agentes de IA
Objetivo
Construye una biblioteca local, persistente, modular y consultable de herramientas, repositorios, frameworks, skills, ejemplos y técnicas de motion graphics generados mediante código.
Esta biblioteca debe funcionar como una base de conocimiento y un catálogo de capacidades para agentes de programación como Claude Code, Codex, Gemini CLI y otros.
IMPORTANTE: No quiero que generes un video ni una animación de demostración en este momento. Tu tarea es investigar, recopilar, clasificar, documentar y preparar herramientas para que cualquier agente pueda utilizarlas posteriormente.
1. Investigar y catalogar herramientas
Investiga los siguientes proyectos y descubre alternativas relevantes:
Motores de animación y composición

* Remotion
* Motion Canvas
* Manim
* p5.js
* Three.js
* PixiJS
* GSAP
* Motion
* Anime.js
* Theatre.js
* Paper.js
* Rough.js
* Lottie Web

Recursos para agentes y referencias

* https://github.com/remotion-dev/skills
* https://github.com/shadcn-labs/snapcn
* https://github.com/Liamrjohnston/remotion-motion-graphics-skill
* https://github.com/av/remotion-bits
* https://github.com/imjszhang/awesome-code-video
* https://github.com/motion-canvas/examples

Busca también repositorios adicionales sobre:

* Creative coding.
* Generative art.
* Kinetic typography.
* Procedural animation.
* SVG animation.
* Canvas 2D y WebGL.
* Particle systems.
* Shaders y efectos visuales.
* Animated infographics.
* Data-driven animation.
* Transiciones cinematográficas.
* Animación de interfaces.
* Motion design systems.

No te limites a esta lista.
2. Construir la biblioteca
Crea una estructura organizada similar a esta:

```
motion-library/
├── README.md
├── AGENTS.md
├── catalog/
│   ├── tools.json
│   ├── repositories.json
│   ├── skills.json
│   └── capabilities.json
├── engines/
│   ├── remotion/
│   ├── motion-canvas/
│   ├── p5js/
│   ├── threejs/
│   └── others/
├── techniques/
│   ├── typography/
│   ├── geometry/
│   ├── particles/
│   ├── transitions/
│   ├── shaders/
│   ├── camera/
│   └── procedural/
├── references/
├── examples/
├── workflows/
├── agent-skills/
└── scripts/
```

Puedes mejorar la estructura si encuentras una arquitectura superior.
No dupliques innecesariamente repositorios completos. Prefiere referencias, documentación, índices, ejemplos pequeños y dependencias instalables bajo demanda.
3. Documentar cada recurso
Para cada herramienta o repositorio registra:

* Nombre y descripción.
* URL oficial y repositorio.
* Funcionalidades principales.
* Casos de uso recomendados.
* Tecnologías y dependencias.
* Instalación y configuración.
* Ejemplos de uso.
* Compatibilidad con agentes de IA.
* Posibilidad de exportar video.
* Licencia y restricciones relevantes.
* Fecha de última verificación.
* Estado de mantenimiento, cuando pueda verificarse.
* Ventajas y limitaciones.

No inventes información. Si algo no se puede verificar, indícalo expresamente.
4. Sistema de consulta inteligente
La biblioteca debe permitir que un agente reciba solicitudes como:

* "Quiero animar letras individualmente".
* "Necesito una animación de partículas".
* "Quiero figuras geométricas que se transformen".
* "Necesito un video explicativo de 30 segundos".
* "Quiero una animación 3D con cámara cinematográfica".

Y pueda:

1. Consultar el catálogo.
2. Identificar las técnicas necesarias.
3. Seleccionar las herramientas más apropiadas.
4. Consultar documentación y ejemplos.
5. Determinar qué dependencias necesita.
6. Utilizar los recursos seleccionados para implementar la animación.

El sistema debe funcionar sin depender de que el usuario recuerde el nombre de una librería.
Prioriza búsqueda local mediante metadatos, palabras clave y capacidades. Incorpora búsqueda semántica únicamente si aporta una ventaja demostrable.
5. Integración con agentes de IA
Prepara instrucciones reutilizables compatibles, cuando sea posible, con:

* Claude Code.
* OpenAI Codex.
* Gemini CLI.
* Otros agentes que admitan instrucciones de repositorio.

Utiliza AGENTS.md como documentación general y crea adaptadores específicos cuando sean necesarios.
Evalúa la conveniencia de crear skills reutilizables y herramientas MCP.
No presupongas que todos los agentes admiten exactamente los mismos formatos o mecanismos de descubrimiento.
6. Biblioteca de conocimientos de diseño
Además de las herramientas técnicas, documenta principios de motion design:

* Composición y jerarquía visual.
* Tipografía y legibilidad.
* Timing y spacing.
* Easing y curvas de movimiento.
* Anticipación y seguimiento.
* Movimiento secundario.
* Ritmo visual.
* Transiciones entre escenas.
* Uso de color y contraste.
* Sincronización con audio.
* Sistemas visuales coherentes.

Incluye ejemplos y referencias que permitan distinguir una animación técnicamente funcional de una visualmente profesional.
7. Actualización y mantenimiento
Prepara un mecanismo ejecutable bajo demanda para:

* Revisar repositorios y versiones.
* Detectar enlaces rotos.
* Identificar herramientas abandonadas.
* Incorporar nuevas herramientas.
* Actualizar documentación.
* Evitar duplicados.
* Conservar el historial de cambios.

No es necesario mantener procesos ejecutándose permanentemente.
8. Eficiencia y seguridad

* No descargues repositorios enormes sin necesidad.
* No instales todas las dependencias globalmente.
* Prefiere instalaciones aisladas por proyecto.
* Verifica licencias antes de reutilizar código.
* No ejecutes scripts externos sin inspeccionarlos.
* No copies proyectos completos cuando basten referencias y ejemplos.
* Mantén la biblioteca independiente de un proveedor de IA.
* No dependas de servicios de pago si existe una alternativa local adecuada.

9. Entregables
Al terminar quiero:

1. Una biblioteca organizada y persistente.
2. Un catálogo de herramientas y capacidades.
3. Documentación técnica consultable.
4. Instrucciones para que los agentes descubran y utilicen la biblioteca.
5. Un sistema de búsqueda y selección de herramientas.
6. Un mecanismo de actualización.
7. Un README que explique cómo conectar la biblioteca a proyectos nuevos y existentes.

10. Criterio de finalización
No consideres terminada la tarea únicamente porque creaste carpetas y archivos Markdown.
Verifica que:

* El catálogo contenga recursos reales.
* Los enlaces principales funcionen.
* Las herramientas estén correctamente clasificadas.
* Las instrucciones sean comprensibles para diferentes agentes.
* La búsqueda devuelva resultados relevantes.
* Se pueda consultar la biblioteca desde otro proyecto.
* No sea necesario volver a investigar las mismas herramientas en cada tarea.

Realiza pruebas de consulta usando varias solicitudes de animación, pero no generes videos.
Resultado esperado: una biblioteca de referencia y herramientas de motion graphics programáticos que cualquier agente de IA pueda consultar y aprovechar para crear animaciones de alta calidad cuando se le solicite.
