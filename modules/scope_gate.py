"""
Scope authorization gate.

VulnScout will not run any scanning module against a target until the
operator explicitly confirms they are authorized to test it. This is
not optional and is not meant to be bypassed except for scripted runs
where authorization has already been verified out-of-band (--yes flag).
"""

DISCLAIMER = """
This tool performs active and passive reconnaissance against the target
you specify. Running it against a domain you do not own or do not have
explicit written authorization to test (e.g. a HackerOne / Bugcrowd
program scope, your own infrastructure, or a lab environment) may be
illegal in your jurisdiction.

By continuing, you confirm that:
  1. You own this target, OR
  2. You have explicit written authorization to test it (e.g. it is
     in-scope for a bug bounty program you are enrolled in), OR
  3. This is a lab/training target (TryHackMe, HackTheBox, etc.)

The author accepts no responsibility for misuse of this tool.
"""


def confirm(target: str) -> bool:
    print(DISCLAIMER)
    print(f"Target: {target}\n")
    answer = input("Type 'I CONFIRM' (exact, case-sensitive) to proceed: ").strip()
    return answer == "I CONFIRM"
