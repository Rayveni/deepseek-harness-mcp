import base64
import logging
import os
import re
import subprocess
import zlib
from mcp.types import ImageContent
from fastmcp.utilities.types import Image

import sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from skeletons import SKELETONS

log = logging.getLogger("plantuml")

PLANTUML_JAR = os.environ.get("PLANTUML_JAR", "/app/plantuml.jar")
JAVA_BIN = os.environ.get("JAVA_BIN", "java")
SUPPORTED_FORMATS = ("svg", "png", "txt", "eps", "utxt")
TEXT_FORMATS = ("txt", "utxt")
MAX_SOURCE_BYTES = 500_000

DIAGNOSTIC_RE = re.compile(
    r"(syntax error|syntax error\?|error line|cannot be parsed|"
    r"cannot create group|assumed diagram type|the diagram does not fit|"
    r"has been already defined)",
    re.IGNORECASE,
)
# Paired guards: @start<kind> ... @end<kind> (same kind, nothing after)
GUARD_RE = re.compile(
    r"^\s*@start(\w+).*?@end\1\s*$",
    re.DOTALL | re.MULTILINE,
)



def _encode_6bit(value: int) -> str:
    if value < 10:
        return chr(48 + value)
    if value < 36:
        return chr(65 + value - 10)
    if value < 62:
        return chr(97 + value - 36)
    return "-" if value == 62 else "_"


def _append3(b1: int, b2: int, b3: int) -> str:
    return (
        _encode_6bit(b1 >> 2)
        + _encode_6bit(((b1 & 0x3) << 4) | (b2 >> 4))
        + _encode_6bit(((b2 & 0xf) << 2) | (b3 >> 6))
        + _encode_6bit(b3 & 0x3f)
    )


def encode_plantuml(text: str) -> str:
    """PlantUML-encoding: raw DEFLATE + 6-bit packing."""
    data = zlib.compress(text.encode("utf-8"))[2:-4]  # raw deflate
    out = []
    for i in range(0, len(data), 3):
        chunk = data[i : i + 3]
        if len(chunk) == 1:
            out.append(_append3(chunk[0], 0, 0))
        elif len(chunk) == 2:
            out.append(_append3(chunk[0], chunk[1], 0))
        else:
            out.append(_append3(chunk[0], chunk[1], chunk[2]))
    return "".join(out)


# ---------------------------------------------------------------- validation


def _validate_source(source: str) -> str:
    if not source or not source.strip():
        raise ValueError("source is empty")
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise ValueError(f"source too large: {len(source)} bytes (max {MAX_SOURCE_BYTES})")
    # Paired guards: the @start<kind> must match @end<kind>
    if not GUARD_RE.search(source):
        if not re.search(r"^\s*@start\w+", source, re.MULTILINE):
            raise ValueError("missing @startuml (or @startgantt/@startmindmap/...)")
        if not re.search(r"@end\w+\s*$", source, re.MULTILINE):
            raise ValueError("missing @enduml")
        raise ValueError("unpaired @start/@end guards (mismatched kind?)")
    return source


# ---------------------------------------------------------------- java runner


def _plantuml(
    args: list[str],
    source: str,
    timeout_s: int,
    text_mode: bool,
) -> dict:
    """Run plantuml.jar. Returns dict with proc or error."""
    if not os.path.isfile(PLANTUML_JAR):
        return {"ok": False, "message": f"plantuml.jar not found: {PLANTUML_JAR}"}
    cmd = [JAVA_BIN, "-Djava.awt.headless=true", "-jar", PLANTUML_JAR, *args]
    log.debug("plantuml %s", " ".join(args))
    # input must match the stream mode: str for text_mode, bytes otherwise
    stdin = source if text_mode else source.encode("utf-8")
    try:
        proc = subprocess.run(
            cmd,
            input=stdin,
            capture_output=True,
            text=text_mode,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "message": f"timeout ({timeout_s}s)"}
    except (FileNotFoundError, OSError) as err:
        return {"ok": False, "message": f"failed to launch java: {err}"}
    log.debug("plantuml exit %s", proc.returncode)
    return {"ok": proc.returncode == 0, "proc": proc}


def _stderr_text(proc, text_mode: bool) -> str:
    if text_mode:
        return proc.stderr or ""
    return (proc.stderr or b"").decode("utf-8", "replace")


def _diagnostic(text: str) -> str | None:
    """Extract syntax error diagnostic from text (stderr or stdout)."""
    m = DIAGNOSTIC_RE.search(text)
    if not m:
        return None
    lines = text.splitlines()
    idx = next((i for i, l in enumerate(lines) if m.group(0) in l), 0)
    context = " | ".join(l.strip() for l in lines[idx : idx + 2] if l.strip())
    return context or m.group(0).strip()


def _check(source: str, timeout_s: int = 120) -> dict:
    """Syntax check: plantuml.jar -syntax -pipe."""
    result = _plantuml(["-syntax", "-pipe"], source, timeout_s, text_mode=True)
    if "proc" not in result:
        return result
    proc = result["proc"]
    # Diagnostics may go to stderr or stdout depending on the version
    diag = _diagnostic(proc.stderr or "") or _diagnostic(proc.stdout or "")
    if diag:
        return {"ok": False, "syntax": True, "message": diag}
    if proc.returncode != 0:
        msg = (proc.stderr or "").strip() or f"check error (exit {proc.returncode})"
        return {"ok": False, "syntax": False, "message": msg[:500]}
    return {"ok": True, "syntax": False, "message": "ok"}


def _render(source: str, fmt: str, timeout_s: int = 180) -> dict:
    """Render via plantuml.jar -t<fmt> -pipe."""
    text_mode = fmt in TEXT_FORMATS
    result = _plantuml(["-t" + fmt, "-pipe"], source, timeout_s, text_mode)
    if "proc" not in result:
        return result
    proc = result["proc"]
    diag = _diagnostic(_stderr_text(proc, text_mode))
    if diag:
        return {"ok": False, "syntax": True, "message": diag}
    if proc.returncode != 0 or not proc.stdout:
        msg = _stderr_text(proc, text_mode).strip() or f"render error (exit {proc.returncode})"
        return {"ok": False, "syntax": False, "message": msg[:500]}
    # stdout: str for txt/utxt, bytes for binary formats
    data = proc.stdout
    return {"ok": True, "syntax": False, "data": data}


# ---------------------------------------------------------------- tools

VARIANTS = "\n".join(f"- `{name}`" for name in SKELETONS)

def register(mcp) -> None:
    @mcp.tool
    def puml_check_source(source: str) -> str:
        """Check PlantUML source syntax locally (plantuml.jar).

        source: full diagram text with @start.../@end... guards.
        Returns 'OK' or a syntax error message.
        """
        try:
            text = _validate_source(source)
        except ValueError as err:
            return f"INVALID SOURCE: {err}"
        result = _check(text)
        if result["ok"]:
            return "OK: syntax is valid"
        return f"SYNTAX ERROR: {result['message']}"


    @mcp.tool
    def puml_render(
        source: str,
        output_format: str = "png",
    ) -> Image:
        """Render PlantUML source locally (plantuml.jar).

        source: full diagram text with @start.../@end... guards.
        output_format: png (default), svg, txt, eps or utxt.
        Single java launch: plantuml.jar itself returns syntax
        errors (see _diagnostic). Returns content as base64.
        """
        fmt = output_format.lower()
        if fmt not in SUPPORTED_FORMATS:
            return f"ERROR: unsupported format '{output_format}' (use svg, png, txt, eps, utxt)"
        try:
            text = _validate_source(source)
        except ValueError as err:
            return f"INVALID SOURCE: {err}"
        rendered = _render(text, fmt)
        if not rendered["ok"]:
            if rendered.get("syntax"):
                return f"SYNTAX ERROR: {rendered['message']}"
            return f"RENDER FAILED: {rendered['message']}"
        data = rendered["data"]
        if fmt == "svg" and b"<svg" not in data[:200]:
            return "RENDER FAILED: response is not SVG"
        if fmt == "png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "RENDER FAILED: response is not PNG"
        if isinstance(data, bytes):
            payload = data
        else:
            payload = data.encode("utf-8")
        b64 = base64.b64encode(payload).decode("ascii")
        #return f"OK: rendered {len(payload)} bytes as {fmt}\nbase64_{fmt}: {b64}"
        return [ImageContent(type="image",data=b64,mimeType=f"image/{fmt}") ]


    @mcp.tool
    def puml_encode(source: str) -> str:
        """Encode PlantUML source into a shareable URL (no render).

        source: full diagram text with @start.../@end... guards.
        Returns the encoded string and the URL to open in a browser.
        NOTE: the URL points to www.plantuml.com — an external
        service. Rendering itself is local (puml_render); this
        URL is only for sharing the diagram with others.
        """
        try:
            text = _validate_source(source)
        except ValueError as err:
            return f"INVALID SOURCE: {err}"
        encoded = encode_plantuml(text)
        return (
            f"{encoded}\n\n"
            f"https://www.plantuml.com/plantuml/svg/{encoded}\n"
            f"(URL uses external www.plantuml.com; rendering is local via puml_render)"
        )


    @mcp.tool
    def puml_list_types() -> str:
        """Reference of available PlantUML diagram variants.

        Returns the list of variants: activity, sequence, component,
        deployment, class, er, state, usecase, gantt, wbs, mindmap,
        comparison.
        """
        return f"Available variants:\n{VARIANTS}"


    @mcp.tool
    def puml_skeleton(variant: str) -> str:
        """Source skeleton for the chosen diagram variant.

        variant: one of activity, sequence, component, deployment, class,
        er, state, usecase, gantt, wbs, mindmap, comparison.
        Returns a source stub with <...> placeholders.
        """
        key = variant.strip().lower()
        if key not in SKELETONS:
            return f"ERROR: unknown variant '{variant}'. Available: {', '.join(SKELETONS)}"
        return SKELETONS[key]