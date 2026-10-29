// FINN - Financial Investment Agent Mobile Client (v1.3.0)
let state = {
  priceThreshold: 3.0,
  volThreshold: 1.8,
  activeCategory: 'all',
  activeTicker: 'TATAMOTORS.NS',
  showRoutine: false,
  isPlayingAudio: false,
  audioSpeed: parseFloat(localStorage.getItem('finn_audio_speed')) || 1.0,
  lastAudioScript: '',
  speechSynthUtterance: null,
  currentTheme: 'midnight'
};

document.addEventListener('DOMContentLoaded', () => {
  initThemes();
  initNav();
  initThresholds();
  initCategoryFilters();
  initResearchModule();
  initAudioDispatch();
  initWhatsAppShare();
  initCopilotDrawer();
  
  // Initial data load
  loadDigest();
  loadAlerts();
  loadPortfolio();
  runResearch(state.activeTicker);
});

// Theme Management System
function initThemes() {
  const savedTheme = localStorage.getItem('finn_theme') || 'midnight';
  applyTheme(savedTheme);

  const toggleBtn = document.getElementById('theme-toggle-btn');
  const modal = document.getElementById('theme-modal');
  const closeBtn = document.getElementById('close-theme-btn');

  if (toggleBtn && modal) {
    toggleBtn.addEventListener('click', () => {
      modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  document.querySelectorAll('.theme-opt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const theme = btn.getAttribute('data-theme');
      applyTheme(theme);
      if (modal) modal.style.display = 'none';
      showToast(`Switched to ${theme.toUpperCase()} theme`);
    });
  });
}

function applyTheme(theme) {
  state.currentTheme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  document.body.setAttribute('data-theme', theme);
  localStorage.setItem('finn_theme', theme);

  const icons = {
    midnight: '🌙',
    light: '☀️',
    bloomberg: '📟',
    emerald: '🌲',
    cyberpunk: '⚡',
    matrix: '💻',
    solarized: '🌊',
    parchment: '📜',
    dracula: '🧛'
  };

  const iconEl = document.getElementById('theme-icon');
  if (iconEl) iconEl.textContent = icons[theme] || '🎨';

  document.querySelectorAll('.theme-opt-btn').forEach(btn => {
    if (btn.getAttribute('data-theme') === theme) {
      btn.style.borderColor = 'var(--accent-blue)';
      btn.style.boxShadow = '0 0 10px rgba(59, 130, 246, 0.3)';
    } else {
      btn.style.borderColor = 'var(--border-color)';
      btn.style.boxShadow = 'none';
    }
  });
}

// Navigation Handling
function initNav() {
  const navBtns = document.querySelectorAll('.nav-item');
  const panels = document.querySelectorAll('.view-panel');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      navBtns.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-target');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');

      if (targetId === 'view-alerts') loadAlerts();
      if (targetId === 'view-portfolio') loadPortfolio();
    });
  });
}

// 60-Second Audio Voice Dispatch
function initAudioDispatch() {
  const toggleBtn = document.getElementById('audio-dispatch-toggle');
  const banner = document.getElementById('audio-banner');
  const stopBtn = document.getElementById('stop-audio-btn');

  // Set initial active speed button
  document.querySelectorAll('.audio-speed-btn').forEach(btn => {
    const spd = parseFloat(btn.getAttribute('data-speed'));
    if (spd === state.audioSpeed) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }

    btn.addEventListener('click', () => {
      document.querySelectorAll('.audio-speed-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.audioSpeed = parseFloat(btn.getAttribute('data-speed'));
      localStorage.setItem('finn_audio_speed', state.audioSpeed);
      showToast(`Playback speed: ${state.audioSpeed}x`);

      if (state.isPlayingAudio && state.lastAudioScript) {
        playVoiceBriefing(state.lastAudioScript);
      }
    });
  });

  toggleBtn.addEventListener('click', async () => {
    if (state.isPlayingAudio) {
      stopAudio();
      return;
    }

    try {
      const res = await fetch('/api/audio-dispatch');
      const data = await res.json();
      state.lastAudioScript = data.script;
      playVoiceBriefing(data.script);
    } catch (e) {
      showToast('Error playing audio brief');
    }
  });

  stopBtn.addEventListener('click', stopAudio);
}

function playVoiceBriefing(text) {
  if (!('speechSynthesis' in window)) {
    showToast('Speech synthesis not supported in this browser');
    return;
  }

  state.lastAudioScript = text;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = state.audioSpeed || 1.0;
  utterance.pitch = 0.95;

  utterance.onstart = () => {
    state.isPlayingAudio = true;
    document.getElementById('audio-banner').style.display = 'flex';
    document.getElementById('audio-label').textContent = `${state.audioSpeed}x Playing`;
  };

  utterance.onend = stopAudio;
  utterance.onerror = stopAudio;

  state.speechSynthUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function stopAudio() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  state.isPlayingAudio = false;
  const banner = document.getElementById('audio-banner');
  if (banner) banner.style.display = 'none';
  const label = document.getElementById('audio-label');
  if (label) label.textContent = 'Listen 60s';
}

// WhatsApp / Telegram Share Memo
function initWhatsAppShare() {
  const copyBtn = document.getElementById('copy-memo-btn');
  copyBtn.addEventListener('click', async () => {
    try {
      const res = await fetch('/api/whatsapp-memo');
      const data = await res.json();
      await navigator.clipboard.writeText(data.memo);
      showToast('Copied WhatsApp Memo to Clipboard!');
    } catch (e) {
      showToast('Failed to copy memo');
    }
  });
}

function showToast(msg) {
  const toast = document.getElementById('toast-notify');
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { toast.style.display = 'none'; }, 2200);
}

// Interactive Financial Copilot
function initCopilotDrawer() {
  const floatBtn = document.getElementById('copilot-floating-btn');
  const drawer = document.getElementById('copilot-drawer');
  const closeBtn = document.getElementById('close-copilot-btn');
  const sendBtn = document.getElementById('copilot-send-btn');
  const input = document.getElementById('copilot-input');
  const pills = document.querySelectorAll('.copilot-pill');

  floatBtn.addEventListener('click', () => {
    drawer.style.display = drawer.style.display === 'none' ? 'block' : 'none';
    if (drawer.style.display === 'block') input.focus();
  });

  closeBtn.addEventListener('click', () => {
    drawer.style.display = 'none';
  });

  sendBtn.addEventListener('click', () => {
    if (input.value.trim()) handleCopilotQuery(input.value.trim());
  });

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && input.value.trim()) handleCopilotQuery(input.value.trim());
  });

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const q = pill.getAttribute('data-q');
      input.value = q;
      handleCopilotQuery(q);
    });
  });
}

async function handleCopilotQuery(query) {
  const history = document.getElementById('copilot-chat-history');
  const input = document.getElementById('copilot-input');
  input.value = '';

  // Append user message
  history.innerHTML += `
    <div style="background:#2563eb; color:#fff; padding:6px 10px; border-radius:8px 8px 0 8px; margin-bottom:6px; margin-left:20px; font-weight:600;">
      ${query}
    </div>
    <div id="copilot-loading" style="background:#1e293b; color:#94a3b8; padding:8px 10px; border-radius:8px; margin-bottom:6px; font-size:11px;">
      Searching primary filings & concall transcripts...
    </div>
  `;
  history.scrollTop = history.scrollHeight;

  try {
    const res = await fetch('/api/copilot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, ticker: state.activeTicker })
    });
    const data = await res.json();

    const loadingEl = document.getElementById('copilot-loading');
    if (loadingEl) loadingEl.remove();

    history.innerHTML += `
      <div style="background:#1e293b; border-left:3px solid #3b82f6; padding:8px 10px; border-radius:8px; margin-bottom:8px;">
        <div style="color:#e2e8f0; margin-bottom:4px;">${data.grounded_response}</div>
        <div style="font-size:9px; color:#38bdf8; font-family:monospace;">
          ${data.citations.map(c => `📄 Citation: ${c}`).join('<br>')}
        </div>
      </div>
    `;
    history.scrollTop = history.scrollHeight;
  } catch (err) {
    const loadingEl = document.getElementById('copilot-loading');
    if (loadingEl) loadingEl.remove();
    history.innerHTML += `<div style="color:#ef4444; font-size:11px; margin-bottom:6px;">Error: ${err.message}</div>`;
  }
}

// Threshold Configuration Modal
function initThresholds() {
  const toggleBtn = document.getElementById('threshold-toggle-btn');
  const modal = document.getElementById('threshold-modal');
  const closeBtn = document.getElementById('close-modal-btn');

  toggleBtn.addEventListener('click', () => {
    modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  document.querySelectorAll('.thresh-p-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.thresh-p-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.priceThreshold = parseFloat(btn.getAttribute('data-val'));
      updateThresholdDisplay();
      loadAlerts();
      loadPortfolio();
    });
  });

  document.querySelectorAll('.thresh-v-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.thresh-v-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.volThreshold = parseFloat(btn.getAttribute('data-val'));
      updateThresholdDisplay();
      loadAlerts();
      loadPortfolio();
    });
  });
}

function updateThresholdDisplay() {
  const text = `Vol >${state.volThreshold}x | ±${state.priceThreshold}%`;
  document.getElementById('active-thresholds-text').textContent = text;
}

// Category filter pills
function initCategoryFilters() {
  document.querySelectorAll('.filter-scroll .pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-scroll .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeCategory = btn.getAttribute('data-cat');
      loadDigest();
    });
  });

  const toggleRoutineBtn = document.getElementById('toggle-routine-btn');
  toggleRoutineBtn.addEventListener('click', () => {
    state.showRoutine = !state.showRoutine;
    const container = document.getElementById('routine-feed-container');
    container.style.display = state.showRoutine ? 'block' : 'none';
    toggleRoutineBtn.textContent = state.showRoutine ? '🔼 Hide Routine Paperwork' : '📁 Show Suppressed Routine Filings';
  });
}

// 1. PUSH MODE: THE WIRE (WINDOWED DIGEST)
async function loadDigest() {
  const container = document.getElementById('digest-feed-container');
  const routineContainer = document.getElementById('routine-feed-container');

  container.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b; font-size:12px;">Scanning portfolio filings...</div>';

  try {
    const res = await fetch(`/api/digest?window=24&category=${state.activeCategory}&include_routine=false`);
    const data = await res.json();

    if (!data.feed || data.feed.length === 0) {
      container.innerHTML = '<div style="text-align:center; padding:30px; color:#64748b; font-size:12px;">No material announcements in this filter window.</div>';
      return;
    }

    container.innerHTML = data.feed.map(item => renderAnnouncementCard(item)).join('');
    
    if (data.collapsed_routine && data.collapsed_routine.length > 0) {
      routineContainer.innerHTML = data.collapsed_routine.map(item => `
        <div style="background:#131b2e; border:1px solid #24324f; border-radius:8px; padding:8px 10px; margin-bottom:6px; font-size:11px;">
          <div style="display:flex; justify-content:space-between; color:#64748b; margin-bottom:2px;">
            <span style="font-weight:700;">${item.ticker}</span>
            <span style="font-size:8px;">ROUTINE FILING</span>
          </div>
          <div style="color:#94a3b8;">${item.title}</div>
        </div>
      `).join('');
    }
  } catch (err) {
    container.innerHTML = `<div style="color:#ef4444; font-size:12px; padding:20px;">Error loading digest: ${err.message}</div>`;
  }
}

function renderAnnouncementCard(item) {
  const cat = item.category || 'unclassified';
  const catClass = `cat-${cat.replace('_', '')}`;
  
  let metricsHtml = '';
  if (cat === 'results' && item.metrics) {
    const m = item.metrics;
    metricsHtml = `
      <div class="metrics-grid">
        <div class="metric-col">
          <div class="metric-label">Revenue</div>
          <div class="metric-value">₹${(m.revenue.current/1000).toFixed(1)}k Cr</div>
          <div class="metric-delta delta-up">+${m.revenue.yoy_pct}% YoY</div>
        </div>
        <div class="metric-col">
          <div class="metric-label">EBITDA</div>
          <div class="metric-value">₹${(m.ebitda.current/1000).toFixed(1)}k Cr</div>
          <div class="metric-delta delta-up">+${m.ebitda.yoy_pct}% YoY</div>
        </div>
        <div class="metric-col">
          <div class="metric-label">PBT</div>
          <div class="metric-value">₹${(m.pbt.current/1000).toFixed(1)}k Cr</div>
          <div class="metric-delta delta-up">+${m.pbt.yoy_pct}% YoY</div>
        </div>
        <div class="metric-col">
          <div class="metric-label">PAT</div>
          <div class="metric-value">₹${(m.pat.current/1000).toFixed(1)}k Cr</div>
          <div class="metric-delta delta-up">+${m.pat.yoy_pct}% YoY</div>
        </div>
      </div>
    `;
  }

  let execHtml = '';
  if (cat === 'management_change' && item.executive_enrichment) {
    const ex = item.executive_enrichment;
    execHtml = `
      <div class="executive-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div class="exec-name">👤 ${ex.person_name}</div>
          <span style="font-size:9px; background:#f59e0b20; color:#fbbf24; padding:2px 6px; border-radius:4px; font-weight:700;">PROFILED</span>
        </div>
        <div class="exec-role">${ex.role}</div>
        <div class="exec-detail"><strong>Prior:</strong> ${ex.previous_role}</div>
        <div class="exec-detail" style="margin-top:2px;"><strong>Pedigree:</strong> ${ex.education}</div>
      </div>
    `;
  }

  return `
    <article class="card">
      <div class="card-header">
        <div>
          <div class="company-title">${item.company || item.ticker}</div>
          <div class="ticker-tag">${item.ticker}</div>
        </div>
        <span class="category-tag ${catClass}">${cat.replace('_', ' ')}</span>
      </div>

      <div class="card-title">${item.title}</div>

      ${item.investor_takeaway ? `
        <div class="takeaway-box">
          ⚡ <strong>Takeaway:</strong> ${item.investor_takeaway}
        </div>
      ` : ''}

      ${metricsHtml}
      ${execHtml}

      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:10px; color:#64748b;">
        <span>${formatTime(item.timestamp)}</span>
        ${item.pdf_url ? `<a href="${item.pdf_url}" target="_blank" style="color:#38bdf8; text-decoration:none; font-weight:600;">Original Filing ↗</a>` : ''}
      </div>
    </article>
  `;
}

// 2. TRIGGERED ALERTS (with Sparklines)
async function loadAlerts() {
  const container = document.getElementById('alerts-container');
  container.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b; font-size:12px;">Evaluating live alert triggers...</div>';

  try {
    const res = await fetch(`/api/alerts?price_thresh=${state.priceThreshold}&vol_thresh=${state.volThreshold}`);
    const data = await res.json();

    if (!data.alerts || data.alerts.length === 0) {
      container.innerHTML = '<div style="text-align:center; padding:30px; color:#64748b; font-size:12px;">No threshold breaches currently detected.</div>';
      return;
    }

    container.innerHTML = data.alerts.map(alert => `
      <div class="card" style="border-left: 3px solid ${alert.severity === 'CRITICAL' ? '#ef4444' : '#f59e0b'};">
        <div class="card-header">
          <div>
            <span class="badge-alert">${alert.category.replace('_', ' ').toUpperCase()}</span>
            <div class="company-title" style="margin-top:4px;">${alert.company} (${alert.ticker})</div>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            ${alert.price_history ? renderSparklineSVG(alert.price_history) : ''}
            <span style="font-size:9px; font-family:monospace; color:#94a3b8;">${alert.severity}</span>
          </div>
        </div>
        <div style="font-size:12px; font-weight:700; color:#fff; margin-bottom:3px;">${alert.headline}</div>
        <div style="font-size:11px; color:#cbd5e1;">${alert.detail}</div>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<div style="color:#ef4444; font-size:12px; padding:20px;">Error loading alerts: ${err.message}</div>`;
  }
}

// 3. PULL RESEARCH & NARRATIVE VS NUMBERS
function initResearchModule() {
  const runBtn = document.getElementById('run-research-btn');
  const input = document.getElementById('research-ticker-input');

  runBtn.addEventListener('click', () => {
    if (input.value.trim()) runResearch(input.value.trim());
  });

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && input.value.trim()) runResearch(input.value.trim());
  });

  document.querySelectorAll('.chip-ticker').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.chip-ticker').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const sym = chip.getAttribute('data-sym');
      input.value = sym;
      runResearch(sym);
    });
  });
}

async function runResearch(ticker) {
  state.activeTicker = ticker;
  const container = document.getElementById('research-output-container');
  container.innerHTML = `
    <div style="text-align:center; padding:30px; color:#64748b; font-size:12px;">
      <div class="pulse-dot" style="margin: 0 auto 10px auto;"></div>
      Auditing Primary Concall Transcripts & Annual Reports for <strong>${ticker}</strong>...
    </div>
  `;

  try {
    const res = await fetch(`/api/research?ticker=${encodeURIComponent(ticker)}`);
    const data = await res.json();
    const r = data.research;

    container.innerHTML = `
      <!-- Company Snapshot -->
      <div class="card" style="margin-top:8px;">
        <div style="font-size:15px; font-weight:800; color:#fff;">${r.company_name}</div>
        <div style="font-size:11px; color:#94a3b8; margin-bottom:6px;">${r.sector}</div>
        <div style="font-size:11px; color:#cbd5e1; margin-bottom:6px;">${r.business_snapshot.summary}</div>
        <div style="font-size:10px; color:#38bdf8;"><strong>Segments:</strong> ${r.business_snapshot.revenue_mix}</div>
      </div>

      <!-- Credibility Score Gauge -->
      <div class="credibility-box">
        <div class="score-circle">${r.credibility_score.score}</div>
        <div>
          <div style="font-size:12px; font-weight:800; color:#fef08a;">${r.credibility_score.rating}</div>
          <div style="font-size:11px; color:#cbd5e1; line-height:1.35;">${r.credibility_score.commentary}</div>
        </div>
      </div>

      <!-- Narrative vs Numbers 4-Quarter Delivery Table -->
      <div class="research-section-title">
        <span>Narrative vs. Numbers</span>
        <span style="font-size:9px; color:#94a3b8;">Last 4 Quarters</span>
      </div>

      ${r.narrative_vs_numbers.map(item => `
        <div class="nvn-card">
          <div class="nvn-header">
            <span class="quarter-label">${item.quarter}</span>
            <span class="verdict-badge verdict-${item.verdict.replace(' ', '_')}">${item.verdict}</span>
          </div>
          <div class="guidance-text"><strong>Promised:</strong> ${item.management_guidance}</div>
          <div class="actual-text"><strong>Delivered:</strong> ${item.actual_delivered}</div>
          <div class="quote-source">Source: ${item.quote_source}</div>
        </div>
      `).join('')}

      <!-- Cash Quality & Conversion -->
      <div class="research-section-title">
        <span>Cash Quality & Conversion</span>
        <span style="font-size:9px; color:#10b981;">CFO/PAT: ${r.cash_quality.cfo_to_pat}</span>
      </div>
      <div class="card">
        <div style="font-size:11px; font-weight:700; color:#34d399; margin-bottom:3px;">${r.cash_quality.cash_conversion_verdict}</div>
        <div style="font-size:11px; color:#cbd5e1;">Free Cash Flow: ${r.cash_quality.fcf_generated}</div>
      </div>

      <!-- Bull vs Bear Thesis -->
      <div class="research-section-title">
        <span>Bull vs. Bear (Primary Grounded)</span>
      </div>
      <div class="thesis-grid">
        <div class="thesis-card bull-card">
          <div style="font-weight:800; margin-bottom:3px; color:#34d399;">🐂 BULL CASE</div>
          <ul style="padding-left:12px; margin:0;">
            ${r.bull_vs_bear.bull_case.map(pt => `<li style="margin-bottom:3px;">${pt}</li>`).join('')}
          </ul>
        </div>
        <div class="thesis-card bear-card">
          <div style="font-weight:800; margin-bottom:3px; color:#f87171;">🐻 BEAR CASE</div>
          <ul style="padding-left:12px; margin:0;">
            ${r.bull_vs_bear.bear_case.map(pt => `<li style="margin-bottom:3px;">${pt}</li>`).join('')}
          </ul>
        </div>
      </div>

      <!-- Primary Sources Checked -->
      <div style="margin-top:12px; padding:8px 10px; background:#111827; border-radius:8px; font-size:10px; color:#64748b;">
        <strong style="color:#94a3b8;">Primary Source Links Verified:</strong>
        <div style="margin-top:4px;">
          <a href="${r.annual_report_url}" target="_blank" style="color:#38bdf8; text-decoration:none; margin-right:12px;">Audited Annual Reports ↗</a>
          <a href="${r.concall_transcripts_url}" target="_blank" style="color:#38bdf8; text-decoration:none;">Concall Transcripts ↗</a>
        </div>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<div style="color:#ef4444; font-size:12px; padding:20px;">Error generating research: ${err.message}</div>`;
  }
}

// 4. PORTFOLIO RADAR (with Mini Sparklines)
async function loadPortfolio() {
  const container = document.getElementById('portfolio-container');
  container.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b; font-size:12px;">Fetching 20-day baseline metrics...</div>';

  try {
    const res = await fetch(`/api/portfolio?price_thresh=${state.priceThreshold}&vol_thresh=${state.volThreshold}`);
    const data = await res.json();

    container.innerHTML = data.data.map(stock => {
      const isUp = stock.pct_change >= 0;
      const isAnomalousVol = stock.is_unusual_volume;

      return `
        <div class="card" style="padding:9px 12px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <div style="flex:1;">
            <div style="font-size:13px; font-weight:700; color:#fff;">${stock.name}</div>
            <div style="font-size:10px; color:#94a3b8; font-family:monospace;">${stock.ticker} · ${stock.sector}</div>
          </div>
          
          <div style="margin: 0 10px;">
            ${renderSparklineSVG(stock.price_history || [100, 101, 102, 101, 103, 104])}
          </div>

          <div style="text-align:right;">
            <div style="font-size:13px; font-weight:700; font-family:monospace; color:${isUp ? '#10b981' : '#ef4444'};">
              ${isUp ? '+' : ''}${stock.pct_change}%
            </div>
            <div style="font-size:10px; color:${isAnomalousVol ? '#f59e0b' : '#64748b'}; font-weight:${isAnomalousVol ? '700' : '400'};">
              Vol: ${stock.volume_multiplier}x avg ${isAnomalousVol ? '⚡' : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    container.innerHTML = `<div style="color:#ef4444; font-size:12px; padding:20px;">Error loading portfolio: ${err.message}</div>`;
  }
}

// Mini SVG Sparkline Generator
function renderSparklineSVG(points) {
  if (!points || points.length < 2) return '';
  const min = Math.min(...points);
  const max = Math.max(...points);
  const range = max - min || 1;
  const height = 18;
  const width = 50;

  const coords = points.map((val, idx) => {
    const x = (idx / (points.length - 1)) * width;
    const y = height - ((val - min) / range) * height;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  const isUp = points[points.length - 1] >= points[0];
  const color = isUp ? '#10b981' : '#ef4444';

  return `
    <svg class="sparkline-svg" viewBox="0 0 ${width} ${height}">
      <polyline fill="none" stroke="${color}" stroke-width="1.8" points="${coords}" />
    </svg>
  `;
}

function formatTime(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ago';
}
