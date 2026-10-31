# HY-Motion 1.0

```json
{
  "id": "hy-motion",
  "nombre": "HY-Motion 1.0",
  "tipo": "modelo-ia",
  "areas": ["3d", "personajes"],
  "prioridad": "futuro",
  "estado_local": "incompatible",
  "capacidades": ["movimiento-humano", "personajes-3d"],
  "resumen": "Modelo de Tencent que genera movimiento humano 3D (esqueleto) a partir de texto. Pide 24–26 GB de VRAM: no cabe en la GP100 de 16 GB.",
  "lenguajes": ["Python"],
  "exporta_video": "no",
  "web": "https://hunyuan.tencent.com/motion",
  "repo": "Tencent-Hunyuan/HY-Motion-1.0",
  "licencia": "Licencia comunitaria de Tencent Hunyuan (no estándar): revisar restricciones de uso y de territorio antes de usarlo.",
  "requisitos": "HY-Motion-1.0 (1.0B): 26 GB de VRAM mínimo; Lite (0.46B): 24 GB. Con una semilla, prompt de menos de 30 palabras y menos de 5 s baja el consumo.",
  "relacionados": ["blender", "mmd-tools"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Texto → animación esquelética (caminar, correr, acciones). No genera video, solo movimiento.

## Úsalo para
- Cuando haya una GPU con más de 24 GB (o un servicio local más grande).

## Limitaciones
- No admite interacciones entre varias personas.
- Incompatible con el equipo actual (16 GB de VRAM, Pascal sin FlashAttention).

## En este equipo
Incompatible. Alternativas: movimientos MMD/VMD existentes, captura propia o animación a mano en Blender.
