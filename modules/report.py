"""
report.py — VulnScout cinematic HTML + JSON report writer.

Generates a fully animated HTML report with:
  - Canvas particle network background
  - SVG animated risk gauge
  - Severity badge counters with count-up animation
  - Glassmorphism module cards with slide-in transitions
  - Expandable findings accordion
  - Risk heatmap for open ports
  - Print-freeze mode (animations pause on print)
"""

import json
import os
import html as html_lib


# ── HTML template ─────────────────────────────────────────────────────────────
_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VulnScout Report — {target}</title>
<meta name="description" content="VulnScout security surface scan report for {target}">
<style>
/* ── Reset & base ─────────────────────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:          #050b14;
  --surface:     rgba(12, 22, 40, 0.82);
  --surface2:    rgba(18, 32, 58, 0.9);
  --border:      rgba(0, 210, 255, 0.18);
  --border2:     rgba(0, 210, 255, 0.08);
  --accent:      #00d2ff;
  --accent2:     #7b2fff;
  --accent3:     #ff6b35;
  --text:        #c9d8e8;
  --text-muted:  #5a7a99;
  --critical:    #ff3b5c;
  --high:        #ff7b35;
  --medium:      #ffcc00;
  --low:         #3b82f6;
  --info:        #64748b;
  --ok:          #22c55e;
  --radius:      14px;
  --shadow:      0 8px 32px rgba(0,0,0,0.5);
  --glow:        0 0 20px rgba(0,210,255,0.15);
}}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
  line-height: 1.6;
}}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{
  background: rgba(0,210,255,0.08);
  border: 1px solid var(--border);
  padding: 2px 7px;
  border-radius: 5px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.85em;
  color: var(--accent);
}}

/* ── Canvas background ────────────────────────────────────────────────────── */
#particle-canvas {{
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
}}

/* ── Layout ───────────────────────────────────────────────────────────────── */
.page-wrapper {{
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}}

/* ── Header ───────────────────────────────────────────────────────────────── */
.report-header {{
  text-align: center;
  padding: 3rem 2rem 2.5rem;
  margin-bottom: 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow), var(--glow);
  backdrop-filter: blur(12px);
  animation: slideDown 0.7s ease both;
}}
.logo-text {{
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -1px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 60%, var(--accent3) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}}
.report-header h2 {{
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--text-muted);
  margin-top: 0.4rem;
  letter-spacing: 0.05em;
}}
.meta-bar {{
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}}
.meta-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}}
.meta-item .label {{
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
}}
.meta-item .value {{
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--accent);
}}

/* ── Risk gauge ───────────────────────────────────────────────────────────── */
.gauge-section {{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(12px);
  animation: fadeUp 0.8s 0.2s ease both;
  box-shadow: var(--shadow);
}}
.gauge-wrap {{ text-align: center; }}
.gauge-wrap h3 {{
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
  margin-bottom: 0.8rem;
}}
.gauge-svg {{ filter: drop-shadow(0 0 12px rgba(0,210,255,0.3)); }}

/* ── Severity counter cards ───────────────────────────────────────────────── */
.severity-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
  animation: fadeUp 0.8s 0.35s ease both;
}}
.sev-card {{
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 1.2rem 1rem;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: default;
}}
.sev-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}}
.sev-card .sev-count {{
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.3rem;
}}
.sev-card .sev-label {{
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}}
.sev-card.critical  {{ border-color: rgba(255,59,92,0.4);  }}
.sev-card.high      {{ border-color: rgba(255,123,53,0.4); }}
.sev-card.medium    {{ border-color: rgba(255,204,0,0.35); }}
.sev-card.low       {{ border-color: rgba(59,130,246,0.4); }}
.sev-card.info      {{ border-color: rgba(100,116,139,0.4);}}
.sev-card.critical .sev-count {{ color: var(--critical); }}
.sev-card.high      .sev-count {{ color: var(--high);     }}
.sev-card.medium    .sev-count {{ color: var(--medium);   }}
.sev-card.low       .sev-count {{ color: var(--low);      }}
.sev-card.info      .sev-count {{ color: var(--info);     }}

/* ── Section heading ──────────────────────────────────────────────────────── */
.section-title {{
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-muted);
  margin: 2.5rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}}
.section-title::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}}

/* ── Module cards ─────────────────────────────────────────────────────────── */
.module-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 1.2rem;
  overflow: hidden;
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
  animation: slideIn 0.5s ease both;
  transition: box-shadow 0.2s;
}}
.module-card:hover {{
  box-shadow: var(--shadow), 0 0 30px rgba(0,210,255,0.08);
}}
.module-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.4rem;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid transparent;
  transition: background 0.2s, border-color 0.2s;
  gap: 1rem;
}}
.module-header:hover {{ background: rgba(0,210,255,0.04); border-color: var(--border); }}
.module-title {{
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex: 1;
}}
.module-title .icon {{ font-size: 1.1rem; }}
.module-badges {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}}
.badge {{
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 2px 8px;
  border-radius: 20px;
  border: 1px solid currentColor;
}}
.badge.critical {{ color: var(--critical); }}
.badge.high     {{ color: var(--high);     }}
.badge.medium   {{ color: var(--medium);   }}
.badge.low      {{ color: var(--low);      }}
.badge.info     {{ color: var(--info);     }}
.badge.ok       {{ color: var(--ok);       }}
.chevron {{
  color: var(--text-muted);
  transition: transform 0.3s;
  font-size: 0.85rem;
  flex-shrink: 0;
}}
.chevron.open {{ transform: rotate(180deg); }}
.module-body {{
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.45s cubic-bezier(0.4,0,0.2,1);
}}
.module-body.open {{ max-height: 3000px; }}
.module-content {{ padding: 1.2rem 1.4rem 1.4rem; }}

/* ── Tables ───────────────────────────────────────────────────────────────── */
.data-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
  margin-top: 0.8rem;
}}
.data-table th {{
  text-align: left;
  padding: 0.5rem 0.75rem;
  color: var(--accent);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid var(--border);
  font-weight: 700;
}}
.data-table td {{
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border2);
  vertical-align: top;
  color: var(--text);
}}
.data-table tr:last-child td {{ border-bottom: none; }}
.data-table tr:hover td {{ background: rgba(0,210,255,0.03); }}
.warn {{ color: var(--high); }}
.ok-text {{ color: var(--ok); }}
.critical-text {{ color: var(--critical); font-weight: 700; }}

/* ── Finding rows ─────────────────────────────────────────────────────────── */
.finding-row {{
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border2);
  font-size: 0.875rem;
}}
.finding-row:last-child {{ border-bottom: none; }}
.finding-sev {{
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 7px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.finding-sev.critical {{ background: rgba(255,59,92,0.15);  color: var(--critical); }}
.finding-sev.high     {{ background: rgba(255,123,53,0.15); color: var(--high);     }}
.finding-sev.medium   {{ background: rgba(255,204,0,0.12);  color: var(--medium);   }}
.finding-sev.low      {{ background: rgba(59,130,246,0.12); color: var(--low);      }}
.finding-sev.info     {{ background: rgba(100,116,139,0.12);color: var(--info);     }}
.finding-msg {{ flex: 1; }}
.finding-link {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem; }}

/* ── Port heatmap ─────────────────────────────────────────────────────────── */
.port-grid {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.8rem;
}}
.port-chip {{
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-family: 'JetBrains Mono', monospace;
  border: 1px solid var(--border);
  transition: transform 0.15s;
}}
.port-chip:hover {{ transform: scale(1.05); }}
.port-chip.danger {{ border-color: rgba(255,59,92,0.5);  background: rgba(255,59,92,0.1);  color: var(--critical); }}
.port-chip.warn   {{ border-color: rgba(255,123,53,0.5); background: rgba(255,123,53,0.1); color: var(--high);     }}
.port-chip.safe   {{ border-color: rgba(34,197,94,0.4);  background: rgba(34,197,94,0.08); color: var(--ok);       }}

/* ── Progress bar ─────────────────────────────────────────────────────────── */
.progress-bar-wrap {{
  height: 6px;
  background: rgba(0,210,255,0.08);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 0.5rem;
}}
.progress-bar-fill {{
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  width: 0%;
  transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
}}

/* ── SAN pills ────────────────────────────────────────────────────────────── */
.san-list {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.6rem;
}}
.san-pill {{
  padding: 2px 8px;
  background: rgba(0,210,255,0.07);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}}

/* ── Empty state ──────────────────────────────────────────────────────────── */
.empty-state {{
  color: var(--ok);
  padding: 0.6rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}}

/* ── Footer ───────────────────────────────────────────────────────────────── */
.report-footer {{
  text-align: center;
  padding: 2rem;
  color: var(--text-muted);
  font-size: 0.8rem;
  border-top: 1px solid var(--border2);
  margin-top: 3rem;
}}

/* ── Animations ───────────────────────────────────────────────────────────── */
@keyframes slideDown {{
  from {{ opacity:0; transform: translateY(-30px); }}
  to   {{ opacity:1; transform: translateY(0);     }}
}}
@keyframes fadeUp {{
  from {{ opacity:0; transform: translateY(20px); }}
  to   {{ opacity:1; transform: translateY(0);    }}
}}
@keyframes slideIn {{
  from {{ opacity:0; transform: translateX(-15px); }}
  to   {{ opacity:1; transform: translateX(0);     }}
}}
@keyframes countUp {{
  from {{ opacity:0; transform: scale(0.7); }}
  to   {{ opacity:1; transform: scale(1);   }}
}}
@keyframes glowPulse {{
  0%, 100% {{ box-shadow: var(--shadow), 0 0 20px rgba(0,210,255,0.1); }}
  50%       {{ box-shadow: var(--shadow), 0 0 40px rgba(0,210,255,0.25); }}
}}
.module-card:nth-child(1)  {{ animation-delay: 0.05s; }}
.module-card:nth-child(2)  {{ animation-delay: 0.10s; }}
.module-card:nth-child(3)  {{ animation-delay: 0.15s; }}
.module-card:nth-child(4)  {{ animation-delay: 0.20s; }}
.module-card:nth-child(5)  {{ animation-delay: 0.25s; }}
.module-card:nth-child(6)  {{ animation-delay: 0.30s; }}
.module-card:nth-child(7)  {{ animation-delay: 0.35s; }}
.module-card:nth-child(8)  {{ animation-delay: 0.40s; }}
.module-card:nth-child(9)  {{ animation-delay: 0.45s; }}
.module-card:nth-child(10) {{ animation-delay: 0.50s; }}
.module-card:nth-child(11) {{ animation-delay: 0.55s; }}
.module-card:nth-child(12) {{ animation-delay: 0.60s; }}

/* ── Print ────────────────────────────────────────────────────────────────── */
@media print {{
  #particle-canvas {{ display: none; }}
  .module-body {{ max-height: none !important; }}
  .module-card {{ box-shadow: none; border-color: #ccc; background: #fff; }}
  body {{ background: #fff; color: #111; }}
  .logo-text {{ -webkit-text-fill-color: #111; }}
}}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>

<canvas id="particle-canvas"></canvas>

<div class="page-wrapper">

  <!-- Header -->
  <div class="report-header">
    <div class="logo-text">VulnScout</div>
    <h2>Security Surface Scan Report</h2>
    <div class="meta-bar">
      <div class="meta-item"><span class="label">Target</span><span class="value" id="meta-target">{target}</span></div>
      <div class="meta-item"><span class="label">Generated</span><span class="value">{timestamp}</span></div>
      <div class="meta-item"><span class="label">Version</span><span class="value">v{version}</span></div>
      <div class="meta-item"><span class="label">Risk Score</span><span class="value" id="meta-risk">{risk_score}/100</span></div>
    </div>
  </div>

  <!-- Risk gauge + severity counters -->
  <div class="gauge-section">
    <div class="gauge-wrap">
      <h3>Overall Risk Score</h3>
      <svg class="gauge-svg" width="180" height="100" viewBox="0 0 180 100">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%"   stop-color="#22c55e"/>
            <stop offset="40%"  stop-color="#ffcc00"/>
            <stop offset="75%"  stop-color="#ff7b35"/>
            <stop offset="100%" stop-color="#ff3b5c"/>
          </linearGradient>
        </defs>
        <!-- Track -->
        <path d="M 20 90 A 70 70 0 0 1 160 90" fill="none" stroke="rgba(0,210,255,0.12)" stroke-width="12" stroke-linecap="round"/>
        <!-- Fill -->
        <path id="gauge-fill" d="M 20 90 A 70 70 0 0 1 160 90" fill="none"
              stroke="url(#gaugeGrad)" stroke-width="12" stroke-linecap="round"
              stroke-dasharray="220" stroke-dashoffset="220"
              style="transition: stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1);"/>
        <!-- Needle -->
        <line id="gauge-needle" x1="90" y1="90" x2="90" y2="30"
              stroke="#00d2ff" stroke-width="2" stroke-linecap="round"
              style="transform-origin:90px 90px; transform:rotate(-90deg);
                     transition: transform 1.5s cubic-bezier(0.4,0,0.2,1);"/>
        <circle cx="90" cy="90" r="5" fill="#00d2ff"/>
        <!-- Score text -->
        <text id="gauge-text" x="90" y="80" text-anchor="middle"
              font-size="22" font-weight="800" fill="#c9d8e8">0</text>
      </svg>
    </div>
    <div class="severity-grid" style="margin:0; flex:1; animation:none;">
      {severity_cards}
    </div>
  </div>

  <!-- Module results -->
  <div class="section-title">◈ &nbsp; Scan Results</div>
  {module_cards}

  <div class="report-footer">
    Generated by <strong>VulnScout v{version}</strong> — for authorized security testing only.<br>
    <a href="https://github.com/shridhar3902/vulnscout" target="_blank">github.com/shridhar3902/vulnscout</a>
    &nbsp;|&nbsp; Built by Shridhar Vinayak Kirtane
  </div>
</div>

<!-- ── JavaScript ──────────────────────────────────────────────────────────── -->
<script>
// ── Particle network ─────────────────────────────────────────────────────────
(function() {{
  const canvas = document.getElementById('particle-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {{
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }}

  function Particle() {{
    this.x   = Math.random() * W;
    this.y   = Math.random() * H;
    this.vx  = (Math.random() - 0.5) * 0.35;
    this.vy  = (Math.random() - 0.5) * 0.35;
    this.r   = Math.random() * 1.8 + 0.6;
    this.a   = Math.random() * 0.5 + 0.15;
  }}

  function init() {{
    resize();
    const count = Math.floor((W * H) / 12000);
    particles = Array.from({{length: count}}, () => new Particle());
  }}

  function draw() {{
    ctx.clearRect(0, 0, W, H);
    // Lines between nearby particles
    for (let i = 0; i < particles.length; i++) {{
      for (let j = i + 1; j < particles.length; j++) {{
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 130) {{
          const alpha = (1 - dist / 130) * 0.25;
          ctx.strokeStyle = `rgba(0,210,255,${{alpha}})`;
          ctx.lineWidth = 0.6;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }}
      }}
      // Dots
      const p = particles[i];
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,210,255,${{p.a}})`;
      ctx.fill();
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
    }}
    requestAnimationFrame(draw);
  }}

  window.addEventListener('resize', init);
  init();
  draw();
}})();

// ── Risk gauge animation ──────────────────────────────────────────────────────
(function() {{
  const score = {risk_score};
  const fill   = document.getElementById('gauge-fill');
  const needle = document.getElementById('gauge-needle');
  const text   = document.getElementById('gauge-text');
  const maxDash = 220;

  setTimeout(() => {{
    const offset = maxDash - (maxDash * score / 100);
    fill.style.strokeDashoffset = offset;
    const deg = -90 + (score / 100) * 180;
    needle.style.transform = `rotate(${{deg}}deg)`;

    // Count-up animation
    let current = 0;
    const step = score / 50;
    const timer = setInterval(() => {{
      current = Math.min(current + step, score);
      text.textContent = Math.round(current);
      if (current >= score) clearInterval(timer);
    }}, 30);
  }}, 600);
}})();

// ── Severity counter count-up ─────────────────────────────────────────────────
document.querySelectorAll('.sev-count[data-target]').forEach(el => {{
  const target = parseInt(el.dataset.target, 10);
  if (target === 0) {{ el.textContent = '0'; return; }}
  let current = 0;
  const step = Math.max(1, Math.ceil(target / 30));
  const timer = setInterval(() => {{
    current = Math.min(current + step, target);
    el.textContent = current;
    if (current >= target) clearInterval(timer);
  }}, 40);
}});

// ── Accordion toggle ──────────────────────────────────────────────────────────
document.querySelectorAll('.module-header').forEach(header => {{
  header.addEventListener('click', () => {{
    const body    = header.nextElementSibling;
    const chevron = header.querySelector('.chevron');
    const isOpen  = body.classList.contains('open');
    body.classList.toggle('open', !isOpen);
    if (chevron) chevron.classList.toggle('open', !isOpen);
    // Animate progress bars inside
    if (!isOpen) {{
      body.querySelectorAll('.progress-bar-fill').forEach(bar => {{
        const pct = bar.dataset.pct || '0';
        setTimeout(() => {{ bar.style.width = pct + '%'; }}, 50);
      }});
    }}
  }});
}});

// Auto-open cards with findings
document.querySelectorAll('.module-card').forEach(card => {{
  const body = card.querySelector('.module-body');
  if (card.dataset.hasFindings === 'true') {{
    body.classList.add('open');
    const chevron = card.querySelector('.chevron');
    if (chevron) chevron.classList.add('open');
    // Trigger progress bars
    body.querySelectorAll('.progress-bar-fill').forEach(bar => {{
      const pct = bar.dataset.pct || '0';
      setTimeout(() => {{ bar.style.width = pct + '%'; }}, 800);
    }});
  }}
}});
</script>
</body>
</html>
"""


# ── Helpers ────────────────────────────────────────────────────────────────────
def _e(s) -> str:
    """HTML-escape a value."""
    return html_lib.escape(str(s)) if s is not None else "—"


def _badge(sev: str, text: str | None = None) -> str:
    s = sev.lower()
    t = _e(text or sev.upper())
    return f'<span class="badge {s}">{t}</span>'


def _finding_badge(sev: str) -> str:
    s = sev.lower()
    return f'<span class="finding-sev {s}">{s.upper()}</span>'


def _card(icon: str, title: str, content: str, findings: list, has_findings: bool = False) -> str:
    badges = ""
    if findings:
        counts: dict[str, int] = {}
        for f in findings:
            sev = f.get("severity", "info").lower()
            counts[sev] = counts.get(sev, 0) + 1
        for sev in ["critical", "high", "medium", "low", "info"]:
            if sev in counts:
                badges += _badge(sev, f"{counts[sev]} {sev}")
    else:
        badges = _badge("ok", "CLEAN")

    findings_html = ""
    if findings:
        findings_html = "<div style='margin-top:1rem;'>"
        for f in findings:
            sev  = f.get("severity", "info").lower()
            msg  = _e(f.get("msg", ""))
            link = f.get("advisory", "")
            link_html = f'<div class="finding-link"><a href="{_e(link)}" target="_blank">→ {_e(link)}</a></div>' if link else ""
            findings_html += f"""
            <div class="finding-row">
              {_finding_badge(sev)}
              <div class="finding-msg">{msg}{link_html}</div>
            </div>"""
        findings_html += "</div>"

    return f"""
<div class="module-card" data-has-findings="{'true' if has_findings else 'false'}">
  <div class="module-header">
    <div class="module-title"><span class="icon">{icon}</span> {_e(title)}</div>
    <div class="module-badges">{badges}</div>
    <span class="chevron">▾</span>
  </div>
  <div class="module-body">
    <div class="module-content">
      {content}
      {findings_html}
    </div>
  </div>
</div>"""


def _table(headers: list[str], rows: list[list]) -> str:
    if not rows:
        return '<div class="empty-state">✔ No items found</div>'
    th = "".join(f"<th>{_e(h)}</th>" for h in headers)
    td_rows = ""
    for row in rows:
        tds = "".join(f"<td>{_e(c)}</td>" for c in row)
        td_rows += f"<tr>{tds}</tr>"
    return f'<table class="data-table"><thead><tr>{th}</tr></thead><tbody>{td_rows}</tbody></table>'


def _progress(label: str, pct: float, value: str = "") -> str:
    pct = max(0, min(100, pct))
    return f"""
    <div style="margin-bottom:0.6rem;">
      <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;">
        <span>{_e(label)}</span><span style="color:var(--accent)">{_e(value)}</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" data-pct="{pct:.0f}"></div>
      </div>
    </div>"""


# ── Module renderers ───────────────────────────────────────────────────────────
def _render_subdomains(m: dict) -> str:
    subs = m.get("subdomains", [])
    count = m.get("count", len(subs))
    rows = [[s] for s in subs[:150]]
    extra = f"<p style='color:var(--text-muted);font-size:0.8rem;margin-top:0.5rem;'>Showing first 150 of {count}</p>" if count > 150 else ""
    content = f"<p style='margin-bottom:0.8rem;'><strong>{count}</strong> unique subdomains discovered via crt.sh (passive, CT logs)</p>"
    content += _table(["Subdomain"], rows)
    content += extra
    return _card("🌐", "Passive Subdomain Enumeration", content,
                 m.get("findings", []), has_findings=bool(subs))


def _render_tech(m: dict) -> str:
    detected = m.get("detected", [])
    content  = (
        _progress("Server Header",    100, m.get("server_header") or "—") +
        _progress("X-Powered-By",     100, m.get("powered_by")    or "—") +
        "<div style='margin-top:0.8rem;'><strong>Detected Technologies:</strong><br>"
    )
    if detected:
        content += "<div style='display:flex;flex-wrap:wrap;gap:0.4rem;margin-top:0.5rem;'>"
        for t in detected:
            content += f"<span class='san-pill'>{_e(t)}</span>"
        content += "</div>"
    else:
        content += "<span style='color:var(--text-muted)'>No signatures matched</span>"
    content += "</div>"
    return _card("🔬", "Technology Fingerprinting", content,
                 m.get("findings", []), has_findings=bool(detected))


def _render_headers(m: dict) -> str:
    missing = m.get("missing", [])
    present = m.get("present", {})
    m_rows  = [[f"<span class='warn'>{_e(x['header'])}</span>", _e(x['risk'])] for x in missing]
    p_rows  = [[f"<span class='ok-text'>{_e(k)}</span>", _e(v)] for k, v in present.items()]
    content = ""
    if missing:
        content += "<strong style='color:var(--high)'>Missing Headers:</strong>"
        content += _table(["Header", "Risk"], m_rows)
    if present:
        content += "<strong style='color:var(--ok);display:block;margin-top:1rem;'>Present Headers:</strong>"
        content += _table(["Header", "Value"], p_rows)
    if not missing and not present:
        content = '<div class="empty-state">✔ All security headers present</div>'
    return _card("🛡️", "HTTP Security Headers Audit", content,
                 m.get("findings", []), has_findings=bool(missing))


def _render_exposed(m: dict) -> str:
    findings_list = m.get("findings", [])
    if findings_list:
        rows = [[f"<span class='warn'>{_e(f['path'])}</span>",
                 str(f["status_code"]),
                 str(f["size_bytes"]) + " B"] for f in findings_list]
        content = _table(["Path", "Status", "Size"], rows)
    else:
        content = f'<div class="empty-state">✔ No exposed paths found (checked {m.get("checked",0)} paths)</div>'
    vuln_findings = [{"severity":"high","msg":f"Exposed: {f['path']} ({f['size_bytes']} bytes)"} for f in findings_list]
    return _card("📂", "Exposed Sensitive Files", content,
                 vuln_findings, has_findings=bool(findings_list))


def _render_ports(m: dict) -> str:
    ip        = m.get("resolved_ip", "—")
    open_ports = m.get("open_ports", [])
    DANGER_PORTS = {21,23,3389,5900,6379,27017,1521,9200,445,135,139}
    WARN_PORTS   = {22,3306,5432,1433,8080,8000}
    content = f"<p><strong>Resolved IP:</strong> <code>{_e(ip)}</code></p>"
    if open_ports:
        content += "<div class='port-grid' style='margin-top:0.8rem;'>"
        for p in open_ports:
            port = p["port"]
            cls  = "danger" if port in DANGER_PORTS else "warn" if port in WARN_PORTS else "safe"
            content += f"<span class='port-chip {cls}'>{port}/{_e(p['service'])}</span>"
        content += "</div>"
    else:
        content += '<div class="empty-state" style="margin-top:0.8rem;">✔ No open ports found</div>'
    findings = [{"severity":"high" if p["port"] in DANGER_PORTS else "medium","msg":f"Port {p['port']} open ({p['service']})"} for p in open_ports]
    return _card("🔌", "Port Scan", content, findings, has_findings=bool(open_ports))


def _render_reflected(m: dict) -> str:
    reflected = m.get("reflected", [])
    if reflected:
        rows = [[f"<span class='warn'>{_e(r['param'])}</span>", f"<code>{_e(r['url'])}</code>"] for r in reflected]
        content = _table(["Parameter", "Test URL"], rows)
        content += "<p style='margin-top:0.8rem;font-size:0.8rem;color:var(--text-muted);'>⚠ Manual verification required before claiming XSS.</p>"
    else:
        content = '<div class="empty-state">✔ No unescaped reflection detected</div>'
    findings = [{"severity":"medium","msg":f"Reflected param: {r['param']}"} for r in reflected]
    return _card("💉", "Reflected Parameters (XSS Surface)", content,
                 findings, has_findings=bool(reflected))


def _render_ssl(m: dict) -> str:
    days   = m.get("days_left")
    color  = "var(--critical)" if (days is not None and days < 14) else "var(--ok)"
    content = (
        _progress("Validity",    100, "✔ Valid" if m.get("valid") else "✘ EXPIRED") +
        _progress("Days left",   max(0, min(100, (days or 0) / 365 * 100)), f"{days}d" if days is not None else "—") +
        _progress("Expires",     100, m.get("expires") or "—") +
        _progress("Issuer",      100, m.get("issued_by") or "—") +
        _progress("TLS Version", 100, m.get("tls_version") or "—") +
        _progress("Cipher",      100, m.get("cipher") or "—") +
        _progress("Self-signed", 100, "⚠ YES" if m.get("self_signed") else "No")
    )
    sans = m.get("sans", [])
    if sans:
        content += "<strong style='font-size:0.8rem;'>Subject Alternative Names:</strong>"
        content += "<div class='san-list'>" + "".join(f"<span class='san-pill'>{_e(s)}</span>" for s in sans[:30]) + "</div>"
    return _card("🔒", "TLS/SSL Certificate Inspection", content,
                 m.get("findings", []), has_findings=bool(m.get("findings")))


def _render_cors(m: dict) -> str:
    findings = m.get("findings", [])
    probes   = m.get("probes", [])
    if probes:
        rows = [[_e(p.get("sent_origin",""))[:60], _e(p.get("acao","")), _e(p.get("acac","")), str(p.get("status",""))] for p in probes]
        content = _table(["Origin Sent", "ACAO", "ACAC", "Status"], rows)
    else:
        content = '<div class="empty-state">No probes data</div>'
    return _card("🌍", "CORS Misconfiguration Probe", content,
                 findings, has_findings=bool(findings))


def _render_waf(m: dict) -> str:
    wafs  = m.get("detected_wafs", [])
    content = ""
    if wafs:
        content += "<strong>Detected:</strong><div class='san-list'>" + "".join(f"<span class='san-pill'>{_e(w)}</span>" for w in wafs) + "</div>"
    else:
        content += "<p style='color:var(--text-muted)'>No WAF/CDN signatures matched.</p>"
    content += f"<p style='margin-top:0.8rem;font-size:0.85rem;'>Probe blocked: <strong>{'Yes' if m.get('probe_blocked') else 'No'}</strong></p>"
    return _card("🧱", "WAF / CDN Detection", content,
                 m.get("findings", []), has_findings=bool(wafs))


def _render_whois(m: dict) -> str:
    rows = [
        ["Registrar",    m.get("registrar")],
        ["Organisation", m.get("org")],
        ["Created",      m.get("created")],
        ["Expires",      m.get("expires")],
        ["Updated",      m.get("updated")],
        ["Days to Expiry", str(m.get("days_until_expiry", "—"))],
        ["Nameservers",  ", ".join(m.get("nameservers", []))],
        ["Status Flags", ", ".join(m.get("status_flags", []))],
    ]
    content = _table(["Field", "Value"], [[r[0], r[1]] for r in rows])
    return _card("📋", "WHOIS Domain Intelligence", content,
                 m.get("findings", []), has_findings=bool(m.get("findings")))


def _render_robots(m: dict) -> str:
    disallowed = m.get("disallowed", [])
    sensitive  = m.get("sensitive_paths", [])
    sitemap_urls = m.get("sitemap_urls", [])
    content = f"<p><strong>robots.txt:</strong> {'Found' if m.get('robots_found') else 'Not found'}  |  <strong>Sitemap:</strong> {'Found' if m.get('sitemap_found') else 'Not found'}</p>"
    if disallowed:
        rows = [[f"<span class='{'warn' if d['path'] in sensitive else ''}'>{ _e(d['path'])}</span>",
                 _e(d.get("agent","*"))] for d in disallowed[:50]]
        content += "<strong style='display:block;margin-top:0.8rem;'>Disallowed Paths:</strong>"
        content += _table(["Path", "User-Agent"], rows)
    if sitemap_urls:
        content += f"<strong style='display:block;margin-top:0.8rem;'>Sitemap URLs ({len(sitemap_urls)} listed):</strong>"
        content += _table(["URL"], [[u] for u in sitemap_urls[:30]])
    return _card("🤖", "robots.txt & Sitemap Surface", content,
                 m.get("findings", []), has_findings=bool(sensitive))


def _render_vuln_hints(m: dict) -> str:
    hints = m.get("hints", [])
    if hints:
        rows = [[h.get("cve",""), h.get("tech",""), h.get("severity","").upper(), h.get("desc",""),
                 f"<a href='{_e(h.get('advisory',''))}' target='_blank'>→</a>"] for h in hints[:60]]
        content = _table(["CVE / ID", "Technology", "Severity", "Description", "Advisory"], rows)
    else:
        content = '<div class="empty-state">✔ No CVE hints for detected technologies</div>'
    return _card("🧬", "CVE / Vulnerability Hints", content,
                 m.get("findings", []), has_findings=bool(hints))


# ── Severity counter cards ─────────────────────────────────────────────────────
def _severity_cards(results: dict) -> str:
    counts: dict[str, int] = {}
    for mod in results.get("modules", {}).values():
        if isinstance(mod, dict):
            for f in mod.get("findings", []):
                sev = f.get("severity", "info").lower()
                counts[sev] = counts.get(sev, 0) + 1

    html = ""
    for sev in ["critical", "high", "medium", "low", "info"]:
        n = counts.get(sev, 0)
        html += f"""
        <div class="sev-card {sev}">
          <div class="sev-count" data-target="{n}">0</div>
          <div class="sev-label">{sev.upper()}</div>
        </div>"""
    return html


# ── Main render ────────────────────────────────────────────────────────────────
_RENDERERS = {
    "subdomains":     _render_subdomains,
    "tech_fingerprint": _render_tech,
    "headers":        _render_headers,
    "exposed_files":  _render_exposed,
    "ports":          _render_ports,
    "reflected_params": _render_reflected,
    "ssl":            _render_ssl,
    "cors":           _render_cors,
    "waf":            _render_waf,
    "whois":          _render_whois,
    "robots":         _render_robots,
    "vuln_hints":     _render_vuln_hints,
}

_RENDER_ORDER = [
    "whois", "subdomains", "robots", "tech_fingerprint", "waf", "ssl",
    "headers", "cors", "exposed_files", "ports", "reflected_params", "vuln_hints",
]


def _render_modules(results: dict) -> str:
    modules = results.get("modules", {})
    parts   = []
    for key in _RENDER_ORDER:
        if key in modules:
            renderer = _RENDERERS.get(key)
            if renderer:
                parts.append(renderer(modules[key]))
    # Any extra modules not in the order list
    for key, data in modules.items():
        if key not in _RENDER_ORDER:
            parts.append(_card("📌", key.replace("_"," ").title(),
                               "<pre style='font-size:0.75rem;overflow-x:auto;'>" +
                               _e(json.dumps(data, indent=2)[:2000]) + "</pre>",
                               data.get("findings", []) if isinstance(data, dict) else []))
    return "".join(parts)


# ── Write ──────────────────────────────────────────────────────────────────────
def write(results: dict, out_base: str) -> tuple[str, str]:
    json_path = os.path.join("reports", f"{out_base}.json")
    html_path = os.path.join("reports", f"{out_base}.html")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    html = _HTML.format(
        target      = _e(results.get("target", "unknown")),
        timestamp   = _e(results.get("timestamp", "")),
        version     = _e(results.get("version",   "2.0")),
        risk_score  = results.get("risk_score", 0),
        severity_cards = _severity_cards(results),
        module_cards   = _render_modules(results),
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return json_path, html_path
