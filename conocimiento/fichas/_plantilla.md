# Nombre de la herramienta

```json
{
  "id": "nombre-en-minusculas-con-guiones",
  "nombre": "Nombre de la herramienta",
  "tipo": "libreria",
  "areas": ["motion-graphics"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["tipografia-cinetica"],
  "resumen": "Una línea (máx. 220 caracteres): qué es y para qué sirve. Es lo que leen los modelos en las listas.",
  "lenguajes": ["TypeScript"],
  "exporta_video": "indirecto",
  "web": "https://…",
  "repo": "dueño/repositorio",
  "paquetes": {"npm": ["paquete"], "pypi": []},
  "docs": ["https://…"],
  "llms_txt": "https://…/llms.txt",
  "licencia": "MIT (y cualquier restricción relevante)",
  "agentes": "Skills, MCP, llms.txt o qué tan bien la escriben los modelos.",
  "requisitos": "GPU, RAM, sistema, dependencias pesadas.",
  "relacionados": ["otra-ficha"],
  "fuentes": ["bandeja/AAAA-MM-DD-tema.md"],
  "verificado": "AAAA-MM-DD",
  "confianza": "por-verificar"
}
```

## Qué es
Dos o tres frases. Cómo funciona por dentro, en palabras simples.

## Úsalo para
- Casos concretos.

## No lo uses para
- Cuándo hay algo mejor (y cuál).

## Instalación
Comandos exactos. En Scriptorium: nunca `npm install` dentro de `video/` (usar `herramientas_wsl/npm_agregar.sh`).

## Ejemplo mínimo
Código corto y real (opcional).

## Ventajas
- …

## Limitaciones
- Incluye licencias, mantenimiento, rendimiento en este equipo.

## En este equipo
¿Instalado? ¿Compatible con la GP100 (16 GB, Pascal), 16 GB de RAM, WSL y el Control inteligente de aplicaciones?

<!--
Valores permitidos (los revisa «saber validar»):
  tipo:          motor | libreria | skill | mcp | plantilla | referencia | aplicacion | modelo-ia | herramienta | infraestructura
  areas:         video-explicativo | motion-graphics | audio-voz | 2d | 3d | personajes | anime | conocimiento
  prioridad:     ahora | complemento | futuro
  estado_local:  en-uso | instalado | no-instalado | incompatible
  exporta_video: si | no | indirecto | no-aplica
  confianza:     verificado (datos comprobados en la fecha) | parcial (metadatos sí, detalles no) | por-verificar
  capacidades:   ids de catalogo/capacidades.json (saber capacidades)
Los archivos que empiezan con «_» no se indexan.
-->
