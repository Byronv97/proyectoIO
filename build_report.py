"""Build the academic project report as a styled PDF."""

from html import escape
from pathlib import Path
import re

import markdown
from xhtml2pdf import pisa


ROOT = Path(__file__).parent
SOURCE = ROOT / "PROJECT_DRAFT.md"
OUTPUT = ROOT / "INFORME_PROYECTO.pdf"


def _render_equation(match: re.Match[str]) -> str:
    equation = match.group(1).strip()
    equation = re.sub(r"\\text\{([^}]*)\}", r"\1", equation)
    equation = equation.replace(r"\leq", "<=")
    equation = equation.replace(r"\geq", ">=")
    equation = equation.replace(r"\qquad", "   ")
    equation = equation.replace(r"\quad", "   ")
    equation = equation.replace("{", "").replace("}", "")
    return f'<div class="equation">{escape(equation)}</div>'


def _markdown_to_html(source: str) -> str:
    source = re.sub(r"\\\[(.*?)\\\]", _render_equation, source, flags=re.DOTALL)
    body = markdown.markdown(
        source,
        extensions=["extra", "sane_lists", "toc"],
    )
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <style>
    @page {{ size: Letter; margin: 2cm 1.8cm 2cm 1.8cm; }}
    body {{
      color: #1f2937;
      font-family: "DejaVu Sans", Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.45;
    }}
    h1 {{
      color: #12343b;
      font-size: 23pt;
      line-height: 1.15;
      margin: 0 0 24pt;
      text-align: center;
    }}
    h2 {{
      border-bottom: 1px solid #9ab7b2;
      color: #12343b;
      font-size: 16pt;
      margin: 24pt 0 9pt;
      page-break-after: avoid;
    }}
    h3 {{
      color: #2f7f75;
      font-size: 12.5pt;
      margin: 16pt 0 6pt;
      page-break-after: avoid;
    }}
    p, ul, ol, blockquote {{ margin: 7pt 0; }}
    li {{ margin: 3pt 0; }}
    blockquote {{
      background: #f1f7f6;
      border-left: 4px solid #2f7f75;
      margin-left: 0;
      padding: 8pt 12pt;
    }}
    code {{
      background: #f1f5f9;
      border-radius: 3px;
      font-family: "DejaVu Sans Mono", monospace;
      padding: 1px 3px;
    }}
    table {{
      font-size: 9pt;
      margin: 10pt 0 14pt;
      page-break-inside: avoid;
      width: 100%;
    }}
    th {{ background: #dcebe8; color: #12343b; }}
    th, td {{ border: 1px solid #b7c9c6; padding: 5pt 6pt; }}
    tr {{ page-break-inside: avoid; }}
    .equation {{
      background: #f8fafc;
      border: 1px solid #d7e2e0;
      font-family: "DejaVu Sans Mono", monospace;
      margin: 10pt auto;
      padding: 8pt;
      text-align: center;
      width: 86%;
    }}
    img {{ display: block; margin: 10pt auto; max-height: 15cm; max-width: 100%; }}
    a {{ color: #176b87; }}
  </style>
</head>
<body>
{body}
</body>
</html>"""


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    html = _markdown_to_html(source)
    with OUTPUT.open("wb") as pdf_file:
        result = pisa.CreatePDF(
            html,
            dest=pdf_file,
            path=str(ROOT),
            encoding="utf-8",
        )
    if result.err:
        raise RuntimeError("No fue posible generar el PDF del informe.")
    print(f"PDF generado: {OUTPUT}")


if __name__ == "__main__":
    main()
