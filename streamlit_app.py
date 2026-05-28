"""
╔══════════════════════════════════════════════════════════════╗
║  HAPPY BIRTHDAY POOJA — v2 — Premium Cinematic Edition      ║
║  Python + Streamlit  |  Deployable on Streamlit Cloud        ║
╠══════════════════════════════════════════════════════════════╣
║  HOW TO PERSONALISE:                                         ║
║  • Search "# ⭐ REPLACE:" to swap photos / name / messages  ║
║  • Stage 2: edit  letters = list("POOJA")                   ║
║  • Stage 3: swap the picsum.photos URLs                      ║
║  • Stage 5: edit cake message in ph2 div                     ║
║  • Stage 7: edit subtext paragraph                           ║
╠══════════════════════════════════════════════════════════════╣
║  TO RUN:  streamlit run app.py                               ║
╚══════════════════════════════════════════════════════════════╝
"""

import base64
import json
import os
import streamlit as st
import streamlit.components.v1 as components

# ── Page config (must be first Streamlit call) ───────────────────
st.set_page_config(
    page_title="Happy Birthday Pooja ✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = 1

# ─────────────────────────────────────────────────────────────────
# HELPER — render raw HTML via st.iframe + base64 data URI
# (replaces deprecated st.components.v1.html)
# ─────────────────────────────────────────────────────────────────
def render_html(html: str, height: int = 5000, scrolling: bool = False) -> None:
  # Ensure every embedded page stays fixed to the frame and does not scroll.
  if '<style>' in html:
    html = html.replace('<style>', '<style>\nhtml,body{height:100%;overflow:hidden;}\n', 1)
  # Use Streamlit components to render raw HTML safely.
  # We intentionally set a very large height (5000) so Streamlit's iframe never
  # clips the content. The JS layout fixer injected in inject_global_styles()
  # will resize this iframe to exactly fill the available viewport space.
  try:
    components.html(html, height=height, scrolling=False)
  except Exception:
    # fallback to iframe data URI for very old Streamlit versions
    encoded = base64.b64encode(html.encode("utf-8")).decode("utf-8")
    st.components.v1.iframe(f"data:text/html;base64,{encoded}", height=height, scrolling=False)


def _path_to_data_uri(src: str) -> str:
    if not isinstance(src, str) or not src:
        return src
    normalized = src.strip()
    if normalized.startswith(('http://', 'https://', 'data:')):
        return normalized
    if normalized.startswith('file://'):
        normalized = normalized[7:]
    if not os.path.isabs(normalized):
        normalized = os.path.join(os.path.dirname(__file__), normalized)
    if not os.path.isfile(normalized):
        return src
    try:
        with open(normalized, 'rb') as fh:
            raw = fh.read()
        ext = os.path.splitext(normalized)[1].lower().lstrip('.')
        if ext == 'jpg':
            ext = 'jpeg'
        mime = f'image/{ext}' if ext else 'application/octet-stream'
        return f"data:{mime};base64,{base64.b64encode(raw).decode('utf-8')}"
    except Exception:
        return src

def _get_music_data_uri() -> str:
    music_path = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "birthday_music.mp3"
    )

    if not os.path.isfile(music_path):
        return ""

    try:
        with open(music_path, "rb") as fh:
            data = fh.read()

        encoded = base64.b64encode(data).decode()

        return f"data:audio/mpeg;base64,{encoded}"

    except Exception:
        return ""

# ─────────────────────────────────────────────────────────────────
# SHARED CONSTANTS — embedded into every stage
# ─────────────────────────────────────────────────────────────────

# Cinematic stage-entry animation (every stage fades+zooms in)
ENTRY_CSS = """
  @keyframes stageReveal {
    0%   { opacity:0; transform:scale(1.09) translateY(18px); filter:blur(14px); }
    100% { opacity:1; transform:scale(1)    translateY(0px);  filter:blur(0px);  }
  }
  .stage-root { animation: stageReveal 1.4s cubic-bezier(0.16,1,0.3,1) both; }
"""

# Light-beam sweep CSS
BEAM_CSS = """
  .beam {
    position:fixed; top:-20vh; width:110px; height:190vh;
    background:linear-gradient(to bottom,
      transparent 0%, rgba(139,92,246,.07) 30%,
      rgba(139,92,246,.13) 50%, rgba(59,130,246,.07) 70%, transparent 100%);
    transform-origin:top center; pointer-events:none; z-index:1;
    animation:beamSweep var(--dur,18s) linear var(--del,0s) infinite;
    filter:blur(9px);
  }
  @keyframes beamSweep {
    0%   { left:-15%; transform:skewX(-22deg); opacity:0; }
    8%   { opacity:1; }
    92%  { opacity:1; }
    100% { left:115%; transform:skewX(22deg);  opacity:0; }
  }
"""

# Glowing floating-particle canvas JS (shared across all stages)
PARTICLE_JS = r"""
(function initParticles() {
  var c   = document.getElementById('bgCvs');
  if (!c) return;
  var ctx = c.getContext('2d');
  c.width = window.innerWidth; c.height = window.innerHeight;
  window.addEventListener('resize', function () {
    c.width = window.innerWidth; c.height = window.innerHeight;
  });
  var COLS = [
    'rgba(139,92,246',  'rgba(59,130,246',
    'rgba(192,38,211',  'rgba(251,191,36',
    'rgba(167,139,250', 'rgba(96,165,250'
  ];
  function Pt() { this.reset(); }
  Pt.prototype.reset = function () {
    this.x  = Math.random() * c.width;
    this.y  = c.height + 10;
    this.sz = Math.random() * 3 + 0.4;
    this.sp = Math.random() * 1.1 + 0.2;
    this.op = Math.random() * 0.55 + 0.1;
    this.dx = (Math.random() - 0.5) * 0.55;
    this.cl = COLS[Math.floor(Math.random() * COLS.length)];
  };
  Pt.prototype.tick = function () {
    this.y -= this.sp; this.x += this.dx;
    if (this.y < -10) this.reset();
  };
  Pt.prototype.draw = function () {
    ctx.beginPath(); ctx.arc(this.x, this.y, this.sz, 0, Math.PI * 2);
    ctx.fillStyle = this.cl + ',' + this.op + ')'; ctx.fill();
    ctx.beginPath(); ctx.arc(this.x, this.y, this.sz * 3.2, 0, Math.PI * 2);
    ctx.fillStyle = this.cl + ',' + (this.op * 0.13) + ')'; ctx.fill();
  };
  var pts = [];
  for (var i = 0; i < 130; i++) {
    var p = new Pt(); p.y = Math.random() * c.height; pts.push(p);
  }
  (function loop() {
    ctx.clearRect(0, 0, c.width, c.height);
    pts.forEach(function (p) { p.tick(); p.draw(); });
    requestAnimationFrame(loop);
  })();
})();
"""

# Magic button CSS (ripple + spark + float + glow)
MAGIC_BTN_CSS = """
  .magic-btn {
    position:relative; border:none; border-radius:50px; cursor:pointer;
    font-family:'Cinzel',serif; font-weight:700; letter-spacing:3px;
    overflow:hidden; transition:all .38s cubic-bezier(.34,1.56,.64,1);
  }
  .magic-btn.gold {
    padding:17px 58px; font-size:17px;
    background:linear-gradient(135deg,#fbbf24,#f59e0b,#d97706); color:#030312;
    box-shadow:0 0 32px rgba(251,191,36,.55), 0 0 65px rgba(251,191,36,.2);
    animation:btnFloat 3s ease-in-out infinite;
  }
  .magic-btn.gold:hover {
    transform:scale(1.1) translateY(-6px);
    box-shadow:0 0 72px rgba(251,191,36,.95), 0 0 140px rgba(251,191,36,.4);
  }
  .magic-btn.violet {
    padding:17px 58px; font-size:17px;
    background:linear-gradient(135deg,#7c3aed,#2563eb,#9333ea); color:#fff;
    box-shadow:0 0 32px rgba(124,58,237,.55);
    animation:btnFloat 3s ease-in-out .5s infinite;
  }
  .magic-btn.violet:hover {
    transform:scale(1.1) translateY(-6px);
    box-shadow:0 0 72px rgba(124,58,237,.9), 0 0 140px rgba(37,99,235,.35);
  }
  @keyframes btnFloat {
    0%,100% { transform:translateY(0);   }
    50%      { transform:translateY(-7px); }
  }
  /* Ripple */
  .magic-btn::after {
    content:''; position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%) scale(0);
    width:320px; height:320px; border-radius:50%;
    background:rgba(255,255,255,.22); opacity:0;
  }
  .magic-btn.ripple::after {
    animation:rippleAnim .65s ease-out forwards;
  }
  @keyframes rippleAnim {
    0%   { transform:translate(-50%,-50%) scale(0); opacity:1; }
    100% { transform:translate(-50%,-50%) scale(1); opacity:0; }
  }
  /* Hover spark particle */
  .btn-spark {
    position:fixed; pointer-events:none; z-index:999; border-radius:50%;
    width:5px; height:5px;
    animation:sparkFly .6s ease-out forwards;
  }
  @keyframes sparkFly {
    0%   { transform:scale(1) translate(0,0);               opacity:1; }
    100% { transform:scale(0) translate(var(--tx),var(--ty)); opacity:0; }
  }
"""

# Ripple + spark JS (attach to any .magic-btn)
MAGIC_BTN_JS = r"""
(function () {
  document.querySelectorAll('.magic-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      this.classList.remove('ripple');
      void this.offsetWidth;
      this.classList.add('ripple');
      for (var i = 0; i < 12; i++) {
        var spark = document.createElement('div');
        spark.className = 'btn-spark';
        var angle = Math.random() * 360;
        var dist  = Math.random() * 70 + 20;
        var col   = Math.random() > 0.5 ? '#fbbf24' : '#a78bfa';
        spark.style.cssText =
          'left:' + (e.clientX - 3) + 'px;top:' + (e.clientY - 3) + 'px;' +
          '--tx:' + (Math.cos(angle * Math.PI / 180) * dist).toFixed(0) + 'px;' +
          '--ty:' + (Math.sin(angle * Math.PI / 180) * dist).toFixed(0) + 'px;' +
          'background:' + col + ';box-shadow:0 0 7px ' + col + ';' +
          'animation-duration:' + (Math.random() * 0.3 + 0.35) + 's;' +
          'animation-delay:'   + (i * 0.025) + 's;';
        document.body.appendChild(spark);
        setTimeout(function () { spark.remove(); }, 700);
      }
    });
  });
})();
"""


# ─────────────────────────────────────────────────────────────────
# GLOBAL STREAMLIT CSS
# ─────────────────────────────────────────────────────────────────
def inject_global_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400;1,700&family=Inter:wght@300;400;600&display=swap');

    #MainMenu, footer, header,
    [data-testid="stDeployButton"],
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"] { visibility:hidden!important; display:none!important; }

    html, body, .stApp, .stAppViewContainer {
      background:#030312!important;
      height:100vh!important;
      overflow:hidden!important;
      margin:0!important; padding:0!important;
    }

    /* Make the Streamlit block container fill 100vh as a flex column */
    .block-container {
      padding: 0 !important;
      max-width: 100% !important;
      height: 100vh !important;
      display: flex !important;
      flex-direction: column !important;
      overflow: hidden !important;
    }

    /* Root vertical block — full height flex column, no gaps */
    div[data-testid="stVerticalBlock"]:not(div[data-testid="column"] div[data-testid="stVerticalBlock"]) {
      height: 100vh !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 0px !important;
      overflow: hidden !important;
    }
    div[data-testid="stVerticalBlock"]:not(div[data-testid="column"] div[data-testid="stVerticalBlock"]) > div {
      margin: 0 !important;
      padding: 0 !important;
    }

    /* The element-container that wraps the main stage iframe grows to fill all remaining space */
    div[data-testid="element-container"]:has(> div > iframe:not([style*="display: none"])) {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      overflow: hidden !important;
    }
    div[data-testid="element-container"]:has(> div > iframe:not([style*="display: none"])) > div {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
    }

    /* All iframes fill their container; JS will override height on the stage one */
    iframe {
      width: 100% !important;
      border: none !important;
      display: block !important;
    }

    /* Progress strip */
    .pg-strip {
      display:flex; justify-content:center; align-items:center;
      gap:10px; padding:10px 20px 8px;
      background:rgba(3,3,18,.98);
      border-bottom:1px solid rgba(139,92,246,.14);
      flex-shrink: 0;
    }
    .pg-dot {
      width:9px; height:9px; border-radius:50%;
      background:rgba(255,255,255,.1);
      transition:all .4s ease; cursor:default;
    }
    .pg-dot.done { background:#fbbf24; box-shadow:0 0 8px #fbbf24; }
    .pg-dot.live { background:#8b5cf6; box-shadow:0 0 15px #8b5cf6; transform:scale(1.55); }

    /* Nav Streamlit buttons */
    .stButton > button {
      background:linear-gradient(135deg,#7c3aed 0%,#2563eb 55%,#9333ea 100%)!important;
      color:#fff!important; border:1px solid rgba(139,92,246,.35)!important;
      border-radius:50px!important; padding:14px 52px!important;
      font-family:'Cinzel',serif!important; font-size:15px!important;
      font-weight:700!important; letter-spacing:3px!important;
      text-transform:uppercase!important;
      transition:all .4s cubic-bezier(.175,.885,.32,1.275)!important;
      box-shadow:0 0 28px rgba(124,58,237,.45)!important;
    }
    .stButton > button:hover {
      transform:translateY(-5px) scale(1.08)!important;
      box-shadow:0 0 72px rgba(124,58,237,.9), 0 0 135px rgba(37,99,235,.3)!important;
    }
    .stButton > button:active { transform:translateY(-1px) scale(1.02)!important; }
    div[data-testid="stHorizontalBlock"] {
      padding:0!important; gap:0!important;
      background:rgba(3,3,18,.98)!important;
      border-top:1px solid rgba(139,92,246,.12)!important;
      flex-shrink:0!important;
    }
    /* Kill any extra space Streamlit adds after the nav row */
    div[data-testid="stHorizontalBlock"] ~ div,
    div[data-testid="stHorizontalBlock"] + div { display:none!important; }
    /* Ensure nothing overflows the viewport */
    * { max-height: 100vh; }
    .stApp, .block-container,
    div[data-testid="stVerticalBlock"]:not(div[data-testid="column"] div[data-testid="stVerticalBlock"]) {
      max-height: 100vh !important;
    }
    </style>

    <script>
    /* ── Fullscreen Layout Fixer ──────────────────────────────────────────────
       Streamlit sets an inline style height on every iframe it creates, which
       CSS alone cannot override. This script directly measures what height the
       stage iframe SHOULD be (viewport minus progress bar + nav bar) and applies
       it as an inline style, overriding Streamlit's value.
       A MutationObserver re-runs the layout whenever Streamlit re-renders.
    ─────────────────────────────────────────────────────────────────────────── */
    (function() {
      'use strict';

      function applyLayout() {
        try {
          var vh = window.innerHeight;

          /* ── measure chrome elements ── */
          var pgStrip = document.querySelector('.pg-strip');
          var pgH = pgStrip ? pgStrip.getBoundingClientRect().height : 0;

          /* Nav bar: the stHorizontalBlock that contains Prev/Next buttons */
          var navH = 0;
          document.querySelectorAll('[data-testid="stHorizontalBlock"]').forEach(function(el) {
            var h = el.getBoundingClientRect().height;
            if (h > navH) navH = h;
          });

          /* ── available height for the stage iframe ── */
          var availH = Math.max(200, vh - pgH - navH);

          /* ── find the main stage iframe (visible, non-zero, not the music one) ── */
          var iframes = document.querySelectorAll('iframe');
          var stageFrame = null;
          iframes.forEach(function(f) {
            if (f.id === 'globalBgAudio') return;
            if (f.style.display === 'none') return;
            if (f.offsetWidth === 0) return;  /* hidden music frame */
            /* The largest visible iframe is the stage */
            if (!stageFrame || f.offsetWidth > stageFrame.offsetWidth) {
              stageFrame = f;
            }
          });

          if (stageFrame) {
            stageFrame.style.setProperty('height', availH + 'px', 'important');
            stageFrame.style.setProperty('min-height', availH + 'px', 'important');
            stageFrame.style.setProperty('max-height', availH + 'px', 'important');
            /* Also fix its wrapper containers */
            var wrapper = stageFrame.parentElement;
            while (wrapper && wrapper !== document.body) {
              if (wrapper.dataset && wrapper.dataset.testid === 'stVerticalBlock') break;
              wrapper.style.setProperty('height', availH + 'px', 'important');
              wrapper.style.setProperty('min-height', '0', 'important');
              wrapper.style.setProperty('overflow', 'hidden', 'important');
              wrapper = wrapper.parentElement;
            }
          }
        } catch(e) { console.warn('Layout fixer:', e); }
      }

      /* Run now and after brief delays to catch Streamlit's late renders */
      applyLayout();
      setTimeout(applyLayout, 100);
      setTimeout(applyLayout, 400);
      setTimeout(applyLayout, 900);

      /* Re-run on every window resize */
      window.addEventListener('resize', applyLayout);

      /* Watch for Streamlit DOM mutations (reruns) and re-apply layout */
      var observer = new MutationObserver(function(mutations) {
        var hasFrameChange = mutations.some(function(m) {
          return Array.from(m.addedNodes).some(function(n) {
            return n.nodeType === 1 && (n.tagName === 'IFRAME' || n.querySelector && n.querySelector('iframe'));
          });
        });
        if (hasFrameChange) {
          setTimeout(applyLayout, 80);
          setTimeout(applyLayout, 350);
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });

    })();
    </script>
    """, unsafe_allow_html=True)


def show_progress(current: int, total: int = 4) -> None:
    names = {1:"Welcome",2:"The Reveal",3:"Gallery",
             4:"Celebration"}
    dots = "".join(
        f'<div class="pg-dot {"live" if i==current else "done" if i<current else ""}"></div>'
        for i in range(1, total + 1)
    )
    st.markdown(f"""
    <div class="pg-strip">
      {dots}
      <span style="color:rgba(255,255,255,.28);font-family:'Inter',sans-serif;
                   font-size:11px;letter-spacing:4px;margin-left:14px;">
        {names.get(current,"")}
      </span>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# STAGE 1 — CINEMATIC WELCOME
# ═══════════════════════════════════════════════════════════════
def stage_1() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@1,400&family=Inter:wght@300;400&display=swap');
{ENTRY_CSS} {BEAM_CSS} {MAGIC_BTN_CSS}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#030312;min-height:100vh;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}}
.blob{{position:fixed;border-radius:50%;filter:blur(95px);pointer-events:none;z-index:1;
  animation:blobAnim ease-in-out infinite alternate;}}
@keyframes blobAnim{{0%{{transform:scale(1) translate(0,0);opacity:.55;}}
  100%{{transform:scale(1.2) translate(26px,-24px);opacity:.9;}}}}
.star{{position:fixed;background:#fff;border-radius:50%;animation:tw ease-in-out infinite;z-index:1;}}
@keyframes tw{{0%,100%{{opacity:.06;transform:scale(1);}}50%{{opacity:.95;transform:scale(1.7);}}}}
.wrap{{position:relative;z-index:10;text-align:center;padding:clamp(10px, 3.5vh, 32px) 24px;}}
.eyebrow{{font-family:'Cinzel',serif;font-size:12px;letter-spacing:11px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(8px, 2.2vh, 20px);animation:fadeUp 1s ease .5s both;opacity:0;}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(24px);}}to{{opacity:1;transform:translateY(0);}}}}
.title{{font-family:'Cinzel Decorative',serif;font-size:clamp(22px,6.8vh,48px);
  font-weight:900;line-height:1.2;
  background:linear-gradient(135deg,#f0eaff,#c4b5fd,#818cf8,#60a5fa,#a78bfa);
  background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;filter:drop-shadow(0 0 42px rgba(139,92,246,.8));
  animation:fadeUp 1s ease .8s both,titleSh 5s linear 2s infinite;opacity:0;margin-bottom:clamp(8px, 1.8vh, 18px);}}
@keyframes titleSh{{from{{background-position:0% center;}}to{{background-position:300% center;}}}}
.divider{{width:180px;height:1px;
  background:linear-gradient(90deg,transparent,#8b5cf6,#fbbf24,#3b82f6,transparent);
  margin:clamp(8px, 2vh, 16px) auto;animation:fadeUp 1s ease 1.1s both;opacity:0;}}
.subtitle{{font-family:'Playfair Display',serif;font-style:italic;
  font-size:clamp(13px,2.2vh,18px);color:rgba(196,181,253,.85);
  margin-bottom:clamp(20px, 4vh, 40px);animation:fadeUp 1s ease 1.3s both;opacity:0;}}
.ring{{position:absolute;border-radius:50%;border:1px solid rgba(139,92,246,.22);
  top:50%;left:50%;transform:translate(-50%,-50%);
  animation:ringEx 4s ease-out infinite;pointer-events:none;}}
@keyframes ringEx{{0%{{width:0;height:0;opacity:.9;}}100%{{width:550px;height:550px;opacity:0;}}}}
.music-badge{{
  position:fixed;top:16px;right:20px;z-index:50;
  display:flex;align-items:center;gap:8px;
  background:rgba(139,92,246,.22);backdrop-filter:blur(18px);
  border:1px solid rgba(139,92,246,.55);border-radius:30px;
  padding:8px 18px;
  font-family:'Cinzel',serif;font-size:11px;letter-spacing:3px;
  color:rgba(196,181,253,.95);
  animation:fadeUp 1s ease 2.2s both,badgeGlow 2.5s ease-in-out 3s infinite alternate;opacity:0;
  pointer-events:none;}}
@keyframes badgeGlow{{
  0%{{box-shadow:0 0 10px rgba(139,92,246,.4);border-color:rgba(139,92,246,.4);}}
  100%{{box-shadow:0 0 28px rgba(139,92,246,.85),0 0 50px rgba(192,38,211,.4);border-color:rgba(192,38,211,.7);}}}}
.music-icon{{font-size:16px;animation:mBob .7s ease-in-out infinite alternate;}}
@keyframes mBob{{from{{transform:scale(1);}}to{{transform:scale(1.3) rotate(15deg);}}}}
.scroll-hint{{display:none;}}
</style></head><body>
<canvas id="bgCvs"></canvas>
<div class="blob" style="width:420px;height:420px;background:rgba(76,29,149,.4);top:0%;left:0%;animation-duration:11s;"></div>
<div class="blob" style="width:330px;height:330px;background:rgba(30,64,175,.36);top:42%;right:1%;animation-duration:14s;animation-delay:-5s;"></div>
<div class="blob" style="width:270px;height:270px;background:rgba(192,38,211,.28);bottom:4%;left:18%;animation-duration:9s;animation-delay:-3s;"></div>
<div class="blob" style="width:210px;height:210px;background:rgba(251,191,36,.14);top:10%;right:20%;animation-duration:17s;animation-delay:-9s;"></div>
<div id="stars"></div>
<div class="beam" style="--dur:17s;--del:0s;"></div>
<div class="beam" style="--dur:23s;--del:-8s;background:linear-gradient(to bottom,transparent,rgba(59,130,246,.09),rgba(59,130,246,.15),rgba(59,130,246,.09),transparent);"></div>
<div class="beam" style="--dur:20s;--del:-13s;background:linear-gradient(to bottom,transparent,rgba(251,191,36,.05),rgba(251,191,36,.11),rgba(251,191,36,.05),transparent);"></div>
<div class="ring" style="animation-delay:0s;"></div>
<div class="ring" style="animation-delay:1.4s;"></div>
<div class="ring" style="animation-delay:2.8s;"></div>
<div class="music-badge" id="musicBadge">
  <span class="music-icon">♫</span>
  <span>Music On</span>
</div>
<div class="stage-root wrap">
  <p class="eyebrow">✦ &nbsp; A Surprise Awaits &nbsp; ✦</p>
  <h1 class="title">Happy Birthday<br>To The Prettiest Soul With The Warmest Smile</h1>
  <div class="divider"></div>
  <p class="subtitle">An experience crafted with warmth, wonder &amp; pure joy</p>
</div>
<script>
{PARTICLE_JS}
(function(){{
  var c=document.getElementById('stars');
  for(var i=0;i<170;i++){{
    var s=document.createElement('div'); s.className='star';
    var sz=Math.random()*2.8+.3;
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;top:'+Math.random()*100+'%;left:'+Math.random()*100+'%;animation-duration:'+(Math.random()*4+2)+'s;animation-delay:'+(Math.random()*5)+'s;';
    c.appendChild(s);
  }}
}})();
(function(){{
  try {{
    var parentDoc = window.parent.document;
    var a = parentDoc ? parentDoc.getElementById('globalBgAudio') : null;
    var badge = document.getElementById('musicBadge');
    var ic = document.getElementById('mIcon'), lb = document.getElementById('mLabel');
    if (!badge || !a) return;
    
    function updateBadge() {{
      if (a.paused) {{
        ic.textContent = '♪';
        lb.textContent = 'Music Off';
        badge.style.background = 'rgba(255,255,255,.05)';
      }} else {{
        ic.textContent = '♫';
        lb.textContent = 'Music On';
        badge.style.background = 'rgba(139,92,246,.18)';
      }}
    }}
    
    updateBadge();
    var intv = setInterval(updateBadge, 400);
    
    window.toggleMusic = function() {{
      if (a.paused) {{
        a.play().then(function() {{
          localStorage.setItem('bgMusicPlaying_v1', '1');
          updateBadge();
          var pBtn = parentDoc.getElementById('musicEnableBtn');
          if (pBtn) pBtn.remove();
        }}).catch(function(err){{}});
      }} else {{
        a.pause();
        localStorage.setItem('bgMusicPlaying_v1', '0');
        updateBadge();
      }}
    }};
    
    window.addEventListener('unload', function() {{
      clearInterval(intv);
    }});
  }} catch(e) {{
    console.error("Badge sync error:", e);
  }}
}})();
{MAGIC_BTN_JS}
</script>
</body></html>"""
    render_html(html, height=600, scrolling=False)


# ═══════════════════════════════════════════════════════════════
# STAGE 2 — NAME REVEAL (enhanced: streaks, sparks, zoom-out)
# ═══════════════════════════════════════════════════════════════
def stage_2() -> None:
    # ⭐ REPLACE: Change "POOJA" and update colours list to match length
    letters  = list("POOJA")
    colours  = ["#e879f9", "#c084fc", "#818cf8", "#60a5fa", "#a78bfa"]
    ltrs_html = "".join(
        f'<span class="ltr" data-h="{i}" style="--gc:{colours[i % len(colours)]};--del:{0.2 + i*0.32}s">{ch}</span>'
        for i, ch in enumerate(letters)
    )

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@900&family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@1,400;1,700&display=swap');
{ENTRY_CSS}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#030312;min-height:100vh;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}}
.wrap{{position:relative;z-index:10;text-align:center;padding:12px 20px;}}
.eyebrow{{font-family:'Cinzel',serif;font-size:11px;letter-spacing:10px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(12px, 3.5vh, 36px);animation:fu .8s ease .2s both;opacity:0;}}
@keyframes fu{{from{{opacity:0;transform:translateY(22px);}}to{{opacity:1;transform:translateY(0);}}}}
.name-row{{display:flex;justify-content:center;align-items:center;
  gap:clamp(3px,1.5vw,18px);margin-bottom:clamp(8px, 2.5vh, 24px);
  animation:nameZoom 1.2s ease 2.8s both;}}
@keyframes nameZoom{{from{{transform:scale(1.35);}}to{{transform:scale(1);}}}}
/* Letter */
.ltr{{
  font-family:'Cinzel Decorative',serif;
  font-size:clamp(40px,11vh,100px);font-weight:900;
  color:var(--gc);display:inline-block;cursor:default;
  text-shadow:0 0 22px var(--gc),0 0 50px var(--gc),0 0 95px var(--gc);
  animation:ltrIn .95s cubic-bezier(.34,1.56,.64,1) var(--del) both,
            flicker 4s ease-in-out calc(var(--del) + 2.2s) infinite;
  opacity:0;position:relative;transition:transform .2s ease;
}}
.ltr:hover{{transform:scale(1.2) translateY(-10px);}}
/* Light streak that falls before letter appears */
.ltr::before{{
  content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:4px;height:0;background:linear-gradient(to bottom,var(--gc),transparent);
  opacity:0;border-radius:2px;animation:streak .45s ease var(--del) both;
}}
@keyframes streak{{
  0%  {{height:280px;top:-280px;opacity:.95;}}
  100%{{height:0;top:0;opacity:0;}}
}}
@keyframes ltrIn{{
  from{{opacity:0;transform:translateY(-100px) scale(.2) rotate(-18deg);filter:blur(22px);}}
  to  {{opacity:1;transform:translateY(0)      scale(1)  rotate(0deg);  filter:blur(0);  }}
}}
@keyframes flicker{{
  0%,90%,100%{{opacity:1;}}91%{{opacity:.6;}}93%{{opacity:1;}}97%{{opacity:.4;}}99%{{opacity:1;}}
}}
.divider{{width:240px;height:1px;
  background:linear-gradient(90deg,transparent,#8b5cf6,#fbbf24,#3b82f6,transparent);
  margin:clamp(8px, 2vh, 18px) auto clamp(12px, 3vh, 30px);animation:fu .8s ease 2.2s both;opacity:0;}}
.quote{{max-width:590px;margin:0 auto;animation:fu 1.2s ease 2.6s both;opacity:0;}}
.ql{{font-family:'Playfair Display',serif;font-style:italic;
  font-size:clamp(14px,2.5vh,22px);line-height:1.7;color:rgba(196,181,253,.9);padding:2px 0;}}
.ql.gold{{color:#fbbf24;font-size:clamp(16px,2.8vh,24px);}}
</style></head><body>
<canvas id="bgCvs"></canvas>
<div class="stage-root wrap">
  <p class="eyebrow">✦ &nbsp; The Reveal &nbsp; ✦</p>
  <div class="name-row">{ltrs_html}</div>
  <div class="divider"></div>
  <div class="quote">
    <p class="ql">"Some people carry beauty in their smile.</p>
    <p class="ql">Some carry it in their soul.</p>
    <p class="ql gold">You carry both."</p>
  </div>
</div>
<script>
{PARTICLE_JS}
(function(){{
  var c=document.getElementById('bgCvs'), ctx=c.getContext('2d');
  function burst(x,y,hue){{
    var pts=[];
    for(var i=0;i<70;i++){{
      var a=Math.random()*Math.PI*2, sp=Math.random()*11+3;
      pts.push({{x:x,y:y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,
        life:1,d:Math.random()*.024+.012,sz:Math.random()*3+1,
        h:hue+(Math.random()-.5)*50}});
    }}
    (function loop(){{
      pts=pts.filter(function(p){{return p.life>0;}});
      if(!pts.length)return;
      pts.forEach(function(p){{
        p.vx*=.95;p.vy*=.95;p.vy+=.08;p.x+=p.vx;p.y+=p.vy;p.life-=p.d;
        ctx.save();ctx.globalAlpha=p.life;
        ctx.beginPath();ctx.arc(p.x,p.y,p.sz,0,Math.PI*2);
        ctx.fillStyle='hsl('+p.h+',100%,70%)';
        ctx.shadowBlur=12;ctx.shadowColor='hsl('+p.h+',100%,62%)';
        ctx.fill();ctx.restore();
      }});
      requestAnimationFrame(loop);
    }})();
  }}
  document.querySelectorAll('.ltr').forEach(function(el){{
    var del=parseFloat(el.style.getPropertyValue('--del'))*1000;
    setTimeout(function(){{
      var r=el.getBoundingClientRect();
      burst(r.left+r.width/2, r.top+r.height/2, 270);
    }}, del+700);
    el.addEventListener('click', function(){{
      var r=this.getBoundingClientRect();
      burst(r.left+r.width/2, r.top+r.height/2, 280);
    }});
  }});
}})();
</script>
</body></html>"""
    render_html(html, height=600, scrolling=False)


# ═══════════════════════════════════════════════════════════════
# STAGE 3 — 3D PHOTO GALLERY (dual row + mouse tilt + glow)
# ═══════════════════════════════════════════════════════════════
def stage_3() -> None:

    # ⭐ REPLACE: Swap picsum.photos URLs with real photo paths/URLs
    row1 = [
        ["assets/sarry.jpeg", "Beautiful Soul"],
        ["assets/selfy.jpeg", "selfie infront mirror"],
        ["assets/kaiking.jpeg", "Kayaking Varkala"],
        ["assets/kodai.jpeg", "KodaiKenal Trip"],
        ["assets/best_for.jpeg", "Beautiful Chaos Together"],
        ["assets/v.jpeg", "Beach Vibes"],
        ["assets/lastyear_bday.jpeg", "Birthday 2025"],
        ["assets/me.jpeg", "black dress vibes"],
        ["assets/bike.jpeg", "Bike Ride Fun"],
    ]
    row2 = [
        ["assets/nandihills.jpeg", "Nandi Hills Vibes"],
        ["assets/trip_2.jpeg", "Road Trip Fun"],
        ["assets/trecking.jpeg", "Trecking with Friends"],
        ["assets/child.jpeg", "Adorable Childhood"],
        ["assets/mygirls.jpeg", "My Beautiful Girls"],
        ["assets/best_friend.jpeg", "Selfie with Best Friend "],
        ["assets/campfire.jpeg", "Camp Fire Memories"],
        ["assets/beauti.jpeg", "So Beauty girl in world"],
    ]
    row1 = [[_path_to_data_uri(src), label] for src, label in row1]
    row2 = [[_path_to_data_uri(src), label] for src, label in row2]
    r1j = json.dumps(row1)
    r2j = json.dumps(row2)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Cinzel:wght@400;700&family=Dancing+Script:wght@600&display=swap');
{ENTRY_CSS}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;height:100%;overflow:hidden;background:#030312;}}
body{{display:flex;flex-direction:column;align-items:stretch;position:relative;}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}}

/* ── Main wrapper fills the full iframe height ── */
.wrap{{
  position:relative;z-index:10;width:100%;
  height:100%;min-height:100vh;
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  padding:clamp(6px,1.5vh,18px) 0;
  gap:0;
}}

/* Header block — fixed natural height */
.hdr{{text-align:center;flex-shrink:0;padding-bottom:clamp(4px,1vh,12px);}}
.eyebrow{{font-family:'Cinzel',serif;font-size:11px;letter-spacing:10px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(3px,.8vh,8px);
  animation:fu .8s ease both;opacity:0;}}
@keyframes fu{{from{{opacity:0;transform:translateY(20px);}}to{{opacity:1;transform:translateY(0);}}}}
.sec-title{{font-family:'Cinzel Decorative',serif;font-size:clamp(15px,3.5vh,34px);
  font-weight:900;background:linear-gradient(135deg,#f0eaff,#c4b5fd,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 26px rgba(139,92,246,.72));
  margin-bottom:0;animation:fu .8s ease .25s both;opacity:0;}}

/* ── Gallery area — expands to fill ALL remaining space ── */
.gallery-area{{
  flex:1 1 0;
  width:100%;
  display:flex;flex-direction:column;
  justify-content:space-evenly;
  align-items:center;
  overflow:hidden;
  gap:clamp(4px,1vh,12px);
  padding:clamp(4px,1vh,12px) 0;
}}

/* Gallery rows — each row takes equal share */
.gallery-row{{
  flex:1 1 0;
  width:100%;
  overflow:hidden;
  position:relative;
  min-height:0;
  display:flex;
  align-items:center;
  mask-image:linear-gradient(90deg,transparent 0%,#000 7%,#000 93%,transparent 100%);
  -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 7%,#000 93%,transparent 100%);
}}
.track{{display:flex;gap:14px;width:max-content;align-items:center;}}
.track-fwd{{animation:scrollFwd 38s linear infinite;}}
.track-rev{{animation:scrollRev 42s linear infinite;}}
.track-fwd:hover,.track-rev:hover{{animation-play-state:paused;}}
@keyframes scrollFwd{{0%{{transform:translateX(0);}}100%{{transform:translateX(-50%);}}}}
@keyframes scrollRev{{0%{{transform:translateX(-50%);}}100%{{transform:translateX(0);}}}}

/* Polaroid card — width & image height set dynamically by JS */
.pc{{
  flex-shrink:0;
  background:rgba(255,255,255,.95);
  border-radius:3px;
  box-shadow:0 10px 30px rgba(0,0,0,.6);
  transform:rotate(var(--r));
  cursor:pointer;position:relative;
  animation:floatPol var(--fd) ease-in-out var(--fdel) infinite;
  will-change:transform;
}}
@keyframes floatPol{{
  0%,100%{{transform:rotate(var(--r)) translateY(0);}}
  50%    {{transform:rotate(var(--r)) translateY(-7px);}}
}}
.pc::after{{
  content:'';position:absolute;inset:-2px;border-radius:3px;
  background:linear-gradient(135deg,#8b5cf6,#3b82f6,#e879f9);
  z-index:-1;opacity:0;filter:blur(7px);transition:opacity .4s;
}}
.pc:hover::after{{opacity:1;}}
.pc-img{{position:relative;overflow:hidden;border-radius:2px;}}
.pc img{{width:100%;display:block;object-fit:cover;
  filter:brightness(.9);transition:filter .5s ease,transform .5s ease;}}
.pc:hover img{{filter:brightness(1.08);transform:scale(1.06);}}
.shine{{position:absolute;inset:0;pointer-events:none;transition:background .12s;border-radius:2px;}}
.caption{{
  font-family:'Dancing Script',cursive;color:#555;
  text-align:center;position:absolute;bottom:0;left:0;right:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 4px;
}}
</style></head><body>
<canvas id="bgCvs"></canvas>
<div class="wrap">
  <div class="hdr stage-root">
    <p class="eyebrow">✦ &nbsp; Gallery &nbsp; ✦</p>
    <h2 class="sec-title">Moments That Feel Special</h2>
  </div>
  <div class="gallery-area">
    <div class="gallery-row"><div class="track track-fwd" id="r1"></div></div>
    <div class="gallery-row"><div class="track track-rev" id="r2"></div></div>
  </div>
</div>
<script>
{PARTICLE_JS}
(function(){{
  var r1={r1j}, r2={r2j};
  function buildRow(photos, trackId){{
    var track=document.getElementById(trackId);
    photos.concat(photos).forEach(function(p){{
      var rot=(Math.random()-.5)*7;
      var card=document.createElement('div'); card.className='pc';
      card.style.setProperty('--r', rot+'deg');
      card.style.setProperty('--fd', (3.5+Math.random()*3).toFixed(1)+'s');
      card.style.setProperty('--fdel', (Math.random()*2.5).toFixed(1)+'s');
      card.innerHTML='<div class="pc-img"><img src="'+p[0]+'" alt="'+p[1]+'" loading="lazy"><div class="shine"></div></div><span class="caption">'+p[1]+'</span>';
      /* 3D tilt on mousemove */
      card.addEventListener('mousemove', function(e){{
        var rect=this.getBoundingClientRect();
        var cx=rect.left+rect.width/2, cy=rect.top+rect.height/2;
        var rx=(e.clientY-cy)/(rect.height/2)*-15;
        var ry=(e.clientX-cx)/(rect.width/2)*15;
        var px=((e.clientX-rect.left)/rect.width*100).toFixed(0);
        var py=((e.clientY-rect.top)/rect.height*100).toFixed(0);
        this.style.transform='perspective(650px) rotateX('+rx+'deg) rotateY('+ry+'deg) scale(1.12)';
        this.querySelector('.shine').style.background=
          'radial-gradient(circle at '+px+'% '+py+'%,rgba(255,255,255,.28) 0%,transparent 65%)';
      }});
      card.addEventListener('mouseleave', function(){{
        this.style.transform='rotate(var(--r))';
        this.style.transition='transform .6s cubic-bezier(.34,1.56,.64,1)';
        this.querySelector('.shine').style.background='none';
      }});
      track.appendChild(card);
    }});
  }}
  /* ── Compute card sizes from actual rendered row height ── */
  function applyCardSizes() {{
    var rows = document.querySelectorAll('.gallery-row');
    if (!rows.length) return;
    var rowH = rows[0].getBoundingClientRect().height;
    /* Image takes 72% of row height; card width ≈ image height × 0.78 */
    var imgH = Math.max(80, Math.round(rowH * 0.72));
    var cardW = Math.max(90, Math.round(imgH * 0.80));
    var topPad = Math.max(6, Math.round(rowH * 0.04));
    var botPad = Math.max(20, Math.round(rowH * 0.16));
    var capFS  = Math.max(9, Math.round(rowH * 0.062));
    document.querySelectorAll('.pc').forEach(function(c) {{
      c.style.width   = cardW + 'px';
      c.style.padding = topPad + 'px ' + topPad + 'px ' + botPad + 'px';
    }});
    document.querySelectorAll('.pc img').forEach(function(img) {{
      img.style.height = imgH + 'px';
    }});
    document.querySelectorAll('.caption').forEach(function(cap) {{
      cap.style.fontSize  = capFS + 'px';
      cap.style.bottom    = Math.max(3, Math.round(rowH * 0.03)) + 'px';
    }});
  }}

  buildRow(r1,'r1'); buildRow(r2,'r2');
  /* Run after layout paint */
  requestAnimationFrame(function() {{ applyCardSizes(); }});
  window.addEventListener('resize', applyCardSizes);
}})();
</script>
</body></html>"""
    render_html(html, height=650, scrolling=False)


# ═══════════════════════════════════════════════════════════════
# STAGE 5 — INTERACTIVE BIRTHDAY CAKE (3-phase experience)
# Phase 0: Make a Wish  →  Phase 1: Blow The Candles  →  Phase 2: Celebration
# ═══════════════════════════════════════════════════════════════
def stage_5() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@1,400;1,700&display=swap');
{ENTRY_CSS} {MAGIC_BTN_CSS}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#030312;min-height:100vh;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  position:relative;transition:background 1.4s ease;}}
body.dimming{{background:#000010;}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;}}
#bgCvs{{z-index:0;}}#fwCvs{{z-index:50;}}#confCvs{{z-index:51;}}

/* ── Phase system ── */
.phase{{display:none;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;padding:clamp(10px, 2vh, 28px) 20px;
  position:relative;z-index:10;width:100%;max-width:700px;margin:0 auto;}}
.phase.active{{display:flex;}}

/* ── Phase 0: Wish Screen ── */
.wstar{{position:fixed;background:#fff;border-radius:50%;animation:tw ease-in-out infinite;}}
@keyframes tw{{0%,100%{{opacity:.08;transform:scale(1);}}50%{{opacity:.92;transform:scale(1.8);}}}}
.float-spark{{position:fixed;border-radius:50%;z-index:2;pointer-events:none;
  animation:floatUp linear infinite;opacity:0;}}
@keyframes floatUp{{
  0%  {{transform:translateY(100vh) scale(0);opacity:0;}}
  10% {{opacity:1;}}
  90% {{opacity:1;}}
  100%{{transform:translateY(-10vh) scale(1);opacity:0;}}
}}
.wish-label{{font-family:'Cinzel',serif;font-size:12px;letter-spacing:11px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(12px, 3vh, 28px);animation:fu 1s ease .3s both;opacity:0;}}
@keyframes fu{{from{{opacity:0;transform:translateY(24px);}}to{{opacity:1;transform:translateY(0);}}}}
.wish-title{{font-family:'Cinzel Decorative',serif;font-size:clamp(24px,7.5vh,64px);
  font-weight:900;line-height:1.18;
  background:linear-gradient(135deg,#fbbf24,#fde68a,#f59e0b,#fbbf24);
  background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;filter:drop-shadow(0 0 38px rgba(251,191,36,.9));
  animation:fu 1.2s ease .6s both,gSh 3s linear 2s infinite;opacity:0;margin-bottom:clamp(8px, 1.5vh, 16px);}}
@keyframes gSh{{from{{background-position:0% center;}}to{{background-position:300% center;}}}}
.wish-sub{{font-family:'Playfair Display',serif;font-style:italic;
  font-size:clamp(13px,2.2vh,18px);color:rgba(196,181,253,.75);
  animation:fu 1s ease 1.1s both;opacity:0;margin-bottom:clamp(20px, 4vh, 50px);}}

/* ── Phase 1: Cake ── */
.cake-eyebrow{{font-family:'Cinzel',serif;font-size:11px;letter-spacing:10px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(6px, 1.5vh, 14px);animation:fu .8s ease both;opacity:0;}}
.cake-scene{{position:relative;display:inline-block;margin:8px auto 14px;}}
.candles{{display:flex;justify-content:center;gap:16px;margin-bottom:5px;position:relative;z-index:10;}}
.candle{{position:relative;width:13px;height:46px;border-radius:4px 4px 2px 2px;overflow:visible;}}
.candle:nth-child(1){{background:linear-gradient(#fbbf24,#d97706);}}
.candle:nth-child(2){{background:linear-gradient(#e879f9,#a855f7);}}
.candle:nth-child(3){{background:linear-gradient(#60a5fa,#2563eb);}}
.candle:nth-child(4){{background:linear-gradient(#34d399,#059669);}}
.candle:nth-child(5){{background:linear-gradient(#fb923c,#ea580c);}}
.c-stripe{{position:absolute;width:100%;height:7px;background:rgba(255,255,255,.3);top:10px;}}
.flame-wrap{{position:absolute;top:-30px;left:50%;transform:translateX(-50%);
  width:22px;height:34px;transition:opacity .5s ease,transform .6s ease;transform-origin:bottom center;}}
.flame-wrap.blown{{opacity:0!important;transform:translateX(-50%) scaleY(0)!important;}}
.flame{{width:13px;height:25px;margin:0 auto;
  background:radial-gradient(ellipse at bottom,#fff 0%,#fbbf24 28%,#f97316 55%,#ef4444 78%,transparent 100%);
  border-radius:50% 50% 22% 22%;animation:flicker .28s ease-in-out infinite alternate;
  filter:blur(.4px);box-shadow:0 0 14px #fbbf24,0 0 28px #f97316;}}
.flame::before{{content:'';position:absolute;bottom:3px;left:50%;transform:translateX(-50%);
  width:5px;height:12px;background:rgba(255,255,255,.88);border-radius:50%;filter:blur(1px);}}
@keyframes flicker{{
  from{{transform:scaleX(1) scaleY(1) rotate(-4deg);}}
  to  {{transform:scaleX(.82) scaleY(1.14) rotate(4deg);}}
}}
.flame-glow{{position:absolute;top:-16px;left:50%;transform:translateX(-50%);
  width:32px;height:32px;border-radius:50%;
  background:radial-gradient(circle,rgba(251,191,36,.55) 0%,transparent 70%);
  filter:blur(9px);animation:gp 1s ease-in-out infinite alternate;}}
@keyframes gp{{from{{transform:translateX(-50%) scale(1);opacity:.5;}}to{{transform:translateX(-50%) scale(1.45);opacity:.95;}}}}
.smoke{{position:absolute;top:-10px;left:50%;transform:translateX(-50%);
  display:none;width:10px;}}
.smoke.show{{display:block;}}
.smoke-puff{{position:absolute;bottom:0;left:50%;transform:translateX(-50%);
  width:9px;height:9px;background:rgba(180,180,200,.35);border-radius:50%;
  animation:sd 1.9s ease-out forwards;}}
@keyframes sd{{
  0%  {{transform:translateX(-50%) scale(.4) translateY(0);opacity:.7;}}
  100%{{transform:translateX(-50%) scale(3.2) translateY(-42px);opacity:0;}}
}}
/* Cake layers */
.l{{position:relative;overflow:visible;}}
.lt{{width:185px;height:58px;background:linear-gradient(135deg,#f472b6,#ec4899,#db2777);
  border-radius:8px 8px 3px 3px;margin:0 auto;
  box-shadow:0 0 25px rgba(244,114,182,.45),inset 0 2px 12px rgba(255,255,255,.2);}}
.frosting{{position:absolute;top:-10px;left:0;right:0;display:flex;justify-content:space-around;padding:0 12px;}}
.drip{{width:18px;height:18px;background:#fff;border-radius:50% 50% 50% 50%/20% 20% 80% 80%;box-shadow:0 0 6px rgba(255,255,255,.5);}}
.lm{{width:208px;height:64px;background:linear-gradient(135deg,#c084fc,#a855f7,#7c3aed);
  margin:0 auto;box-shadow:0 0 25px rgba(192,132,252,.45),inset 0 2px 12px rgba(255,255,255,.2);}}
.lb{{width:240px;height:70px;background:linear-gradient(135deg,#818cf8,#6366f1,#4338ca);
  border-radius:0 0 10px 10px;margin:0 auto;
  box-shadow:0 0 30px rgba(129,140,248,.45),0 15px 40px rgba(0,0,0,.55),inset 0 2px 12px rgba(255,255,255,.2);}}
.cdots{{text-align:center;padding:10px 0;}}
.cdots span{{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:rgba(255,255,255,.42);margin:0 7px;vertical-align:middle;}}
.plate{{width:282px;height:22px;background:linear-gradient(135deg,#e2e8f0,#f8fafc,#e2e8f0);
  border-radius:50%;margin:0 auto;box-shadow:0 8px 26px rgba(0,0,0,.55),0 0 30px rgba(139,92,246,.15);}}
.cake-halo{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:330px;height:330px;border-radius:50%;
  background:radial-gradient(circle,rgba(139,92,246,.11) 0%,transparent 70%);
  animation:halo 3s ease-in-out infinite;z-index:-1;pointer-events:none;}}
@keyframes halo{{0%,100%{{transform:translate(-50%,-50%) scale(1);opacity:.6;}}50%{{transform:translate(-50%,-50%) scale(1.18);opacity:1;}}}}
#blowText{{display:none;font-family:'Cinzel',serif;font-size:13px;letter-spacing:5px;
  color:rgba(255,255,255,.45);text-transform:uppercase;margin-top:10px;animation:fu .5s ease both;}}

/* ── Phase 2: Celebration ── */
.cel-title{{font-family:'Cinzel Decorative',serif;
  font-size:clamp(26px,8vh,72px);font-weight:900;line-height:1.1;
  background:linear-gradient(135deg,#fbbf24,#fde68a,#f59e0b,#fbbf24);
  background-size:400% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;filter:drop-shadow(0 0 38px rgba(251,191,36,.98));
  animation:celReveal 1.6s cubic-bezier(.34,1.56,.64,1) both,gSh 2.5s linear 1.5s infinite;
  opacity:0;margin-bottom:14px;}}
@keyframes celReveal{{
  0%  {{opacity:0;transform:scale(.12) translateY(50px);filter:blur(22px);}}
  100%{{opacity:1;transform:scale(1) translateY(0);filter:blur(0);}}
}}
.cel-name{{font-family:'Cinzel Decorative',serif;
  font-size:clamp(36px,12vh,96px);font-weight:900;letter-spacing:clamp(4px,2vw,16px);
  background:linear-gradient(135deg,#e879f9,#c084fc,#818cf8,#60a5fa,#a78bfa);
  background-size:500% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  animation:celReveal 1.6s cubic-bezier(.34,1.56,.64,1) .35s both,
            nameSh 2s linear 2s infinite,
            nameGl 3s ease-in-out 2s infinite alternate,
            nameFloat 5s ease-in-out 3s infinite;
  opacity:0;margin-bottom:clamp(12px, 3vh, 28px);}}
@keyframes nameSh{{from{{background-position:0% center;}}to{{background-position:500% center;}}}}
@keyframes nameGl{{
  from{{filter:drop-shadow(0 0 26px rgba(139,92,246,.55));}}
  to  {{filter:drop-shadow(0 0 70px rgba(139,92,246,1)) drop-shadow(0 0 130px rgba(192,38,211,.6));}}
}}
@keyframes nameFloat{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-11px);}}}}
.cel-div{{width:310px;height:2px;
  background:linear-gradient(90deg,transparent,#fbbf24,#e879f9,#60a5fa,transparent);
  margin:0 auto clamp(12px, 3vh, 26px);animation:celReveal 1s ease .9s both;opacity:0;}}
.cel-msg{{font-family:'Playfair Display',serif;font-style:italic;
  font-size:clamp(14px,2.6vh,20px);color:rgba(226,213,248,.9);line-height:1.8;
  animation:celReveal 1s ease 1.2s both;opacity:0;}}

@media (max-height: 600px) {{
  .cake-scene {{ transform: scale(0.7); margin: 0px auto; transform-origin: center center; }}
  .cake-eyebrow {{ margin-bottom: 6px; }}
  .magic-btn {{ padding: 12px 36px !important; font-size: 14px !important; }}
  .wish-title {{ margin-bottom: 6px; }}
  .wish-sub {{ margin-bottom: 20px; }}
  #blowBtn {{ margin-top: 10px !important; }}
}}
.cel-ring{{position:fixed;border-radius:50%;border:1px solid;
  top:50%;left:50%;transform:translate(-50%,-50%);
  animation:ringEx 3.5s ease-out infinite;pointer-events:none;z-index:52;}}
@keyframes ringEx{{0%{{width:0;height:0;opacity:.9;}}100%{{width:260vmax;height:260vmax;opacity:0;}}}}
</style></head><body>
<canvas id="bgCvs"></canvas>
<canvas id="fwCvs"></canvas>
<canvas id="confCvs"></canvas>

<!-- PHASE 0: Make a Wish -->
<div class="phase active" id="ph0">
  <div id="wstars"></div>
  <p class="wish-label">✦ &nbsp; A Special Moment &nbsp; ✦</p>
  <h1 class="wish-title">Make a Birthday Wish ✨</h1>
  <p class="wish-sub">Close your eyes… take a deep breath… make your wish</p>
  <button class="magic-btn gold" onclick="showCake(this)">Show The Cake ✨</button>
</div>

<!-- PHASE 1: Cake -->
<div class="phase" id="ph1">
  <p class="cake-eyebrow">✦ &nbsp; The Celebration &nbsp; ✦</p>
  <div class="cake-scene">
    <div class="cake-halo"></div>
    <div class="candles">
      <div class="candle"><div class="c-stripe"></div>
        <div class="flame-wrap" id="fw0"><div class="flame-glow"></div><div class="flame"></div></div>
        <div class="smoke" id="sm0"><div class="smoke-puff"></div><div class="smoke-puff" style="animation-delay:.18s;left:55%;"></div></div></div>
      <div class="candle"><div class="c-stripe"></div>
        <div class="flame-wrap" id="fw1"><div class="flame-glow"></div><div class="flame"></div></div>
        <div class="smoke" id="sm1"><div class="smoke-puff"></div><div class="smoke-puff" style="animation-delay:.18s;left:55%;"></div></div></div>
      <div class="candle"><div class="c-stripe"></div>
        <div class="flame-wrap" id="fw2"><div class="flame-glow"></div><div class="flame"></div></div>
        <div class="smoke" id="sm2"><div class="smoke-puff"></div><div class="smoke-puff" style="animation-delay:.18s;left:55%;"></div></div></div>
      <div class="candle"><div class="c-stripe"></div>
        <div class="flame-wrap" id="fw3"><div class="flame-glow"></div><div class="flame"></div></div>
        <div class="smoke" id="sm3"><div class="smoke-puff"></div><div class="smoke-puff" style="animation-delay:.18s;left:55%;"></div></div></div>
      <div class="candle"><div class="c-stripe"></div>
        <div class="flame-wrap" id="fw4"><div class="flame-glow"></div><div class="flame"></div></div>
        <div class="smoke" id="sm4"><div class="smoke-puff"></div><div class="smoke-puff" style="animation-delay:.18s;left:55%;"></div></div></div>
    </div>
    <div class="l"><div class="lt">
      <div class="frosting"><div class="drip"></div><div class="drip"></div><div class="drip"></div><div class="drip"></div><div class="drip"></div></div>
    </div></div>
    <div class="l"><div class="lm"><div class="cdots"><span></span><span></span><span></span></div></div></div>
    <div class="l"><div class="lb"><div class="cdots"><span></span><span></span><span></span><span></span></div></div></div>
    <div class="plate"></div>
  </div>
  <button class="magic-btn violet" id="blowBtn" onclick="startBlowing(this)"
    style="margin-top:20px;animation:fu .8s ease .5s both;opacity:0;">
    Blow The Candles
  </button>
  <p id="blowText">✨ Making magic happen…</p>
</div>

<!-- PHASE 2: Grand Birthday Reveal -->
<div class="phase" id="ph2">
  <div class="cel-ring" style="border-color:rgba(251,191,36,.38);animation-delay:0s;"></div>
  <div class="cel-ring" style="border-color:rgba(139,92,246,.25);animation-delay:1.15s;"></div>
  <div class="cel-ring" style="border-color:rgba(59,130,246,.2);animation-delay:2.3s;"></div>
  <!-- ⭐ REPLACE: Edit the birthday message and name below -->
  <h1 class="cel-title">HAPPY BIRTHDAY</h1>
  <div class="cel-name">POOJA</div>
  <div class="cel-div"></div>
  <p class="cel-msg">May your life always shine as beautifully as your heart.</p>
</div>

<script>
{PARTICLE_JS}
{MAGIC_BTN_JS}

/* ── Phase 0: wish-screen stars + floating sparks ── */
(function(){{
  var ws=document.getElementById('wstars');
  ws.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none;';
  for(var i=0;i<90;i++){{
    var s=document.createElement('div'); s.className='wstar';
    var sz=Math.random()*3.2+.4;
    var col=Math.random()>.55?'#fbbf24':Math.random()>.5?'#a78bfa':'#fff';
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;background:'+col+';top:'+Math.random()*100+'%;left:'+Math.random()*100+'%;animation-duration:'+(Math.random()*3+2)+'s;animation-delay:'+(Math.random()*4)+'s;';
    ws.appendChild(s);
  }}
  setInterval(function(){{
    var sp=document.createElement('div'); sp.className='float-spark';
    var sz=Math.random()*5+2;
    var cols=['rgba(251,191,36','rgba(139,92,246','rgba(192,38,211','rgba(167,139,250'];
    var col=cols[Math.floor(Math.random()*cols.length)];
    sp.style.cssText='width:'+sz+'px;height:'+sz+'px;background:'+col+',.8);left:'+(Math.random()*100)+'%;animation-duration:'+(Math.random()*4+3)+'s;animation-delay:'+(Math.random()*.5)+'s;box-shadow:0 0 8px '+col+',.4);';
    document.body.appendChild(sp);
    setTimeout(function(){{sp.remove();}},5500);
  }},380);
}})();

/* ── Phase switch ── */
function switchPhase(fromId, toId){{
  var from=document.getElementById(fromId);
  from.style.opacity='0';from.style.transition='opacity .5s ease';
  setTimeout(function(){{
    from.classList.remove('active');from.style.opacity='';from.style.transition='';
    var to=document.getElementById(toId);
    to.classList.add('active');
  }},500);
}}

function showCake(btn){{ btn.disabled=true; switchPhase('ph0','ph1'); }}

/* ── Blow candle sequence ── */
var blown=0;
var fwCvs=document.getElementById('fwCvs'), fwCtx=fwCvs.getContext('2d');
fwCvs.width=window.innerWidth; fwCvs.height=window.innerHeight;

function startBlowing(btn){{
  btn.style.display='none';
  document.getElementById('blowText').style.display='block';
  var iv=setInterval(function(){{
    blowCandle(blown); blown++;
    if(blown>=5){{clearInterval(iv);setTimeout(triggerCelebration,1500);}}
  }},430);
}}

function blowCandle(idx){{
  document.getElementById('fw'+idx).classList.add('blown');
  var sm=document.getElementById('sm'+idx);
  sm.classList.add('show');
  sm.querySelectorAll('.smoke-puff').forEach(function(p){{p.style.animation='none';void p.offsetWidth;p.style.animation='';}} );
  /* dim room incrementally */
  var d=idx/5;
  document.body.style.background='rgb('+(3+Math.round(d*4))+','+(3+Math.round(d*4))+','+(18+Math.round(d*6))+')';
  /* mini spark burst */
  var fw=document.getElementById('fw'+idx), rect=fw.getBoundingClientRect();
  for(var i=0;i<35;i++){{
    var a=Math.random()*Math.PI*2,sp=Math.random()*6+1;
    (function(p){{
      var pts=[p], raf=requestAnimationFrame;
      (function loop(){{
        pts=pts.filter(function(q){{return q.life>0;}});if(!pts.length)return;
        pts.forEach(function(q){{
          q.vx*=.93;q.vy*=.93;q.vy+=.06;q.x+=q.vx;q.y+=q.vy;q.life-=q.d;
          fwCtx.save();fwCtx.globalAlpha=q.life;
          fwCtx.beginPath();fwCtx.arc(q.x,q.y,q.sz,0,Math.PI*2);
          fwCtx.fillStyle='hsl('+q.h+',100%,72%)';fwCtx.shadowBlur=10;fwCtx.shadowColor='hsl('+q.h+',100%,62%)';
          fwCtx.fill();fwCtx.restore();
        }});raf(loop);
      }})();
    }})({{x:rect.left+rect.width/2,y:rect.top+rect.height/2,
         vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,life:1,d:.04,sz:Math.random()*2+1,
         h:Math.random()>.5?45:280}});
  }}
}}

/* ── Celebration ── */
var fwPts=[],confPts=[],goldPts=[],fwActive=false;
var confCvs=document.getElementById('confCvs'),confCtx=confCvs.getContext('2d');
confCvs.width=window.innerWidth; confCvs.height=window.innerHeight;

function triggerCelebration(){{
  document.body.style.background='#030312';
  document.body.style.transition='background 1.2s ease';
  /* Show finale immediately after blowing */
  setTimeout(function(){{
    showFinale();
  }}, 500);
}}

function showFinale(){{
  var finale=document.getElementById('finale');
  if(finale){{
    finale.style.opacity='1';
    createBalloons();
  }}
}}
function FWPt(x,y,h){{
  this.x=x;this.y=y;this.h=h;
  var a=Math.random()*Math.PI*2,sp=Math.random()*12+4;
  this.vx=Math.cos(a)*sp;this.vy=Math.sin(a)*sp;
  this.life=1;this.d=Math.random()*.016+.009;this.sz=Math.random()*3.5+1;this.trail=[];
}}
FWPt.prototype.update=function(){{
  this.trail.push({{x:this.x,y:this.y}});if(this.trail.length>7)this.trail.shift();
  this.vx*=.967;this.vy*=.967;this.vy+=.07;this.x+=this.vx;this.y+=this.vy;this.life-=this.d;
}};
FWPt.prototype.draw=function(){{
  var s=this;
  this.trail.forEach(function(t,i){{fwCtx.save();fwCtx.globalAlpha=.35*(i/7)*s.life;fwCtx.beginPath();fwCtx.arc(t.x,t.y,s.sz*.5,0,Math.PI*2);fwCtx.fillStyle='hsl('+s.h+',100%,72%)';fwCtx.fill();fwCtx.restore();}});
  fwCtx.save();fwCtx.globalAlpha=this.life;fwCtx.beginPath();fwCtx.arc(this.x,this.y,this.sz,0,Math.PI*2);
  fwCtx.fillStyle='hsl('+this.h+',100%,72%)';fwCtx.shadowBlur=18;fwCtx.shadowColor='hsl('+this.h+',100%,62%)';fwCtx.fill();fwCtx.restore();
}};
function launchFw(){{var x=Math.random()*fwCvs.width,y=Math.random()*fwCvs.height*.52,h=Math.random()*360;for(var i=0;i<110;i++)fwPts.push(new FWPt(x,y,h));}}
function fwLoop(){{
  if(!fwActive)return;
  fwCtx.fillStyle='rgba(3,3,18,.15)';fwCtx.fillRect(0,0,fwCvs.width,fwCvs.height);
  fwPts=fwPts.filter(function(p){{return p.life>0;}});fwPts.forEach(function(p){{p.update();p.draw();}});
  requestAnimationFrame(fwLoop);
}}
function Conf(){{this.reset();}}
Conf.prototype.reset=function(){{
  this.x=Math.random()*confCvs.width;this.y=-25;
  this.w=Math.random()*13+5;this.hh=Math.random()*6+3;
  this.col='hsl('+(Math.random()*360)+',100%,62%)';
  this.vx=(Math.random()-.5)*5;this.vy=Math.random()*4+2;
  this.rot=Math.random()*Math.PI*2;this.rs=(Math.random()-.5)*.16;
}};
Conf.prototype.update=function(){{this.x+=this.vx;this.y+=this.vy;this.rot+=this.rs;this.vy+=.04;if(this.y>confCvs.height+30)this.reset();}};
Conf.prototype.draw=function(){{confCtx.save();confCtx.globalAlpha=.9;confCtx.translate(this.x,this.y);confCtx.rotate(this.rot);confCtx.fillStyle=this.col;confCtx.fillRect(-this.w/2,-this.hh/2,this.w,this.hh);confCtx.restore();}};
function GP(){{this.reset();}}
GP.prototype.reset=function(){{this.x=Math.random()*confCvs.width;this.y=-15;this.sz=Math.random()*4+1.5;this.vy=Math.random()*2+.8;this.vx=(Math.random()-.5)*1.5;this.op=Math.random()*.7+.3;}};
GP.prototype.update=function(){{this.x+=this.vx;this.y+=this.vy;if(this.y>confCvs.height+10)this.reset();}};
GP.prototype.draw=function(){{confCtx.save();confCtx.globalAlpha=this.op;confCtx.beginPath();confCtx.arc(this.x,this.y,this.sz,0,Math.PI*2);confCtx.fillStyle='#fbbf24';confCtx.shadowBlur=11;confCtx.shadowColor='rgba(251,191,36,.7)';confCtx.fill();confCtx.restore();}};
function confLoop(){{confCtx.clearRect(0,0,confCvs.width,confCvs.height);confPts.forEach(function(c){{c.update();c.draw();}});goldPts.forEach(function(g){{g.update();g.draw();}});requestAnimationFrame(confLoop);}}

/* Balloon animation */
function createBalloons(){{
  var balloonContainer=document.getElementById('balloonContainer');
  if(!balloonContainer){{
    balloonContainer=document.createElement('div');
    balloonContainer.id='balloonContainer';
    balloonContainer.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99;';
    document.body.appendChild(balloonContainer);
  }}
  
  var colors=['#fbbf24','#e879f9','#60a5fa','#34d399','#fb923c','#a78bfa','#ec4899'];
  
  for(var i=0;i<12;i++){{
    var balloon=document.createElement('div');
    var col=colors[Math.floor(Math.random()*colors.length)];
    var left=Math.random()*100;
    var delay=Math.random()*1.5;
    var duration=Math.random()*3+5;
    var drift=Math.random()*80-40;
    
    balloon.style.position='fixed';
    balloon.style.width='30px';
    balloon.style.height='40px';
    balloon.style.borderRadius='50% 50% 50% 0';
    balloon.style.background=col;
    balloon.style.boxShadow='0 0 15px '+col+'50,-8px -8px 15px '+col+'30';
    balloon.style.bottom='-50px';
    balloon.style.left=left+'%';
    balloon.style.transform='rotate(-45deg)';
    balloon.style.zIndex='98';
    
    var keyframes='@keyframes balloon'+i+'{{0%{{bottom:-50px;opacity:1;left:'+left+'%;}}100%{{bottom:120vh;opacity:0;left:'+(left+drift)+'%;}}}}';
    if(!document.getElementById('balloonStyle'+i)){{
      var style=document.createElement('style');
      style.id='balloonStyle'+i;
      style.textContent=keyframes;
      document.head.appendChild(style);
    }}
    
    balloon.style.animation='balloon'+i+' '+duration+'s ease-in '+delay+'s forwards';
    balloonContainer.appendChild(balloon);
  }}
}}

window.addEventListener('resize',function(){{fwCvs.width=window.innerWidth;fwCvs.height=window.innerHeight;confCvs.width=window.innerWidth;confCvs.height=window.innerHeight;}});
</script>

<div id="finale" style="display:flex;opacity:0;transition:opacity 2s ease;position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg,rgba(3,3,18,0.85),rgba(30,15,50,0.9));flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:100;padding:20px;pointer-events:none;">
  <div style="position:relative;margin-bottom:30px;">
    <h1 style="font-family:'Cinzel Decorative',serif;font-size:clamp(38px,12vh,96px);font-weight:900;letter-spacing:clamp(5px,2vw,18px);background:linear-gradient(135deg,#fbbf24,#fde68a,#f59e0b,#fbbf24);background-size:400% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 30px rgba(251,191,36,.7));animation:slideInDown 1s cubic-bezier(.34,1.56,.64,1) .3s both,pulse 2s ease 1.5s infinite;margin:0 0 10px 0;text-shadow:0 0 40px rgba(251,191,36,.4);">HAPPY BIRTHDAY</h1>
  </div>
  <div style="font-family:'Cinzel Decorative',serif;font-size:clamp(38px,12vh,96px);font-weight:900;letter-spacing:clamp(5px,2vw,18px);background:linear-gradient(135deg,#e879f9,#c084fc,#818cf8,#60a5fa,#a78bfa);background-size:500% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:slideInUp 1s cubic-bezier(.34,1.56,.64,1) .5s both,glow 2s ease 1.8s infinite;margin-bottom:20px;text-shadow:0 0 50px rgba(139,92,246,.5);">POOJA</div>
  <div style="width:350px;height:2px;background:linear-gradient(90deg,transparent,#fbbf24,#e879f9,#60a5fa,transparent);margin-bottom:20px;animation:slideInUp 1s ease .7s both;"></div>
  <p style="font-family:'Playfair Display',serif;font-style:italic;font-size:clamp(14px,2.6vh,24px);color:rgba(226,213,248,.92);text-shadow:0 0 30px rgba(139,92,246,.45);margin-bottom:10px;animation:slideInUp 1s ease .9s both;opacity:0;">You make every moment brighter just by being yourself.</p>
  <p style="font-family:'Playfair Display',serif;font-style:italic;font-size:14px;color:rgba(251,191,36,.45);letter-spacing:3px;animation:slideInUp 1s ease 1.1s both;opacity:0;">— Made with warmth & wonder —</p>
  <style>
    @keyframes slideInDown {{
      from {{ opacity:0;transform:translateY(-40px) scale(.8);filter:blur(10px); }}
      to {{ opacity:1;transform:translateY(0) scale(1);filter:blur(0); }}
    }}
    @keyframes slideInUp {{
      from {{ opacity:0;transform:translateY(30px);filter:blur(5px); }}
      to {{ opacity:1;transform:translateY(0);filter:blur(0); }}
    }}
    @keyframes pulse {{
      0%,100% {{ filter:drop-shadow(0 0 20px rgba(251,191,36,.7)); }}
      50% {{ filter:drop-shadow(0 0 40px rgba(251,191,36,1)); }}
    }}
    @keyframes glow {{
      0%,100% {{ filter:drop-shadow(0 0 30px rgba(139,92,246,.6)); }}
      50% {{ filter:drop-shadow(0 0 60px rgba(139,92,246,1)) drop-shadow(0 0 100px rgba(192,38,211,.8)); }}
    }}
  </style>
</div>

</body></html>"""
    render_html(html, height=600, scrolling=False)



# ═══════════════════════════════════════════════════════════════
# STAGE 7 — GRAND FINALE (mega fireworks + golden rain + aurora)
# ═══════════════════════════════════════════════════════════════
def stage_7() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@1,400;1,700&display=swap');
{ENTRY_CSS}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#030312;min-height:100vh;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;}}
#auroraC{{z-index:0;}}#fwC{{z-index:1;}}#goldC{{z-index:2;}}
.star{{position:fixed;background:#fff;border-radius:50%;animation:tw ease-in-out infinite;z-index:3;}}
@keyframes tw{{0%,100%{{opacity:.07;transform:scale(1);}}50%{{opacity:1;transform:scale(1.8);}}}}
.ring{{position:fixed;border-radius:50%;border:1px solid;top:50%;left:50%;
  transform:translate(-50%,-50%);animation:ringEx 5s ease-out infinite;z-index:3;pointer-events:none;}}
@keyframes ringEx{{0%{{width:0;height:0;opacity:.9;}}100%{{width:230vmax;height:230vmax;opacity:0;}}}}
.wrap{{position:relative;z-index:10;text-align:center;padding:clamp(10px, 2.5vh, 34px) 20px;
  animation:grandReveal 2.2s cubic-bezier(.16,1,.3,1) both;}}
@keyframes grandReveal{{
  0%  {{opacity:0;transform:scale(.07) rotate(-9deg);filter:blur(32px);}}
  60% {{filter:blur(3px);}}
  100%{{opacity:1;transform:scale(1) rotate(0);filter:blur(0);}}
}}
.eyebrow{{font-family:'Cinzel',serif;font-size:12px;letter-spacing:12px;color:#fbbf24;
  text-transform:uppercase;margin-bottom:clamp(10px, 2vh, 20px);animation:fu 1s ease 1.1s both;opacity:0;}}
@keyframes fu{{from{{opacity:0;transform:translateY(20px);}}to{{opacity:1;transform:translateY(0);}}}}
.hb{{font-family:'Cinzel Decorative',serif;font-size:clamp(26px,8vh,76px);
  font-weight:900;line-height:1.1;
  background:linear-gradient(135deg,#fbbf24,#fde68a,#f59e0b,#fbbf24);background-size:400% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 34px rgba(251,191,36,.95));
  animation:fu 1s ease .5s both,gSh 2s linear 2s infinite;opacity:0;margin-bottom:clamp(6px, 1vh, 10px);}}
@keyframes gSh{{from{{background-position:0% center;}}to{{background-position:400% center;}}}}
.name{{font-family:'Cinzel Decorative',serif;
  font-size:clamp(38px,12vh,96px);font-weight:900;letter-spacing:clamp(5px,2vw,18px);
  background:linear-gradient(135deg,#e879f9,#c084fc,#818cf8,#60a5fa,#a78bfa);background-size:500% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:fu 1s ease .8s both,nameSh 2s linear 2s infinite,
            nameGl 3s ease-in-out 2s infinite alternate,nameFloat 5s ease-in-out 3s infinite;
  opacity:0;margin-bottom:clamp(12px, 3vh, 28px);}}
@keyframes nameSh{{from{{background-position:0% center;}}to{{background-position:500% center;}}}}
@keyframes nameGl{{from{{filter:drop-shadow(0 0 26px rgba(139,92,246,.55));}}to{{filter:drop-shadow(0 0 72px rgba(139,92,246,1)) drop-shadow(0 0 140px rgba(192,38,211,.65));}}}}
@keyframes nameFloat{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-12px);}}}}
.divider{{width:350px;height:2px;
  background:linear-gradient(90deg,transparent,#fbbf24,#e879f9,#60a5fa,transparent);
  margin:0 auto clamp(12px, 3vh, 28px);animation:fu 1s ease 1.4s both;opacity:0;}}
/* ⭐ REPLACE: Edit subtext below */
.sub{{font-family:'Playfair Display',serif;font-style:italic;
  font-size:clamp(14px,2.6vh,24px);color:rgba(226,213,248,.92);
  text-shadow:0 0 30px rgba(139,92,246,.45);margin-bottom:clamp(10px, 2vh, 20px);animation:fu 1s ease 1.8s both;opacity:0;}}
.sig{{font-family:'Playfair Display',serif;font-style:italic;font-size:14px;
  color:rgba(251,191,36,.45);letter-spacing:3px;animation:fu 1.5s ease 2.4s both;opacity:0;}}
</style></head><body>
<canvas id="auroraC"></canvas>
<canvas id="fwC"></canvas>
<canvas id="goldC"></canvas>
<div id="stars"></div>
<div class="ring" style="border-color:rgba(139,92,246,.32);animation-delay:0s;"></div>
<div class="ring" style="border-color:rgba(192,38,211,.22);animation-delay:1.25s;"></div>
<div class="ring" style="border-color:rgba(59,130,246,.18);animation-delay:2.5s;"></div>
<div class="ring" style="border-color:rgba(251,191,36,.18);animation-delay:3.75s;"></div>
<div class="wrap">
  <p class="eyebrow">✦ &nbsp; The Grand Finale &nbsp; ✦</p>
  <h1 class="hb">HAPPY BIRTHDAY</h1>
  <!-- ⭐ REPLACE: Change the name below -->
  <div class="name">POOJA</div>
  <div class="divider"></div>
  <!-- ⭐ REPLACE: Edit the subtext below -->
  <p class="sub">You make every moment brighter just by being yourself.</p>
  <p class="sig">— Made with warmth &amp; wonder —</p>
</div>
<script>
{PARTICLE_JS}
/* Stars */
(function(){{
  var c=document.getElementById('stars');
  for(var i=0;i<210;i++){{
    var s=document.createElement('div');s.className='star';
    var sz=Math.random()*3.5+.3;
    s.style.cssText='width:'+sz+'px;height:'+sz+'px;top:'+Math.random()*100+'%;left:'+Math.random()*100+'%;animation-duration:'+(Math.random()*4+1.5)+'s;animation-delay:'+(Math.random()*5)+'s;';
    c.appendChild(s);
  }}
}})();
/* Animated aurora */
(function(){{
  var c=document.getElementById('auroraC'),ctx=c.getContext('2d');
  c.width=window.innerWidth;c.height=window.innerHeight;
  var t=0,orbs=[
    {{x:.18,y:.38,r:.45,col:'rgba(76,29,149',ph:0}},
    {{x:.82,y:.28,r:.38,col:'rgba(30,64,175',ph:1}},
    {{x:.5, y:.72,r:.34,col:'rgba(192,38,211',ph:2}},
    {{x:.12,y:.82,r:.28,col:'rgba(251,191,36',ph:3}},
    {{x:.92,y:.72,r:.25,col:'rgba(139,92,246',ph:4}},
  ];
  (function loop(){{
    ctx.clearRect(0,0,c.width,c.height);t+=.004;
    orbs.forEach(function(o){{
      var ox=(o.x+Math.sin(t+o.ph)*.13)*c.width;
      var oy=(o.y+Math.cos(t+o.ph)*.11)*c.height;
      var r=o.r*Math.min(c.width,c.height);
      var g=ctx.createRadialGradient(ox,oy,0,ox,oy,r);
      g.addColorStop(0,o.col+',.36)');g.addColorStop(1,o.col+',0)');
      ctx.fillStyle=g;ctx.fillRect(0,0,c.width,c.height);
    }});requestAnimationFrame(loop);
  }})();
  window.addEventListener('resize',function(){{c.width=window.innerWidth;c.height=window.innerHeight;}});
}})();
/* Mega fireworks with trails */
(function(){{
  var c=document.getElementById('fwC'),ctx=c.getContext('2d');
  c.width=window.innerWidth;c.height=window.innerHeight;
  var pts=[];
  function FW(x,y,h){{
    this.x=x;this.y=y;this.h=h;
    var a=Math.random()*Math.PI*2,sp=Math.random()*13+5;
    this.vx=Math.cos(a)*sp;this.vy=Math.sin(a)*sp;
    this.life=1;this.d=Math.random()*.015+.007;this.sz=Math.random()*4+1;this.trail=[];
  }}
  FW.prototype.update=function(){{
    this.trail.push({{x:this.x,y:this.y}});if(this.trail.length>8)this.trail.shift();
    this.vx*=.968;this.vy*=.968;this.vy+=.065;this.x+=this.vx;this.y+=this.vy;this.life-=this.d;
  }};
  FW.prototype.draw=function(){{
    var s=this;
    this.trail.forEach(function(t,i){{ctx.save();ctx.globalAlpha=.4*(i/8)*s.life;ctx.beginPath();ctx.arc(t.x,t.y,s.sz*.55,0,Math.PI*2);ctx.fillStyle='hsl('+s.h+',100%,72%)';ctx.fill();ctx.restore();}});
    ctx.save();ctx.globalAlpha=this.life;ctx.beginPath();ctx.arc(this.x,this.y,this.sz,0,Math.PI*2);
    ctx.fillStyle='hsl('+this.h+',100%,72%)';ctx.shadowBlur=20;ctx.shadowColor='hsl('+this.h+',100%,64%)';ctx.fill();ctx.restore();
  }};
  function launch(){{var x=Math.random()*c.width,y=Math.random()*c.height*.52,h=Math.random()*360;for(var i=0;i<125;i++)pts.push(new FW(x,y,h));}}
  (function loop(){{ctx.fillStyle='rgba(3,3,18,.12)';ctx.fillRect(0,0,c.width,c.height);pts=pts.filter(function(p){{return p.life>0;}});pts.forEach(function(p){{p.update();p.draw();}});requestAnimationFrame(loop);}})();
  var cnt=0;(function af(){{launch();cnt++;setTimeout(af,cnt<14?340:1400);}})();
  window.addEventListener('resize',function(){{c.width=window.innerWidth;c.height=window.innerHeight;}});
}})();
/* Golden rain */
(function(){{
  var c=document.getElementById('goldC'),ctx=c.getContext('2d');
  c.width=window.innerWidth;c.height=window.innerHeight;
  function GP(){{this.reset();}}
  GP.prototype.reset=function(){{this.x=Math.random()*c.width;this.y=Math.random()*-c.height;this.sz=Math.random()*4+1.5;this.vy=Math.random()*1.8+.8;this.vx=(Math.random()-.5)*1;this.op=Math.random()*.7+.3;}};
  GP.prototype.update=function(){{this.x+=this.vx;this.y+=this.vy;if(this.y>c.height+10)this.reset();}};
  GP.prototype.draw=function(){{ctx.save();ctx.globalAlpha=this.op;ctx.beginPath();ctx.arc(this.x,this.y,this.sz,0,Math.PI*2);ctx.fillStyle='#fbbf24';ctx.shadowBlur=13;ctx.shadowColor='rgba(251,191,36,.75)';ctx.fill();ctx.restore();}};
  var gpts=[];for(var i=0;i<190;i++)gpts.push(new GP());
  (function loop(){{ctx.clearRect(0,0,c.width,c.height);gpts.forEach(function(g){{g.update();g.draw();}});requestAnimationFrame(loop);}})();
  window.addEventListener('resize',function(){{c.width=window.innerWidth;c.height=window.innerHeight;}});
}})();
</script>
</body></html>"""
    render_html(html, height=600, scrolling=False)


# ═══════════════════════════════════════════════════════════════
# NAVIGATION
# ═══════════════════════════════════════════════════════════════
def show_navigation(stage: int, total: int = 4) -> None:
    names = {1:"Welcome",2:"Name Reveal",3:"Photo Gallery",
             4:"Grand Finale"}
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if stage > 1:
            if st.button("← Prev", key="btn_prev"):
                st.session_state.stage -= 1; st.rerun()
    with c2:
        st.markdown(
            f'<div style="text-align:center;padding:6px 0;">'
            f'<span style="font-family:Cinzel,serif;font-size:11px;letter-spacing:4px;'
            f'color:rgba(255,255,255,.3);text-transform:uppercase;">'
            f'{names.get(stage,"")}</span></div>',
            unsafe_allow_html=True)
    with c3:
        if stage < total:
            if st.button("Next →", key="btn_next"):
                st.session_state.stage += 1; st.rerun()
        else:
            if st.button("↺ Restart", key="btn_rst"):
                st.session_state.stage = 1; st.rerun()


# ═══════════════════════════════════════════════════════════════
# PERSISTENT BACKGROUND MUSIC
# ═══════════════════════════════════════════════════════════════
def inject_persistent_music() -> None:
    """Inject hidden background audio player that persists across stage navigation.
    Auto-plays on first ANY user interaction (satisfies browser autoplay policy).
    Music is always on — cannot be turned off.
    """
    uri = _get_music_data_uri()
    if not uri:
        return

    html = f"""
    <script>
    (function(){{
      try {{
        var parentDoc = window.parent.document;
        var parentWin = window.parent;
        if (!parentDoc) return;

        var keyTime      = 'bgMusicTime_v1';

        // ── Find or create global audio element on the parent body ──
        var a = parentDoc.getElementById('globalBgAudio');
        var isNew = false;
        if (!a) {{
          isNew = true;
          a = parentDoc.createElement('audio');
          a.id   = 'globalBgAudio';
          a.loop = true;
          a.style.display = 'none';
          var src = parentDoc.createElement('source');
          src.src  = "{uri}";
          src.type = 'audio/mpeg';
          a.appendChild(src);
          parentDoc.body.appendChild(a);
        }}

        // Restore saved playback position
        if (isNew) {{
          var savedTime = parseFloat(localStorage.getItem(keyTime) || 0) || 0;
          a.currentTime = savedTime;
        }}

        // ── Volume fade-in for a cinematic feel ──
        function fadeInAudio(audioEl) {{
          audioEl.volume = 0;
          var target = 0.8;
          var fade = setInterval(function() {{
            if (audioEl.volume < target) {{
              audioEl.volume = Math.min(target, audioEl.volume + 0.04);
            }} else {{
              clearInterval(fade);
            }}
          }}, 80);
        }}

        // ── Always play — no pause allowed ──
        function playAudio() {{
          a.play().then(function() {{
            fadeInAudio(a);
          }}).catch(function() {{
            /* Still blocked — will retry on next interaction */
          }});
        }}

        // ── Auto-play on FIRST user interaction anywhere on the page ──
        var interactionEvents = ['click','keydown','scroll','touchstart','pointerdown','mousemove'];
        var interactionFired  = false;

        function onFirstInteraction() {{
          if (interactionFired) return;
          interactionFired = true;
          interactionEvents.forEach(function(ev) {{
            parentDoc.removeEventListener(ev, onFirstInteraction, true);
          }});
          if (a.paused) playAudio();
        }}

        interactionEvents.forEach(function(ev) {{
          parentDoc.addEventListener(ev, onFirstInteraction, {{ capture: true, once: false }});
        }});

        // Immediate autoplay attempt
        if (a.paused) {{
          a.play().then(function() {{
            fadeInAudio(a);
            interactionFired = true;
          }}).catch(function() {{
            /* Blocked — onFirstInteraction will handle it */
          }});
        }}

        // ── Periodically save time and keep music alive ──
        setInterval(function() {{
          try {{
            if (!a.paused) {{
              localStorage.setItem(keyTime, a.currentTime.toString());
            }} else {{
              a.play().catch(function(){{}});
            }}
          }} catch(e) {{}}
        }}, 1000);

        // ── Hide this music component's own iframe ──
        var frame = window.frameElement;
        if (frame) {{
          frame.style.display  = 'none';
          frame.style.height   = '0px';
          frame.style.width    = '0px';
          frame.style.position = 'absolute';
          var parentContainer = frame.closest('div[data-testid="element-container"]');
          if (parentContainer) {{
            parentContainer.style.display = 'none';
            parentContainer.style.height  = '0px';
            parentContainer.style.margin  = '0';
            parentContainer.style.padding = '0';
          }}
        }}

      }} catch(e) {{
        console.error('Global music init failed:', e);
      }}
    }})();
    </script>
    """

    components.html(html, height=10, scrolling=False)
def main() -> None:
    inject_persistent_music()
    inject_global_styles()
    show_progress(st.session_state.stage, total=4)
    {
        1: stage_1, 2: stage_2, 3: stage_3,
        4: stage_5,
    }[st.session_state.stage]()
    show_navigation(st.session_state.stage, total=4)


if __name__ == "__main__":
    main()
