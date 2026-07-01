#!/usr/bin/env bash
# VulnScout v2 — Kali Linux / Debian / Ubuntu installer
set -e

CYAN='\033[96m'
GREEN='\033[92m'
RED='\033[91m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ██╗   ██╗██╗   ██╗██╗     ███╗   ██╗███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗"
echo "  ╚██╗ ██╔╝██║   ██║██║     ████╗  ██║██╔════╝██╔════╝██╔═══██╗██║   ██║╚══██╔══╝"
echo "   ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║███████║╚██████╗╚██████╔╝╚██████╔╝   ██║   "
echo "    ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝   ╚═╝   "
echo -e "${NC}"
echo -e "  VulnScout v2.0 Installer — github.com/shridhar3902/vulnscout"
echo ""

# Check Python version
PY=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
MAJOR=$(echo "$PY" | cut -d. -f1)
MINOR=$(echo "$PY" | cut -d. -f2)
if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]; }; then
    echo -e "${RED}[!] Python 3.10+ required. Found: $PY${NC}"
    exit 1
fi
echo -e "${GREEN}[+] Python $PY detected${NC}"

# Install dependencies
echo -e "${CYAN}[*] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt --break-system-packages --quiet 2>/dev/null \
  || pip3 install -r requirements.txt --quiet

echo -e "${CYAN}[*] Creating reports directory...${NC}"
mkdir -p reports

echo ""
echo -e "${GREEN}[+] VulnScout v2.0 installed successfully!${NC}"
echo ""
echo "  Usage:"
echo "    python3 vulnscout.py -d example.com --all"
echo "    python3 vulnscout.py --help"
echo ""
echo -e "${CYAN}  Happy hunting — responsibly! 🔍${NC}"
echo ""
