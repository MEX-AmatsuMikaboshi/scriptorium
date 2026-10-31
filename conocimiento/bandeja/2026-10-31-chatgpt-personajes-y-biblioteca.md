<!-- procesado: 2026-10-31 → fichas: blender, blender-mcp, scenario-skills, opentoonz, opentoonz-mcp, inochi2d, live2d-cubism, rhubarb-lip-sync, krita-mcp, mmd-tools, vrm-addon-blender, three-vrm, hy-motion, unity-mcp, motion-canvas, manim, remotion-skills, remotion-template-three, lancedb, sqlite-fts5; técnica personajes; flujos personaje-que-habla y modelo-3d-en-video. -->

# Conversación con ChatGPT: personajes anime, modelado 3D y cómo guardar el conocimiento

Pegada por el usuario el 2026-10-31. Abajo, el texto original (solo se juntaron líneas en blanco repetidas).

## Lo que se verificó al procesarla (2026-10-31)

- **Verificado**: Scenario Agent Skills existe (`scenario-labs/skills`, MIT), pero casi todas sus skills usan el servicio
  de pago de Scenario; las *expert tools* de Blender no lo necesitan. MCP for Blender (`ahujasid/mcp-for-blender`) y
  su comando `uvx mcp-for-blender setup` son reales (el paquete antes se llamaba `blender-mcp`). MMD Tools, VRM Add-on,
  three-vrm, Unity MCP (`CoplayDev/unity-mcp`), Inochi Creator, Live2D CubismWebSamples, Rhubarb, HY-Motion, Remotion,
  Motion Canvas, Manim y LanceDB existen y están en el catálogo con sus datos reales.
- **HY-Motion**: confirmado que pide 24 GB (Lite) y 26 GB (estándar) de VRAM y no admite varias personas → incompatible
  con la GP100 de 16 GB.
- **No encontrado**: un repositorio «Anime-Tools» (shaders anime, contornos, animación escalonada). Parecidos: NprEevee
  (kents00) y la rama NPR de Blender; por verificar si interesa.
- **No encontrado**: «OpenToonz Headless» con JSON-RPC. Lo más parecido es `c0d33ngr/opentoonz-mcp` (MCP que usa el motor
  de scripts en modo CLI y `tcomposer`).
- **Krita MCP**: hay varios; se registró `edithatogo/krita-cli` (MIT). Krita no está instalado.
- **En el equipo** (detectado): Blender 5.2.2, Unity 6000.6.7f1 y 2022.3.22f1, VRoid Studio 2.14.0 (probablemente el
  «otro modelador» que no se recordaba).

## Decisiones del usuario que salen de esta conversación

1. Lo primero son **videos explicativos hechos con programación** (lo que ya hace Scriptorium).
2. Después, **meter modelos 2D/3D en esos videos**.
3. Más adelante, **caricaturas y anime**.
4. Ahora toca **juntar toda la información** en un almacenamiento organizado; la técnica de búsqueda (texto, vectorial,
   grafo) se decide después con pruebas.
5. (Dicho en el chat de Claude Code el mismo día) El trabajo lo harán sobre todo **modelos locales**, con mínima
   intervención de IAs grandes: la biblioteca debe darles todo desde el principio.

---

## Texto original

Encontré varios repositorios de GitHub bastante más adecuados para lo que buscas: animar personajes humanos, estilo anime, en 2D o 3D, mediante código y agentes de IA como Claude Code, Codex o Gemini.

La diferencia fundamental es que no buscas simplemente motion graphics, sino herramientas que permitan producir escenas con personajes, expresiones faciales, movimientos corporales, cámaras, diálogos e incluso peleas.
1. Los repositorios que más recomiendo

Scenario Agent Skills
Mi primera elección como biblioteca
Incluye skills especializadas en animación de personajes, rigging, Grease Pencil, actuación, sincronización labial, iluminación y cinematografía. Sus skills expertas de Blender pueden funcionar sin el servicio de generación de Scenario.
GitHub

OpenToonz

Ideal para anime 2D tradicional. Software de producción de animación cuadro por cuadro, basado en Toonz, utilizado históricamente en los flujos de producción de Studio Ghibli. Se puede automatizar parcialmente mediante ToonzScript.
OpenToonz+1

MCP for Blender

Ideal para anime 3D controlado por agentes. Permite que una IA escriba y ejecute Python dentro de Blender, controle escenas, personajes, materiales, rigging, animaciones, cámaras y renders.
GitHub

2. Repositorios para personajes anime 2D
Repositorio	Qué permite hacer	Utilidad para agentes
OpenToonz Headless	Dibujar, crear fotogramas, interpolar, deformar personajes y renderizar mediante JSON-RPC	Muy alta, pero experimental. Documenta compilación en Linux
GitHub
Inochi Creator	Crear personajes anime 2D articulados con deformaciones y expresiones	Alta, requiere preparar las ilustraciones y el rig
GitHub
Inochi2D SDK	Controlar personajes 2D articulados desde aplicaciones programadas	Alta, es una librería de desarrollo, no un editor
GitHub
Live2D Cubism Web Samples	Programar movimientos y expresiones de modelos Live2D	Alta, requiere modelos compatibles y revisar licencias
Live2D/CubismWebSamples · GitHub
Rhubarb Lip Sync	Sincronizar bocas de personajes 2D con audio y diálogos	Muy alta; tiene CLI y formatos JSON/XML
GitHub
Krita MCP	Permitir que un agente dibuje, edite capas e inspeccione ilustraciones	Buena para crear y revisar recursos visuales, no sustituye un animador completo
GitHub

Diferencia importante: OpenToonz está orientado a la animación 2D tradicional, mientras que Inochi2D y Live2D animan personajes utilizando ilustraciones separadas en capas y deformaciones. Son métodos distintos, y cada uno tiene ventajas.
3. Repositorios para anime 3D y movimiento humano
Repositorio	Función principal	Aplicación
MMD Tools	Importar modelos anime PMX y movimientos VMD a Blender	Animaciones de cuerpo completo, bailes y escenas con personajes
GitHub
VRM Add-on for Blender	Importar, editar y exportar personajes VRM, con API Python	Personajes anime 3D reutilizables
GitHub
three-vrm	Animar y visualizar personajes VRM mediante JavaScript y Three.js	Personajes anime animados directamente en navegador
GitHub
HY-Motion 1.0	Generar movimiento humano 3D a partir de texto	Caminar, correr, realizar acciones y producir animaciones esqueléticas
GitHub
Anime-Tools	Shaders anime, contornos, iluminación y animación escalonada	Dar apariencia de anime 2D a modelos 3D
GitHub
Unity MCP	Controlar proyectos y escenas de Unity mediante agentes	Animaciones interactivas, videojuegos y cinemáticas
GitHub

Ojo con HY-Motion: aunque genera movimientos y no videos completos, su documentación señala aproximadamente 24 GB de VRAM para Lite y 26 GB para el modelo estándar. No sería mi primera opción para un equipo con GPU limitada. Además, todavía no admite directamente interacciones entre varias personas.
GitHub+1

4. Cómo los combinaría para conseguir calidad
Opción A — Anime 2D tradicional
Claude Code / Codex
Skills + OpenToonz
Fotogramas y render

Para secuencias dibujadas con poses expresivas, acción y cambios de perspectiva. Requiere ilustraciones originales, planificación visual y revisión cuadro por cuadro.

Opción B — Personajes anime 2D articulados
Arte por capas
Inochi2D / Live2D
Animación por código

Para personajes que hablan, parpadean, cambian de expresión y realizan movimientos controlados. Muy adecuado para diálogos y primeros planos.

Opción C — Anime 3D cinematográfico
Agente + Blender MCP
VRM / MMD + movimientos
Toon render

Para personajes de cuerpo completo, cámaras dinámicas, combates y escenas complejas. Es la ruta que priorizaría para producciones programáticas con movimientos humanos elaborados.

5. La biblioteca que instalaría en tus agentes
De todos los proyectos, Scenario Agent Skills es particularmente interesante porque ya tiene conocimientos organizados para agentes, incluyendo:
- scenario-blender-animation: movimiento corporal, actuación, ciclos y lip-sync.
- scenario-blender-rigging: esqueletos, controles IK/FK y deformaciones.
- scenario-blender-grease-pencil: anime 2D y 2.5D, dibujo cuadro por cuadro.
- scenario-blender-previs-storyboard: planificación de tomas y cámaras.
- scenario-blender-lighting-rendering: iluminación y renderizado.
Estos componentes están documentados en el repositorio.
GitHub

Para instalar el catálogo y seleccionar las skills desde el menú:
Terminal
 Copiar
npx skills add scenario-labs/skills

Para conectar Codex con Blender mediante el MCP verificado:
codex mcp add blender -- uvx mcp-for-blender

Previamente necesitas instalar Blender, el complemento MCP correspondiente y uv.
GitHub

Mi conclusión
Para el objetivo de generar personajes anime de calidad sin depender de un generador de video, usaría principalmente Blender + MCP + Scenario Agent Skills + modelos VRM/MMD + herramientas de render estilo anime.

Para anime 2D tradicional utilizaría OpenToonz; si buscas personajes 2D reutilizables, Inochi2D sería más práctico.

Hay que considerar que ninguno de estos repositorios garantiza por sí solo resultados comparables a una producción profesional de anime: la calidad depende de los personajes, los rigs, la dirección artística y el refinamiento del movimiento.

La decisión que más cambiaría mi recomendación es esta: ¿quieres que la IA cree escenas completas de anime, con personajes peleando, corriendo y actuando, o quieres que genere personajes animados reutilizables para videos, páginas web y videojuegos? Son dos arquitecturas de producción bastante diferentes.

mira tengo tambien instalado modeladores como blender y no recuerdo el otro pero a lo que me refiero es por si o ocupan ademas agregar un mcp o skill para poder usarlos para

Procesó durante 29s

¡Ahora sí, te entiendo! Lo que buscas es que Codex, Claude Code, Gemini u otro agente de IA aproveche los programas de modelado y animación que ya tienes instalados, como Blender, para crear animaciones de personas, personajes estilo anime, escenas 2D y 3D, sin limitarse a generar videos con IA.

Y sí, podemos combinar MCP + Skills + repositorios especializados para conseguirlo.
1. Cómo funcionaría
Agente de IA

Codex / Claude Code / Gemini

MCP

Conecta la IA con los programas

Skills

Aportan técnicas y procedimientos de animación

Blender

Modelado, rigging, animación y render

Otros programas

Unity, Godot, Maya, Unreal, etc.

El agente podría recibir una instrucción como:
Crea una escena estilo anime de dos personajes peleando. Usa Blender, crea o importa los personajes, prepara sus esqueletos, anima los movimientos, configura las cámaras, aplica iluminación y materiales estilo anime y renderiza la secuencia. Revisa los resultados y corrige los errores.

Para hacerlo, el agente necesitaría herramientas conectadas al programa, conocimientos de animación y recursos adecuados. No basta con instalar una skill para que pueda controlar Blender.
2. Las integraciones que te recomiendo
Herramienta	Qué instalar	Prioridad
Blender	MCP for Blender	Alta
Biblioteca de animación	Scenario Agent Skills	Alta
Unity, si lo tienes	Unity MCP	Opcional
Anime 3D	VRM Add-on	Alta para personajes VRM
Anime 2D/2.5D	Grease Pencil de Blender + skills especializadas	Alta si quieres ese estilo

El MCP de Blender permite ejecutar Python en escenas reales; las skills de Scenario incluyen instrucciones especializadas de rigging, animación, cámaras, iluminación y Grease Pencil. Estas skills expertas no requieren contratar el servicio de generación de Scenario.
GitHub+2

3. Cómo instalarlo en tu computadora
Como usas Windows, la forma más sencilla es:

Paso 1. Instalar el gestor necesario

En PowerShell:
winget install --id=astral-sh.uv -e

Paso 2. Configurar automáticamente Blender MCP

Abre una terminal nueva y ejecuta:
uvx mcp-for-blender setup

Este instalador detecta clientes compatibles, incluidos Codex, Claude Code y Antigravity, permite seleccionar cuáles configurar e instala el complemento en Blender. Después reinicia el agente y Blender.
GitHub

Paso 3. Añadir las skills de animación
npx skills add scenario-labs/skills --skill scenario-blender-expert scenario-blender-animation scenario-blender-rigging scenario-blender-grease-pencil scenario-blender-previs-storyboard scenario-blender-lighting-rendering scenario-blender-texturing-shading

Estas skills están documentadas principalmente para Blender 5.2 LTS. Conviene verificar tu versión antes de utilizarlas.
GitHub

4. Prompt para que Codex o Claude Code prepare todo
Puedes darle esta instrucción al agente para que examine tu computadora y configure las herramientas compatibles.
Quiero preparar mi computadora como un entorno profesional de animación programática 2D y 3D, especialmente para crear personas y personajes estilo anime utilizando agentes de IA.

Objetivo: aprovechar los programas de modelado, animación y motores gráficos que ya tengo instalados, incorporando MCP, skills, addons, scripts y repositorios especializados cuando sean necesarios.

Tareas:
1. Detecta los programas instalados relacionados con modelado, animación, renderizado y motores gráficos, incluyendo Blender, Unity, Godot, Unreal Engine y cualquier otro disponible.
2. Identifica sus versiones, capacidades de automatización y posibles incompatibilidades.
3. Investiga sus APIs, interfaces de línea de comandos, MCP y skills disponibles.
4. Para Blender, evalúa ahujasid/mcp-for-blender y las skills expertas de scenario-labs/skills.
5. Selecciona herramientas especializadas en modelado de personajes, rigging, expresiones faciales, animación corporal, anime 2D, anime 3D, cámaras, iluminación y renderizado.
6. Prioriza herramientas locales, gratuitas, de código abierto y compatibles con mi entorno.
7. No instales componentes redundantes ni servicios de pago innecesarios.
8. Antes de modificar configuraciones existentes, hacer instalaciones importantes o ejecutar scripts remotos, explícame los cambios y solicita autorización.
9. Configura las integraciones aprobadas y realiza pruebas reales de comunicación con los programas.
10. Crea una biblioteca reutilizable de herramientas y skills para futuros proyectos de animación.
11. Comprueba el resultado con una escena sencilla que incluya un personaje animado, una cámara y un render de prueba.
Criterios de calidad: las animaciones deben priorizar movimiento natural, expresividad, consistencia visual, buenas deformaciones, dirección cinematográfica y estética anime profesional.

Entrega: inventario de software, herramientas instaladas, integraciones funcionales, limitaciones pendientes y guía para utilizar todo desde el agente.

No confundas una integración MCP con una skill: verifica que realmente puedas controlar el software antes de declarar que funciona.

Mi recomendación: empezar con Blender y sus skills expertas. No necesitas instalar cinco programas distintos para conseguir buenas animaciones. Primero hay que conseguir que el agente controle Blender correctamente, que pueda utilizar personajes articulados y que genere animaciones y renders verificables.

Después podemos conectar el otro programa que tienes instalado, una vez identificado.

osea asi pero no, si quiero agregar esto del modelado o asi pero lo inicial es hacer videos con base a pura programacion o de lo que empesamos habalndo pero lo quiero para meteer esos modelados a los videos ya sea para hacer o agregar a videos explicativos que es lo primero para lo que se va a usar y lo segundo para hacer caricaturas o animes pero eso ya para despues lo que quiero ahorita es tener en un almacenamiento no se si en forma de RAG o grafos o vectoriales pero de momento voy a ir juntando toda la info que quiero tener

Memoria actualizada

Ahora sí, ya quedó claro el proyecto. No quieres construir todavía un sistema de animación ni instalar todas las herramientas. Quieres crear una biblioteca de conocimiento especializada en producción audiovisual mediante código, que cualquier agente de IA pueda consultar para saber qué herramientas utilizar y cómo utilizarlas.

Y quieres ir alimentando esa biblioteca con repositorios, documentación, técnicas, ejemplos, MCP y skills conforme los vayamos encontrando.
1. El objetivo real de tu biblioteca
Biblioteca de conocimiento audiovisual para IA

Conocimiento reutilizable, independiente del modelo o agente

Prioridad actual
Videos explicativos programáticos

Animación de textos, diagramas, personajes sencillos, gráficos, transiciones, simulaciones y movimientos cinematográficos, generados mediante código.
Complemento
Modelos y escenas 2D/3D

Incorporar personajes, objetos y animaciones creados con Blender u otros programas dentro de los videos explicativos.
Futuro
Caricaturas y anime

Aprovechar la biblioteca para desarrollar historias, personajes, actuaciones, escenas complejas y animaciones completas.

Lo importante es que las tres áreas compartan conocimiento. No tendría sentido construir tres bibliotecas aisladas.
2. ¿RAG, base vectorial o grafos?
Son tecnologías que pueden complementarse, no necesariamente alternativas excluyentes.
Tecnología	Para qué te serviría	Mi criterio
Archivos Markdown + Git	Guardar repositorios, documentación, técnicas, ejemplos y decisiones	Base principal desde ahora
Búsqueda de texto completo	Localizar herramientas, comandos y documentación exacta	Muy útil desde el principio
Base vectorial	Encontrar técnicas aunque no recuerdes el nombre exacto	Agregar cuando tengas bastante contenido
RAG	Recuperar información relevante y entregársela al agente para que responda o programe	Agregar como capa de consulta
Grafo de conocimiento	Relacionar herramientas, motores, formatos, MCP, skills y dependencias	Agregar cuando las relaciones se vuelvan complejas

Mi elección sería una arquitectura híbrida, pero implementada gradualmente. Empezaría guardando las fuentes en Markdown y metadatos estructurados, con un repositorio Git como fuente de verdad. Después añadiría índices de búsqueda.

Así no te comprometes prematuramente con una base de datos ni te arriesgas a perder o rehacer todo lo recopilado.
3. Así organizaría el almacenamiento
La estructura inicial sería algo parecido a esto:
Biblioteca-Animacion-IA/

01-motion-graphics/

Animaciones de texto, figuras, gráficos y transiciones

02-videos-explicativos/

Narrativa visual, diagramas y escenas educativas

03-animacion-2d/

Ilustraciones, personajes y técnicas 2D

04-animacion-3d/

Blender, modelos, rigging y movimiento

05-integraciones/

Cómo incorporar 2D/3D en videos programáticos

06-mcp-y-skills/

Herramientas y conocimientos para los agentes

07-ejemplos/

Código funcional, referencias y proyectos

08-caricaturas-anime/

Recursos para desarrollo futuro

09-investigacion/

Fuentes pendientes de analizar o verificar

AGENTS.md — Cómo consultar esta biblioteca

catalogo.json — Índice estructurado

El archivo AGENTS.md contendría instrucciones generales para los agentes, mientras que cada herramienta tendría su propia ficha. Los modelos 3D, videos y otros archivos pesados podrían almacenarse por separado, con referencias desde el catálogo.
4. Primer conjunto de conocimientos que deberíamos recopilar
Recurso	Función en tu biblioteca
Remotion	Composición, escenas, audio, efectos y renderizado de videos mediante React
GitHub
Remotion Agent Skills	Buenas prácticas y procedimientos para que Codex o Claude Code creen videos
Remotion
Motion Canvas	Animaciones vectoriales explicativas con TypeScript, sincronizadas con narración
GitHub
Manim	Explicaciones matemáticas, algoritmos, diagramas y visualizaciones precisas
GitHub
Remotion + React Three Fiber	Ejemplo concreto de incorporar objetos 3D en una composición de video
GitHub
Blender MCP	Conexión de un agente con Blender para preparar y renderizar recursos 3D
LanceDB	Posible motor futuro de búsqueda vectorial y de texto, utilizable localmente
GitHub

Esto es el inicio del catálogo, no una selección definitiva. Por ejemplo, Remotion tiene condiciones especiales de licencia para ciertos usos empresariales que habría que registrar en su ficha.
GitHub

5. Cómo registrar cada recurso
No guardaría solamente un enlace de GitHub. Cada entrada debería incluir información que permita al agente decidir cuándo conviene usarla.

Por ejemplo:
id: motion-canvas
nombre: Motion Canvas
tipo: framework
categoria: motion-graphics

prioridad: principal
lenguaje: TypeScript

capacidades:
  - animacion-vectorial
  - videos-explicativos
  - sincronizacion-con-voz
  - visualizacion-de-procesos

integracion:
  requiere_mcp: false
  usable_mediante_codigo: true

fuente: https://github.com/motion-canvas/motion-canvas
estado: documentado
pruebas_locales: pendiente

relacionados:
  - remotion
  - manim

Además de estos metadatos, almacenaría documentación técnica seleccionada, ejemplos ejecutables, problemas conocidos, compatibilidades y referencias a las fuentes originales. Así evitamos que un RAG solo recupere descripciones generales poco útiles.
6. Mi recomendación para construirla por etapas
Primera etapa — Recopilación

Markdown + JSON/YAML + Git. Guardamos y clasificamos recursos sin instalar todos los programas.

Segunda etapa — Consulta inteligente

SQLite FTS5 para búsqueda exacta y, si hace falta, LanceDB para búsqueda semántica.
SQLite+1

Tercera etapa — Relaciones y agentes

Incorporamos RAG, relaciones entre herramientas y una interfaz para que diferentes agentes consulten el mismo catálogo. Un grafo de conocimiento solo si aporta ventajas reales.

Por ahora no instalaría una base vectorial, un servidor de grafos ni un MCP para cada herramienta. Primero construiría una colección de fuentes bien organizada, verificable y portable.

La idea final es que puedas pedirle a un agente: «Hazme un video explicativo profesional sobre este tema, con gráficos animados, personajes y un modelo 3D».

El agente consultaría la biblioteca, elegiría los recursos pertinentes, utilizaría los conocimientos técnicos recopilados y produciría el video mediante programación.

Y cuando pasemos a caricaturas o anime, reutilizaríamos gran parte de la misma infraestructura.

Ya queda establecido este enfoque para el proyecto: primero recopilación de conocimiento sobre videos programáticos; modelado 2D/3D como complemento; y producción de anime como objetivo posterior.
