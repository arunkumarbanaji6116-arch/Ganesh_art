import base64
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, 'image.png')

with open(IMAGE_PATH, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#050205">
  <title>Lord Ganesha Art — Arun</title>
  <meta name="author" content="Arun">
  <meta property="og:title" content="Lord Ganesha Art — Arun">
  <meta property="og:description" content="Sacred Animated Particle Reveal Art created by Arun">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
      -webkit-user-select: none;
    }}
    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #050205;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    #canvas {{
      display: block;
      width: 100%;
      height: 100%;
      touch-action: none;
    }}

    /* =========================================
       ROTATE PHONE ANIMATION OVERLAY (PORTRAIT)
       ========================================= */
    #orientationOverlay {{
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at center, rgba(30, 18, 48, 0.97) 0%, rgba(5, 2, 8, 0.98) 100%);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      color: #fff;
      text-align: center;
      padding: 24px;
      transition: opacity 0.5s ease, visibility 0.5s ease;
    }}
    #orientationOverlay.hidden {{
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }}

    .rotate-anim-box {{
      position: relative;
      width: 150px;
      height: 150px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;
    }}

    /* Realistic Rotating Smartphone */
    .phone-mockup {{
      width: 60px;
      height: 110px;
      border: 3.5px solid #FFD700;
      border-radius: 14px;
      position: relative;
      box-shadow: 0 0 30px rgba(255, 215, 0, 0.45), inset 0 0 15px rgba(255, 215, 0, 0.2);
      background: linear-gradient(145deg, #1f1430, #0a0612);
      animation: rotatePhone 3.2s cubic-bezier(0.65, 0.05, 0.36, 1) infinite;
      transform-origin: center center;
    }}
    .phone-screen-inner {{
      position: absolute;
      top: 6px;
      bottom: 6px;
      left: 4px;
      right: 4px;
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.25), rgba(255, 90, 0, 0.2));
      border-radius: 7px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .phone-screen-inner::after {{
      content: '🕉';
      font-size: 22px;
      color: #FFD700;
      text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    }}
    .phone-speaker {{
      position: absolute;
      top: 3px;
      left: 50%;
      transform: translateX(-50%);
      width: 16px;
      height: 3px;
      background: #FFD700;
      border-radius: 2px;
    }}

    /* Circular rotation arrow orbit */
    .rotation-ring {{
      position: absolute;
      width: 136px;
      height: 136px;
      border: 2px dashed rgba(255, 215, 0, 0.4);
      border-top-color: #FFD700;
      border-radius: 50%;
      animation: spinRing 4s linear infinite;
    }}
    .rotation-arrow-head {{
      position: absolute;
      top: -6px;
      left: 50%;
      transform: translateX(-50%);
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-bottom: 9px solid #FFD700;
    }}

    @keyframes rotatePhone {{
      0%, 15% {{
        transform: rotate(0deg);
      }}
      50%, 75% {{
        transform: rotate(90deg);
      }}
      90%, 100% {{
        transform: rotate(0deg);
      }}
    }}

    @keyframes spinRing {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}

    .rotate-title {{
      font-size: 22px;
      font-weight: 700;
      color: #FFF2A8;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      text-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
    }}
    .rotate-desc {{
      font-size: 14px;
      color: #DDD0E8;
      line-height: 1.45;
      max-width: 290px;
      margin-bottom: 24px;
    }}
    .btn-continue-portrait {{
      background: rgba(255, 215, 0, 0.15);
      border: 1px solid rgba(255, 215, 0, 0.4);
      color: #FFE680;
      padding: 9px 20px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.2s ease;
    }}
    .btn-continue-portrait:active {{
      transform: scale(0.96);
      background: rgba(255, 215, 0, 0.25);
    }}

    /* =========================================
       SIDEBAR VIEW CONTROLS (VERTICAL DOCK)
       ========================================= */
    #sidebarContainer {{
      position: fixed;
      top: 50%;
      right: 0;
      transform: translateY(-50%);
      z-index: 100;
      display: flex;
      align-items: center;
      transition: transform 0.35s cubic-bezier(0.2, 0.9, 0.3, 1);
    }}
    #sidebarContainer.collapsed {{
      transform: translateY(-50%) translateX(142px);
    }}

    #sidebarTab {{
      width: 26px;
      height: 72px;
      background: rgba(14, 9, 22, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 215, 0, 0.35);
      border-right: none;
      border-radius: 10px 0 0 10px;
      color: #FFD700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 13px;
      box-shadow: -3px 0 12px rgba(0, 0, 0, 0.5);
      touch-action: manipulation;
    }}
    #sidebarTab:active {{
      background: rgba(255, 215, 0, 0.25);
    }}
    .tab-arrow {{
      display: inline-block;
      transition: transform 0.3s ease;
    }}
    #sidebarContainer.collapsed .tab-arrow {{
      transform: rotate(180deg);
    }}

    #sidebarPanel {{
      width: 142px;
      background: rgba(14, 9, 22, 0.85);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 215, 0, 0.35);
      border-right: none;
      border-radius: 12px 0 0 12px;
      padding: 12px 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: -6px 0 25px rgba(0, 0, 0, 0.6);
    }}

    .sidebar-header {{
      text-align: center;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }}
    .sidebar-title {{
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #D4AF37;
      font-weight: 700;
    }}
    .sidebar-speed-val {{
      font-size: 14px;
      font-weight: 700;
      color: #FFF2A8;
      margin-top: 3px;
    }}

    .speed-btn-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
    }}
    .sidebar-btn-half {{
      flex: 1;
      height: 28px;
      background: rgba(255, 215, 0, 0.12);
      border: 1px solid rgba(255, 215, 0, 0.28);
      color: #FFE680;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      touch-action: manipulation;
    }}
    .sidebar-btn-half:active {{
      background: rgba(255, 215, 0, 0.35);
      transform: scale(0.95);
    }}

    .sidebar-btn-full {{
      width: 100%;
      height: 30px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 215, 0, 0.22);
      color: #F0E6FF;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      cursor: pointer;
      touch-action: manipulation;
      transition: background 0.15s ease;
    }}
    .sidebar-btn-full:active {{
      background: rgba(255, 215, 0, 0.25);
      color: #FFF;
      transform: scale(0.96);
    }}

    /* Tap feedback indicator (Play/Pause) */
    #tapIndicator {{
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0.7);
      width: 65px;
      height: 65px;
      border-radius: 50%;
      background: rgba(15, 10, 22, 0.8);
      border: 1.5px solid rgba(255, 215, 0, 0.7);
      color: #FFD700;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      opacity: 0;
      pointer-events: none;
      transition: all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
      z-index: 50;
    }}
    #tapIndicator.active {{
      opacity: 1;
      transform: translate(-50%, -50%) scale(1.1);
    }}

    /* =========================================
       CLEARLY VISIBLE WATERMARK (BOTTOM-LEFT)
       ========================================= */
    #authorWatermark {{
      position: fixed;
      bottom: 16px;
      left: 16px;
      z-index: 90;
      background: rgba(14, 9, 22, 0.82);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1.5px solid rgba(255, 215, 0, 0.6);
      border-radius: 20px;
      padding: 6px 14px;
      display: flex;
      align-items: center;
      gap: 7px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.7), 0 0 12px rgba(255, 215, 0, 0.25);
      pointer-events: none;
    }}
    .watermark-icon {{
      font-size: 13px;
    }}
    .watermark-text {{
      font-size: 13px;
      font-weight: 700;
      color: #FFF2A8;
      letter-spacing: 0.6px;
      text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
    }}
  </style>
</head>
<body>

  <canvas id="canvas"></canvas>

  <!-- CLEARLY VISIBLE AUTHOR BADGE ON BOTTOM-LEFT -->
  <div id="authorWatermark">
    <span class="watermark-icon">✨</span>
    <span class="watermark-text">Arun</span>
  </div>

  <!-- PORTRAIT TO LANDSCAPE ROTATION MODAL -->
  <div id="orientationOverlay">
    <div class="rotate-anim-box">
      <div class="rotation-ring">
        <div class="rotation-arrow-head"></div>
      </div>
      <div class="phone-mockup">
        <div class="phone-speaker"></div>
        <div class="phone-screen-inner"></div>
      </div>
    </div>
    <div class="rotate-title">Lord Ganesha Visualizer</div>
    <div style="font-size:13px; color:#FFD700; font-weight:700; margin-bottom:10px; letter-spacing:0.5px;">✨ Arun</div>
    <div class="rotate-desc">For the most breathtaking wide view of Lord Ganesha, please turn your device to landscape mode.</div>
    <button class="btn-continue-portrait" id="btnContinuePortrait">Continue in Portrait</button>
  </div>

  <!-- SIDEBAR VIEW CONTROLS (VERTICAL DOCK) -->
  <div id="sidebarContainer">
    <div id="sidebarTab" title="Toggle Sidebar">
      <span class="tab-arrow">❯</span>
    </div>
    <div id="sidebarPanel">
      <div class="sidebar-header">
        <div class="sidebar-title">Arun</div>
        <div class="sidebar-speed-val" id="lblSpeed">Speed: 1.0x</div>
      </div>
      <div class="speed-btn-row">
        <button class="sidebar-btn-half" id="btnSpeedDown" title="Slower">-</button>
        <button class="sidebar-btn-half" id="btnSpeedUp" title="Faster">+</button>
      </div>
      <button class="sidebar-btn-full" id="btnPauseResume">⏸ Pause</button>
      <button class="sidebar-btn-full" id="btnSkip">⏭ Skip Phase</button>
      <button class="sidebar-btn-full" id="btnRestart">🔄 Restart</button>
      <button class="sidebar-btn-full" id="btnFullscreen">⛶ Fullscreen</button>
    </div>
  </div>

  <div id="tapIndicator">⏸</div>

  <script>
    // Embedded Base64 Image
    const IMAGE_DATA = "data:image/png;base64,{img_b64}";

    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d', {{ alpha: false }});
    
    let screenW = window.innerWidth;
    let screenH = window.innerHeight;

    // Simulation state (Default 1.0x)
    let speedMultiplier = 1.0;
    let paused = false;
    let phase = 1; // 1: outlines, 2: tiles, 3: glow & petals

    let imageLoaded = false;
    let mainImg = new Image();
    mainImg.crossOrigin = "anonymous";
    mainImg.src = IMAGE_DATA;

    // Offscreen buffers
    let scaledW = 0, scaledH = 0, offsetX = 0, offsetY = 0;
    let offscreenColor = document.createElement('canvas');
    let offColorCtx = offscreenColor.getContext('2d');
    
    let revealedCanvas = document.createElement('canvas');
    let revCtx = revealedCanvas.getContext('2d');

    // Particle queues
    let outlineTargets = [];
    let revealTargets = [];
    let activeParticles = [];
    let bgParticles = [];

    const MAX_ACTIVE_PARTICLES = 4500;
    const TILE_SIZE = 3; // Optimized for crisp mobile 60fps

    // Realistic flame centers tailored for lamps in image
    const flameRatios = [
      {{ rx: 0.205, ry: 0.555 }}, {{ rx: 0.231, ry: 0.535 }}, {{ rx: 0.252, ry: 0.555 }},
      {{ rx: 0.748, ry: 0.555 }}, {{ rx: 0.772, ry: 0.540 }}, {{ rx: 0.795, ry: 0.555 }},
      {{ rx: 0.145, ry: 0.870 }}, {{ rx: 0.201, ry: 0.890 }}, {{ rx: 0.258, ry: 0.810 }},
      {{ rx: 0.740, ry: 0.835 }}, {{ rx: 0.798, ry: 0.890 }}, {{ rx: 0.855, ry: 0.880 }}
    ];
    let flameCenters = [];

    // Setup Canvas Resolution
    function resizeCanvas() {{
      screenW = window.innerWidth;
      screenH = window.innerHeight;
      canvas.width = screenW;
      canvas.height = screenH;

      checkOrientation();

      if (imageLoaded) {{
        initVisualizer();
      }}
    }}

    // Orientation checking & modal handling
    const orientationOverlay = document.getElementById('orientationOverlay');
    let userDismissedPortrait = false;

    function checkOrientation() {{
      const isPortrait = window.innerHeight > window.innerWidth;
      if (isPortrait && !userDismissedPortrait) {{
        orientationOverlay.classList.remove('hidden');
      }} else {{
        orientationOverlay.classList.add('hidden');
      }}
    }}

    document.getElementById('btnContinuePortrait').addEventListener('click', () => {{
      userDismissedPortrait = true;
      orientationOverlay.classList.add('hidden');
    }});

    window.addEventListener('resize', resizeCanvas);
    window.addEventListener('orientationchange', () => {{
      setTimeout(resizeCanvas, 200);
    }});

    // Initialize Targets and Scale
    function initVisualizer() {{
      const origW = mainImg.naturalWidth || mainImg.width || 1024;
      const origH = mainImg.naturalHeight || mainImg.height || 535;

      const scale = Math.min(screenW / origW, screenH / origH);
      scaledW = Math.max(10, Math.floor(origW * scale));
      scaledH = Math.max(10, Math.floor(origH * scale));
      offsetX = Math.floor((screenW - scaledW) / 2);
      offsetY = Math.floor((screenH - scaledH) / 2);

      // Setup color buffer
      offscreenColor.width = scaledW;
      offscreenColor.height = scaledH;
      offColorCtx.drawImage(mainImg, 0, 0, scaledW, scaledH);

      // Setup persistent revealed canvas
      revealedCanvas.width = screenW;
      revealedCanvas.height = screenH;
      revCtx.clearRect(0, 0, screenW, screenH);

      // Compute flame centers in screen coords
      flameCenters = flameRatios.map(r => ({{
        x: Math.floor(scaledW * r.rx) + offsetX,
        y: Math.floor(scaledH * r.ry) + offsetY
      }}));

      // Sobel Edge Detection for Golden Outlines
      const imgData = offColorCtx.getImageData(0, 0, scaledW, scaledH);
      const data = imgData.data;

      outlineTargets = [];
      const lum = new Uint8Array(scaledW * scaledH);
      for (let i = 0, j = 0; i < data.length; i += 4, j++) {{
        lum[j] = (data[i] * 77 + data[i + 1] * 150 + data[i + 2] * 29) >> 8;
      }}

      // Sample step 2 for clean, serene golden outlines
      for (let y = 1; y < scaledH - 1; y += 2) {{
        for (let x = 1; x < scaledW - 1; x += 2) {{
          const idx = y * scaledW + x;
          const gx = (lum[idx + 1] - lum[idx - 1]);
          const gy = (lum[idx + scaledW] - lum[idx - scaledW]);
          const mag = Math.abs(gx) + Math.abs(gy);
          if (mag > 45) {{
            outlineTargets.push({{ x: x + offsetX, y: y + offsetY }});
          }}
        }}
      }}

      // Reveal Targets
      revealTargets = [];
      for (let y = 0; y < scaledH; y += TILE_SIZE) {{
        for (let x = 0; x < scaledW; x += TILE_SIZE) {{
          revealTargets.push({{
            imgX: x,
            imgY: y,
            x: x + offsetX,
            y: y + offsetY
          }});
        }}
      }}

      // Sort ascending by y so bottom pops first
      outlineTargets.sort((a, b) => a.y - b.y);
      revealTargets.sort((a, b) => a.y - b.y);

      activeParticles = [];
      bgParticles = [];
      phase = 1;
    }}

    mainImg.onload = () => {{
      imageLoaded = true;
      resizeCanvas();
      requestAnimationFrame(gameLoop);
    }};

    // Flower petal drawing helper
    function drawFlower(c, x, y, baseColor, size) {{
      c.save();
      c.translate(x, y);
      const center = 0;
      const petalRadius = Math.max(2, size / 3);
      for (let angle = 0; angle < 360; angle += 45) {{
        const rad = angle * Math.PI / 180;
        const px = Math.cos(rad) * (size / 3.5);
        const py = Math.sin(rad) * (size / 3.5);
        c.beginPath();
        c.arc(px, py, petalRadius, 0, Math.PI * 2);
        c.fillStyle = baseColor;
        c.fill();
      }}
      c.beginPath();
      c.arc(0, 0, Math.max(2, petalRadius - 1), 0, Math.PI * 2);
      c.fillStyle = '#FFD700';
      c.fill();
      c.restore();
    }}

    // Animation Loop
    let lastTime = performance.now();
    function gameLoop(now) {{
      requestAnimationFrame(gameLoop);

      const dt = Math.min(64, now - lastTime);
      lastTime = now;

      // Dark sacred background
      ctx.fillStyle = '#050205';
      ctx.fillRect(0, 0, screenW, screenH);

      // Phase 1: Glowing Pastel Aura
      if (phase === 1) {{
        const hue = Math.floor((now / 40) % 360);
        const auraGrad = ctx.createRadialGradient(
          screenW / 2, screenH * 0.45, 10,
          screenW / 2, screenH * 0.45, Math.max(screenW, screenH) * 0.55
        );
        auraGrad.addColorStop(0, `hsla(${{hue}}, 60%, 75%, 0.18)`);
        auraGrad.addColorStop(0.5, `hsla(${{hue}}, 50%, 65%, 0.08)`);
        auraGrad.addColorStop(1, 'rgba(5, 2, 8, 0)');
        ctx.fillStyle = auraGrad;
        ctx.fillRect(0, 0, screenW, screenH);
      }}

      // Blit already revealed artwork
      ctx.drawImage(revealedCanvas, 0, 0);

      // Particle update (gentle, graceful motion at 1.0x)
      if (!paused) {{
        const surviving = [];
        for (let i = 0; i < activeParticles.length; i++) {{
          const p = activeParticles[i];
          if (p.state === 'falling') {{
            p.y += p.speed * 1.5;
            if (p.y >= screenH) {{
              p.y = screenH;
              p.state = 'rising';
            }}
            // Render while falling
            if (p.type === 'tile') {{
              ctx.drawImage(offscreenColor, p.imgX, p.imgY, TILE_SIZE, TILE_SIZE, p.x, p.y, TILE_SIZE, TILE_SIZE);
            }} else {{
              ctx.fillStyle = '#FFD700';
              ctx.fillRect(p.x, p.y, 1.5, 1.5);
            }}
            surviving.push(p);
          }} else if (p.state === 'rising') {{
            p.y -= p.speed;
            if (p.y <= p.targetY) {{
              // Reached destination: commit to persistent revealedCanvas
              if (p.type === 'tile') {{
                revCtx.drawImage(offscreenColor, p.imgX, p.imgY, TILE_SIZE, TILE_SIZE, p.targetX, p.targetY, TILE_SIZE, TILE_SIZE);
              }} else {{
                revCtx.fillStyle = '#FFD700';
                revCtx.fillRect(p.targetX, p.targetY, 1.5, 1.5);
              }}
            }} else {{
              if (p.type === 'tile') {{
                ctx.drawImage(offscreenColor, p.imgX, p.imgY, TILE_SIZE, TILE_SIZE, p.x, p.y, TILE_SIZE, TILE_SIZE);
              }} else {{
                ctx.fillStyle = '#FFD700';
                ctx.fillRect(p.x, p.y, 1.5, 1.5);
              }}
              surviving.push(p);
            }}
          }}
        }}
        activeParticles = surviving;

        // Particle Spawning (slower, serene flow)
        if (phase === 1) {{
          const canSpawn = Math.max(0, MAX_ACTIVE_PARTICLES - activeParticles.length);
          const spawnCount = Math.min(canSpawn, Math.floor(380 * speedMultiplier));
          for (let i = 0; i < spawnCount && outlineTargets.length > 0; i++) {{
            const t = outlineTargets.pop();
            activeParticles.push({{
              type: 'outline',
              x: t.x,
              y: -Math.random() * 80 - 10,
              targetX: t.x,
              targetY: t.y,
              speed: (3.2 + Math.random() * 4.2) * speedMultiplier,
              state: 'falling'
            }});
          }}
          if (outlineTargets.length === 0 && activeParticles.length === 0) {{
            phase = 2;
          }}
        }} else if (phase === 2) {{
          const canSpawn = Math.max(0, MAX_ACTIVE_PARTICLES - activeParticles.length);
          const spawnCount = Math.min(canSpawn, Math.floor(300 * speedMultiplier));
          for (let i = 0; i < spawnCount && revealTargets.length > 0; i++) {{
            const t = revealTargets.pop();
            activeParticles.push({{
              type: 'tile',
              imgX: t.imgX,
              imgY: t.imgY,
              x: t.x,
              y: -Math.random() * 120 - 10,
              targetX: t.x,
              targetY: t.y,
              speed: (3.5 + Math.random() * 4.5) * speedMultiplier,
              state: 'falling'
            }});
          }}
          if (revealTargets.length === 0 && activeParticles.length === 0) {{
            phase = 3;
          }}
        }}
      }}

      // Phase 3: Sacred Diya / Lamp Flame Glow
      if (phase >= 3) {{
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < flameCenters.length; i++) {{
          const fc = flameCenters[i];
          const pulse = Math.sin(now * 0.005 + i);
          const radius = Math.max(6, Math.floor(11 + pulse * 4.5));
          const shakeX = fc.x + (Math.random() - 0.5) * 1.2;
          const shakeY = fc.y + (Math.random() - 0.5) * 1.2;

          const flameGrad = ctx.createRadialGradient(shakeX, shakeY, radius * 0.1, shakeX, shakeY, radius * 1.8);
          flameGrad.addColorStop(0, 'rgba(255, 255, 220, 0.9)');
          flameGrad.addColorStop(0.3, 'rgba(255, 190, 50, 0.6)');
          flameGrad.addColorStop(0.7, 'rgba(255, 80, 0, 0.25)');
          flameGrad.addColorStop(1, 'rgba(255, 30, 0, 0)');

          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.arc(shakeX, shakeY, radius * 1.8, 0, Math.PI * 2);
          ctx.fill();
        }}
        ctx.restore();
      }}

      // Flower Petals & Divine Glitter (gentle, peaceful float)
      if (phase >= 2 && !paused) {{
        if (Math.random() < 0.06 * Math.min(2.0, speedMultiplier)) {{
          const isFlower = Math.random() < 0.5;
          bgParticles.push({{
            isFlower: isFlower,
            color: isFlower ? ['#FF1493', '#00DC78', '#4182FF', '#FFD700', '#FF7F00'][Math.floor(Math.random() * 5)] : '#FFD700',
            size: isFlower ? Math.floor(8 + Math.random() * 5) : Math.floor(2 + Math.random() * 3),
            x: Math.random() * screenW,
            y: -20,
            speedY: (0.9 + Math.random() * 1.6) * speedMultiplier,
            wobbleSpeed: 0.002 + Math.random() * 0.0025,
            wobbleOffset: Math.random() * Math.PI * 2,
            wobbleWidth: 0.8 + Math.random() * 1.0
          }});
        }}
      }}

      const survivingBg = [];
      for (let i = 0; i < bgParticles.length; i++) {{
        const p = bgParticles[i];
        if (!paused) {{
          p.y += p.speedY;
        }}
        const drawX = p.x + Math.sin(now * p.wobbleSpeed + p.wobbleOffset) * p.wobbleWidth * 16;

        if (p.y < screenH + 20) {{
          if (p.isFlower) {{
            drawFlower(ctx, drawX, p.y, p.color, p.size);
          }} else {{
            ctx.beginPath();
            ctx.arc(drawX, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
          }}
          survivingBg.push(p);
        }}
      }}
      bgParticles = survivingBg;
    }}

    // Touch Feedback & Canvas Tap
    const tapIndicator = document.getElementById('tapIndicator');
    function triggerTapFeedback(symbol) {{
      tapIndicator.textContent = symbol;
      tapIndicator.classList.add('active');
      setTimeout(() => tapIndicator.classList.remove('active'), 400);
    }}

    canvas.addEventListener('click', (e) => {{
      paused = !paused;
      triggerTapFeedback(paused ? '⏸' : '▶');
      updatePauseButton();
    }});

    // Sidebar View Controls Handling
    const lblSpeed = document.getElementById('lblSpeed');
    const btnPauseResume = document.getElementById('btnPauseResume');
    const sidebarContainer = document.getElementById('sidebarContainer');
    const sidebarTab = document.getElementById('sidebarTab');

    function updatePauseButton() {{
      btnPauseResume.textContent = paused ? '▶ Play' : '⏸ Pause';
    }}

    // Toggle Sidebar collapse / expand
    sidebarTab.addEventListener('click', (e) => {{
      e.stopPropagation();
      sidebarContainer.classList.toggle('collapsed');
    }});

    document.getElementById('btnSpeedUp').addEventListener('click', (e) => {{
      e.stopPropagation();
      speedMultiplier = Math.min(5.0, Math.round((speedMultiplier + 0.25) * 100) / 100);
      lblSpeed.textContent = `Speed: ${{speedMultiplier.toFixed(1)}}x`;
    }});

    document.getElementById('btnSpeedDown').addEventListener('click', (e) => {{
      e.stopPropagation();
      speedMultiplier = Math.max(0.25, Math.round((speedMultiplier - 0.25) * 100) / 100);
      lblSpeed.textContent = `Speed: ${{speedMultiplier.toFixed(1)}}x`;
    }});

    btnPauseResume.addEventListener('click', (e) => {{
      e.stopPropagation();
      paused = !paused;
      updatePauseButton();
    }});

    document.getElementById('btnSkip').addEventListener('click', (e) => {{
      e.stopPropagation();
      if (phase === 1) {{
        outlineTargets = [];
        activeParticles = [];
        phase = 2;
      }} else if (phase === 2) {{
        revCtx.drawImage(offscreenColor, 0, 0, scaledW, scaledH, offsetX, offsetY, scaledW, scaledH);
        revealTargets = [];
        activeParticles = [];
        phase = 3;
      }}
    }});

    document.getElementById('btnRestart').addEventListener('click', (e) => {{
      e.stopPropagation();
      initVisualizer();
      paused = false;
      updatePauseButton();
    }});

    document.getElementById('btnFullscreen').addEventListener('click', (e) => {{
      e.stopPropagation();
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }});

    // Desktop Keyboard shortcuts
    window.addEventListener('keydown', (e) => {{
      if (e.key === ' ' || e.code === 'Space') {{
        paused = !paused;
        updatePauseButton();
      }} else if (e.key === 'ArrowUp' || e.key === '+') {{
        speedMultiplier = Math.min(5.0, Math.round((speedMultiplier + 0.25) * 100) / 100);
        lblSpeed.textContent = `Speed: ${{speedMultiplier.toFixed(1)}}x`;
      }} else if (e.key === 'ArrowDown' || e.key === '-') {{
        speedMultiplier = Math.max(0.25, Math.round((speedMultiplier - 0.25) * 100) / 100);
        lblSpeed.textContent = `Speed: ${{speedMultiplier.toFixed(1)}}x`;
      }} else if (e.key === 'f' || e.key === 'F') {{
        document.getElementById('btnSkip').click();
      }} else if (e.key === 'r' || e.key === 'R') {{
        document.getElementById('btnRestart').click();
      }} else if (e.key === 'h' || e.key === 'H') {{
        sidebarContainer.classList.toggle('collapsed');
      }}
    }});
  </script>
</body>
</html>
'''

output_path = os.path.join(SCRIPT_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Generated standalone index.html at {output_path} (Size: {os.path.getsize(output_path) / 1024:.1f} KB)")
