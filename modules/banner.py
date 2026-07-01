"""
banner.py — VulnScout animated banner.

Custom block-letter logo hand-crafted letter by letter so it
UNMISTAKABLY reads  V-U-L-N-S-C-O-U-T  on every terminal.

  - UTF-8 terminals  : filled Unicode block characters (█)
  - CP1252 / Windows : equivalent hash (#) characters
  - non-TTY          : plain print, no ANSI
"""

import sys
import time

try:
    from modules.animation import (
        glitch_print, CYAN, BOLD, MAGENTA, GREY, DIM,
        _ANIMATE, _safe_write, _CAN_UNICODE,
    )
except ImportError:
    from animation import (
        glitch_print, CYAN, BOLD, MAGENTA, GREY, DIM,
        _ANIMATE, _safe_write, _CAN_UNICODE,
    )

# ── Custom block-letter logo ─────────────────────────────────────────────────
#
#  Each letter occupies exactly 5 columns + 1 space separator.
#  9 letters × 6 chars = 54 chars of content, 2-space left indent = 56 total.
#
#  Letter map (read column groups):
#
#    V       U       L       N       S       C       O       U       T
#  ─────   ─────   ─────   ─────   ─────   ─────   ─────   ─────   ─────
#  X   X   X   X   X       X   X   XXXXX    XXXX   XXXXX   X   X   XXXXX
#  X   X   X   X   X       XX  X   X       X       X   X   X   X     X
#   X X    X   X   X       X X X   XXXXX    X      X   X   X   X     X
#    X     X   X   X       X  XX       X    X      X   X   X   X     X
#           XXXXX  XXXXX   X   X   XXXXX    XXXX   XXXXX   XXXXX     X
#
#  V:  converges top→bottom (clearly NOT a Y — top has TWO separate strokes)
#  S:  top-bar, left-side, mid-bar, right-side, bottom-bar
#  C:  like O but RIGHT side is OPEN ( XXXX with no right wall )
#  T:  full top bar, single centred stem
#
# ─────────────────────────────────────────────────────────────────────────────

_ROWS_UNI = [
    "  \u2588   \u2588 \u2588   \u2588 \u2588     \u2588   \u2588 \u2588\u2588\u2588\u2588\u2588  \u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588 \u2588   \u2588 \u2588\u2588\u2588\u2588\u2588",
    "  \u2588   \u2588 \u2588   \u2588 \u2588     \u2588\u2588  \u2588 \u2588     \u2588     \u2588   \u2588 \u2588   \u2588   \u2588  ",
    "   \u2588 \u2588  \u2588   \u2588 \u2588     \u2588 \u2588 \u2588 \u2588\u2588\u2588\u2588\u2588  \u2588    \u2588   \u2588 \u2588   \u2588   \u2588  ",
    "    \u2588   \u2588   \u2588 \u2588     \u2588  \u2588\u2588     \u2588  \u2588    \u2588   \u2588 \u2588   \u2588   \u2588  ",
    "        \u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588 \u2588   \u2588 \u2588\u2588\u2588\u2588\u2588  \u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588   \u2588  ",
]

# Same shape, # instead of █  (every █→#, every space stays a space)
_ROWS_ASC = [
    "  #   # #   # #     #   # #####  #### ##### #   # #####",
    "  #   # #   # #     ##  # #     #     #   # #   #   #  ",
    "   # #  #   # #     # # # #####  #    #   # #   #   #  ",
    "    #   #   # #     #  ##     #  #    #   # #   #   #  ",
    "        ##### ##### #   # #####  #### ##### #####   #  ",
]

_ROWS = _ROWS_UNI if _CAN_UNICODE else _ROWS_ASC


# ── Helper ────────────────────────────────────────────────────────────────────
def _typewriter(text: str, delay: float = 0.018, code: str = "96"):
    """Print text one character at a time (typewriter effect)."""
    if not _ANIMATE:
        print(text)
        return
    for ch in text:
        _safe_write(f"\033[{code}m{ch}\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    _safe_write("\n")


# ── Public entry point ────────────────────────────────────────────────────────
def show(version: str):
    print()

    # Glitch-reveal the block-letter logo, then settle into final clean render
    glitch_print("\n".join(_ROWS), iterations=6, delay=0.048)

    print()

    # Tagline — typewriter effect in magenta
    _typewriter(
        "  [*]  Authorized Web Recon & Vulnerability Surface Mapper  [*]",
        delay=0.015,
        code="95",
    )

    # Info bar — version + author (dimmed)
    div = "  " + "-" * 64
    info = (
        f"  v{version:<8}  "
        f"by Shridhar Vinayak Kirtane"
        f"   github.com/shridhar3902/vulnscout"
    )
    if _ANIMATE:
        _safe_write(f"\033[90m{div}\033[0m\n")
        _safe_write(f"\033[90m{info}\033[0m\n")
        _safe_write(f"\033[90m{div}\033[0m\n")
    else:
        print(div)
        print(info)
        print(div)

    print()
