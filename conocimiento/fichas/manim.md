# Manim Community

```json
{
  "id": "manim",
  "nombre": "Manim Community",
  "tipo": "motor",
  "areas": ["video-explicativo"],
  "prioridad": "ahora",
  "estado_local": "no-instalado",
  "capacidades": ["matematicas", "diagramas", "morphing", "geometria", "video-explicativo", "composicion-video"],
  "resumen": "Animaciones matemáticas en Python (el estilo de 3Blue1Brown): ecuaciones LaTeX que se transforman, gráficas de funciones, geometría y diagramas precisos.",
  "lenguajes": ["Python"],
  "exporta_video": "si",
  "web": "https://www.manim.community",
  "repo": "ManimCommunity/manim",
  "paquetes": {"pypi": ["manim"]},
  "docs": ["https://docs.manim.community"],
  "licencia": "MIT",
  "agentes": "API estable y muy presente en datos de entrenamiento: los modelos la escriben bien.",
  "requisitos": "Python, Cairo, Pango, FFmpeg; LaTeX (texlive) para ecuaciones.",
  "relacionados": ["motion-canvas", "katex", "remotion"],
  "fuentes": ["bandeja/2026-10-31-encargo-biblioteca-motion.md", "bandeja/2026-10-31-chatgpt-personajes-y-biblioteca.md"],
  "verificado": "2026-10-31",
  "confianza": "verificado"
}
```

## Qué es
Versión comunitaria de la librería de Grant Sanderson. Una escena es una clase con `construct()`; `self.play(Transform(a, b))` anima. Renderiza a MP4/PNG/GIF con `manim -qh escena.py Clase`. (La versión original de 3b1b es `manimgl`; la comunitaria es más estable y documentada.)

## Úsalo para
- Fórmulas que se transforman, demostraciones, geometría, gráficas de funciones.
- Clips que luego se insertan en Remotion con `<OffthreadVideo>` (flujo [clip-de-manim-en-remotion](../flujos/clip-de-manim-en-remotion.md)).

## No lo uses para
- Tipografía editorial o estética de motion graphics comercial (se nota «estilo Manim»).

## Instalación
```bash
# En WSL, en un venv propio (no en el de Scriptorium)
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg   # + texlive-latex-extra para LaTeX
uv venv ~/.local/share/manim && uv pip install --python ~/.local/share/manim manim
```

## Ejemplo mínimo
```python
from manim import *
class Pitagoras(Scene):
    def construct(self):
        eq = MathTex(r"a^2 + b^2 = c^2")
        self.play(Write(eq))
        self.play(eq.animate.scale(1.5).set_color(YELLOW))
```

## Ventajas
- Precisión matemática y LaTeX nativo.
- Los modelos chicos lo programan razonablemente bien.
- MIT, Python: encaja con el resto de Scriptorium.

## Limitaciones
- Render en CPU (Cairo) lento en 1080p60.
- Sin audio integrado sofisticado: sincronizar se hace afuera.

## En este equipo
No instalado. Instalar en un venv aparte en WSL; el texto en español requiere `Tex` con babel o `Text` (Pango) para acentos.
