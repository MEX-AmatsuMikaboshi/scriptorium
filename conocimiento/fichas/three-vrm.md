# three-vrm

```json
{
  "id": "three-vrm",
  "nombre": "three-vrm",
  "tipo": "libreria",
  "areas": ["3d", "personajes", "anime"],
  "prioridad": "complemento",
  "estado_local": "no-instalado",
  "capacidades": ["personajes-3d", "lip-sync", "render-toon"],
  "resumen": "Carga y anima personajes VRM en Three.js: expresiones (incluidas las vocales de la boca), mirada, huesos humanoides y física de pelo.",
  "lenguajes": ["TypeScript"],
  "exporta_video": "indirecto",
  "web": "https://pixiv.github.io/three-vrm/packages/three-vrm/examples",
  "repo": "pixiv/three-vrm",
  "paquetes": {"npm": ["@pixiv/three-vrm"]},
  "licencia": "MIT",
  "relacionados": ["threejs", "vroid-studio", "remotion-template-three", "rhubarb-lip-sync"],
  "fuentes": ["bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
`GLTFLoader` + `VRMLoaderPlugin`: da `vrm.expressionManager` (feliz, triste, aa/ih/ou/ee/oh para la boca), `vrm.humanoid` para posar huesos y `vrm.update(dt)`.

## Úsalo para
- Un personaje anime que habla dentro de un video de Remotion (expresiones según la alineación de la voz).

## Instalación
```bash
npm i three @pixiv/three-vrm
```

## Limitaciones
- Los resortes de pelo se simulan con dt: en video, avanzar con dt fijo = 1/fps desde el cuadro 0 para que sea determinista.

## En este equipo
No instalado. Ver flujo [personaje-que-habla](../flujos/personaje-que-habla.md).
