"""
animation.py — VulnScout terminal animation primitives.

Provides Spinner, ProgressBar, TypeWriter, GlitchText, SeverityBadge
using raw ANSI escape codes (colorama patches sys.stdout on Windows).
All animations respect a NO_COLOR / TERM=dumb environment check.
Falls back gracefully on Windows CP1252 terminals.
"""

import itertools
import os
import random
import sys
import threading
import time

# ── colour support ──────────────────────────────────────────────────────────
try:
    import colorama
    colorama.init(autoreset=False)
    _COLOUR = True
except ImportError:
    _COLOUR = False

_NO_COLOR = os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb"
_TTY = sys.stdout.isatty()
_ANIMATE = _TTY and not _NO_COLOR

# Detect encoding capability
_ENC = getattr(sys.stdout, "encoding", "ascii").lower().replace("-", "")
_CAN_UNICODE = _ENC in ("utf8", "utf16", "utf32", "cp65001")


def _safe_write(text: str):
    """Write to stdout, replacing unencodable chars on narrow encodings."""
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        sys.stdout.write(text.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))


def _c(code: str, text: str) -> str:
    """Wrap text in an ANSI escape if colour is enabled."""
    if _ANIMATE:
        return f"\033[{code}m{text}\033[0m"
    return text


# Palette
CYAN    = lambda t: _c("96", t)
GREEN   = lambda t: _c("92", t)
YELLOW  = lambda t: _c("93", t)
RED     = lambda t: _c("91", t)
MAGENTA = lambda t: _c("95", t)
BLUE    = lambda t: _c("94", t)
GREY    = lambda t: _c("90", t)
BOLD    = lambda t: _c("1",  t)
DIM     = lambda t: _c("2",  t)

SEVERITY_COLORS = {
    "critical": RED,
    "high":     lambda t: _c("91", t),
    "medium":   YELLOW,
    "low":      BLUE,
    "info":     CYAN,
    "ok":       GREEN,
}

SEVERITY_ICONS = {
    "critical": "🔴",
    "high":     "🟠",
    "medium":   "🟡",
    "low":      "🔵",
    "info":     "⚪",
    "ok":       "🟢",
}


def severity_badge(level: str, text: str) -> str:
    level = level.lower()
    icon  = SEVERITY_ICONS.get(level, "  ")
    color = SEVERITY_COLORS.get(level, CYAN)
    return f"{icon} {color(text)}"


# ── Spinner ─────────────────────────────────────────────────────────────────
class Spinner:
    """Thread-based spinner that runs while a block executes."""
    _FRAMES_UNI = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    _FRAMES_ASC = ["-", "\\", "|", "/"]
    _FRAMES = _FRAMES_UNI if _CAN_UNICODE else _FRAMES_ASC
    _COLORS = ["96", "95", "94", "93", "92"]

    def __init__(self, message: str = "Working", delay: float = 0.08):
        self.message = message
        self.delay   = delay
        self._stop_event = threading.Event()
        self._thread = None

    def _spin(self):
        color_cycle = itertools.cycle(self._COLORS)
        for frame in itertools.cycle(self._FRAMES):
            if self._stop_event.is_set():
                break
            color = next(color_cycle)
            if _ANIMATE:
                _safe_write(f"\r  \033[{color}m{frame}\033[0m  {self.message} ")
                sys.stdout.flush()
            time.sleep(self.delay)

    def start(self):
        if _ANIMATE:
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()

    def stop(self, final_msg: str = "", success: bool = True):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        if _ANIMATE:
            icon = GREEN("OK") if success else RED("ERR")
            _safe_write(f"\r  {icon}  {final_msg or self.message}  \n")
            sys.stdout.flush()
        elif final_msg:
            print(f"  {final_msg}")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()


# ── ProgressBar ─────────────────────────────────────────────────────────────
class ProgressBar:
    """Animated in-place progress bar."""
    WIDTH = 30

    def __init__(self, total: int, label: str = ""):
        self.total   = max(total, 1)
        self.label   = label
        self.current = 0

    def update(self, n: int = 1):
        self.current = min(self.current + n, self.total)
        self._draw()

    def _draw(self):
        if not _ANIMATE:
            return
        pct   = self.current / self.total
        done  = int(self.WIDTH * pct)
        if _CAN_UNICODE:
            bar = GREEN("█" * done) + GREY("░" * (self.WIDTH - done))
        else:
            bar = GREEN("=" * done) + GREY("-" * (self.WIDTH - done))
        pct_s = CYAN(f"{pct*100:5.1f}%")
        label = BOLD(self.label[:20].ljust(20)) if self.label else ""
        _safe_write(f"\r  {label}  [{bar}] {pct_s}  {self.current}/{self.total}  ")
        sys.stdout.flush()

    def finish(self, msg: str = ""):
        self.current = self.total
        self._draw()
        if _ANIMATE:
            _safe_write(f"  {GREEN('done')}  {msg}\n")
            sys.stdout.flush()


# ── TypeWriter ───────────────────────────────────────────────────────────────
def typewriter(text: str, delay: float = 0.03, color_fn=None):
    """Print text character by character."""
    if not _ANIMATE:
        print(text)
        return
    for ch in text:
        char = color_fn(ch) if color_fn else ch
        _safe_write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


# ── GlitchText ───────────────────────────────────────────────────────────────
_GLITCH_CHARS_UNI = "!@#$%^&*<>?/\\|░▒▓█"
_GLITCH_CHARS_ASC = "!@#$%^&*<>?/\\|~+=-"
_GLITCH_CHARS = _GLITCH_CHARS_UNI if _CAN_UNICODE else _GLITCH_CHARS_ASC

def glitch_print(text: str, iterations: int = 6, delay: float = 0.055):
    """Print text with a Matrix-style glitch reveal effect."""
    if not _ANIMATE:
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode(sys.stdout.encoding or 'ascii', errors='replace').decode(sys.stdout.encoding or 'ascii'))
        return
    lines = text.split("\n")
    for _ in range(iterations):
        for line in lines:
            glitched = "".join(
                random.choice(_GLITCH_CHARS) if random.random() < 0.3 else c
                for c in line
            )
            _safe_write(f"\r\033[96m{glitched}\033[0m\n")
        _safe_write(f"\033[{len(lines)}A")  # move cursor up
        sys.stdout.flush()
        time.sleep(delay)
    # Final clean print
    for line in lines:
        _safe_write(f"\033[96m{line}\033[0m\n")


# ── Section header ────────────────────────────────────────────────────────────
def section_header(title: str, icon: str = "*"):
    width = 64
    divider = "-" * width
    bar   = CYAN(divider)
    label = BOLD(CYAN(f"  {icon}  {title}"))
    print(f"\n{bar}")
    print(label)
    print(bar)


# ── Summary table ─────────────────────────────────────────────────────────────
def summary_table(rows: list[tuple]):
    """
    rows: list of (module_name, status, finding_count, severity)
    """
    print()
    header = f"  {'MODULE':<22} {'STATUS':<10} {'FINDINGS':<10} {'SEVERITY':<10}"
    print(BOLD(CYAN(header)))
    print(CYAN("  " + "─" * 56))
    for name, status, count, sev in rows:
        status_str = GREEN("✔ OK") if status == "ok" else RED("✘ ERROR") if status == "error" else YELLOW(status)
        sev_str    = severity_badge(sev, sev.upper())
        print(f"  {BOLD(name):<22} {status_str:<20} {str(count):<10} {sev_str}")
    print(CYAN("  " + "─" * 56))


# ── Risk score bar ────────────────────────────────────────────────────────────
def risk_score_display(score: int):
    """Display a colorful risk score (0-100)."""
    width = 40
    filled = int(width * score / 100)
    if score >= 75:
        color = RED
    elif score >= 50:
        color = YELLOW
    elif score >= 25:
        color = BLUE
    else:
        color = GREEN

    bar = color("█" * filled) + GREY("░" * (width - filled))
    label = color(BOLD(f"Risk Score: {score}/100"))
    print(f"\n  {label}")
    print(f"  [{bar}]")
    if score >= 75:
        print(f"  {RED(BOLD('⚠  HIGH RISK — prioritize remediation'))}")
    elif score >= 50:
        print(f"  {YELLOW('⚠  MEDIUM RISK — review findings carefully')}")
    elif score >= 25:
        print(f"  {BLUE('ℹ  LOW RISK — minor issues detected')}")
    else:
        print(f"  {GREEN('✔  MINIMAL RISK — surface looks clean')}")
    print()
