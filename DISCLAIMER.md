# Disclaimer & Authorized Use

VulnScout is a reconnaissance and vulnerability-surface mapping tool intended
**exclusively** for:

- Assets you personally own
- Targets explicitly in-scope under a bug bounty program you are enrolled in
  (e.g. HackerOne, Bugcrowd, Intigriti)
- Lab/training environments (TryHackMe, HackTheBox, DVWA, etc.)

## What this tool does NOT do

- It does not bypass authentication, exploit vulnerabilities, or modify data
  on the target.
- It does not perform automated exploitation of any kind — the reflected
  parameter module only flags *potential* XSS surface using a benign,
  non-executing canary string; it never injects a working payload.
- It will not run against a target unless you explicitly confirm
  authorization at runtime (or pass `--yes` for scripted runs where
  authorization has already been verified).

## Your responsibility

Running active reconnaissance (port scans, path enumeration) against a
system you are not authorized to test may violate the Computer Fraud and
Abuse Act (US), the Computer Misuse Act (UK), India's IT Act 2000, or
equivalent laws in your jurisdiction — even if no data is altered. You are
solely responsible for ensuring you have permission before scanning any
target. The author and contributors accept no liability for misuse of this
software.

If you are unsure whether a target is in scope, do not scan it.
