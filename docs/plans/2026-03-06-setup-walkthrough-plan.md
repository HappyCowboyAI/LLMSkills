# Setup Walkthrough Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the plain-text Setup tab content with an animated, platform-specific setup walkthrough showing CSS-drawn UI mockups of Claude.ai, Claude Code, and ChatGPT.

**Architecture:** A `SetupWalkthrough` class renders inside the existing Setup tab panel (`data-panel="setup"`). Each supported platform gets a sub-tab that initializes a platform-specific animation sequence using CSS-drawn UI mockups. All data comes from existing `skills.json` fields (`setupSteps`, `instructions`, `name`, `projectKnowledgeFiles`, `mcpTools`).

**Tech Stack:** Vanilla JS, CSS (no libraries). All changes in `docs/index.html`.

---

### Task 1: Add Setup Walkthrough CSS

**Files:**
- Modify: `docs/index.html:504-703` (add new CSS after existing walkthrough styles, before `</style>`)

**Context:** The existing `SkillWalkthrough` uses dark terminal styling. The setup walkthrough needs platform-specific mockup styles: browser chrome, sidebar panels, form fields, terminal windows. These CSS classes will be used by the JS in Tasks 3-5.

**Step 1: Add CSS for shared setup walkthrough structure**

Insert the following CSS block after line 703 (after the `.wt-parallel-label` rule, before `</style>`):

```css
/* ── Setup Walkthrough ── */
.setup-wt {
  position: relative;
}
.setup-wt-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--pai-light-gray);
}
.setup-wt-tab {
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: var(--pai-dark-gray);
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}
.setup-wt-tab:hover { color: var(--pai-primary-blue); }
.setup-wt-tab.active {
  color: var(--pai-primary-blue);
  border-bottom-color: var(--pai-primary-blue);
}
.setup-wt-tab.disabled {
  opacity: 0.4;
  cursor: default;
}

/* Shared mockup frame */
.setup-mockup {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,32,78,0.12);
  margin-bottom: 20px;
  min-height: 340px;
  position: relative;
}

/* Browser chrome shared */
.mock-browser-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  font-size: 12px;
}
.mock-dots {
  display: flex;
  gap: 6px;
}
.mock-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.mock-dots span:nth-child(1) { background: #FF5F57; }
.mock-dots span:nth-child(2) { background: #FFBD2E; }
.mock-dots span:nth-child(3) { background: #28C840; }
.mock-url-bar {
  flex: 1;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-family: 'SF Mono', 'Consolas', monospace;
}

/* ── Claude.ai mockup ── */
.mock-claude {
  background: #F5F0EA;
  color: #2D2B28;
}
.mock-claude .mock-browser-bar {
  background: #E8E0D5;
}
.mock-claude .mock-url-bar {
  background: #F5F0EA;
  color: #8B7E6E;
}
.mock-claude-body {
  display: flex;
  height: 300px;
}
.mock-claude-sidebar {
  width: 200px;
  background: #EDE7DD;
  padding: 16px 12px;
  font-size: 12px;
  border-right: 1px solid #DDD5C8;
  flex-shrink: 0;
}
.mock-claude-sidebar-item {
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 2px;
  cursor: default;
  color: #5D5549;
  transition: background 0.2s;
}
.mock-claude-sidebar-item.active {
  background: #D4C9B8;
  font-weight: 600;
  color: #2D2B28;
}
.mock-claude-sidebar-item.highlighted {
  background: rgba(191, 131, 62, 0.2);
  box-shadow: 0 0 0 2px rgba(191, 131, 62, 0.5);
  animation: setupPulse 1.5s ease-in-out infinite;
}
.mock-claude-main {
  flex: 1;
  padding: 20px;
  overflow: hidden;
  position: relative;
}

/* Claude dialog / form elements */
.mock-claude-dialog {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
}
.mock-claude-dialog.visible {
  opacity: 1;
  transform: translateY(0);
}
.mock-field-label {
  font-size: 11px;
  font-weight: 600;
  color: #8B7E6E;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.mock-text-field {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #DDD5C8;
  border-radius: 6px;
  font-size: 13px;
  color: #2D2B28;
  background: #FAF7F2;
  margin-bottom: 12px;
  min-height: 32px;
}
.mock-text-field.highlighted {
  border-color: rgba(191, 131, 62, 0.6);
  box-shadow: 0 0 0 2px rgba(191, 131, 62, 0.2);
}
.mock-textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #DDD5C8;
  border-radius: 6px;
  font-size: 11px;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #5D5549;
  background: #FAF7F2;
  min-height: 80px;
  line-height: 1.4;
  white-space: pre-wrap;
  overflow: hidden;
  margin-bottom: 12px;
}
.mock-textarea.highlighted {
  border-color: rgba(191, 131, 62, 0.6);
  box-shadow: 0 0 0 2px rgba(191, 131, 62, 0.2);
}
.mock-file-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #EDE7DD;
  border-radius: 4px;
  font-size: 11px;
  color: #5D5549;
  margin: 2px 4px 2px 0;
  opacity: 0;
  transition: opacity 0.3s;
}
.mock-file-chip.visible { opacity: 1; }
.mock-toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-top: 1px solid #EDE7DD;
}
.mock-toggle {
  width: 36px;
  height: 20px;
  border-radius: 10px;
  background: #D4D4D4;
  position: relative;
  transition: background 0.3s;
}
.mock-toggle.on { background: #BF833E; }
.mock-toggle::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  transition: left 0.3s;
}
.mock-toggle.on::after { left: 18px; }

/* Claude chat input */
.mock-claude-chat {
  position: absolute;
  bottom: 16px;
  left: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  align-items: center;
}
.mock-claude-chat-input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 20px;
  border: 1px solid #DDD5C8;
  background: white;
  font-size: 13px;
  color: #2D2B28;
}
.mock-claude-chat-send {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #BF833E;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s;
}
.mock-claude-chat-send.visible { opacity: 1; }

/* ── Claude Code / Terminal mockup ── */
.mock-terminal {
  background: #1E1E2E;
  color: #CDD6F4;
}
.mock-terminal .mock-browser-bar {
  background: #181825;
}
.mock-terminal .mock-url-bar {
  background: #1E1E2E;
  color: #6C7086;
}
.mock-terminal-body {
  padding: 16px;
  font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 12px;
  line-height: 1.6;
  height: 300px;
  overflow: hidden;
}
.mock-terminal-line {
  opacity: 0;
  transition: opacity 0.3s;
  white-space: pre-wrap;
}
.mock-terminal-line.visible { opacity: 1; }
.mock-terminal-prompt { color: #A6E3A1; }
.mock-terminal-cmd { color: #CDD6F4; }
.mock-terminal-comment { color: #6C7086; }
.mock-terminal-success { color: #A6E3A1; }
.mock-terminal-file-content {
  color: #89B4FA;
  padding-left: 16px;
  border-left: 2px solid #313244;
  margin: 4px 0;
}

/* ── ChatGPT mockup ── */
.mock-chatgpt {
  background: #FFFFFF;
  color: #343541;
}
.mock-chatgpt .mock-browser-bar {
  background: #F7F7F8;
  border-bottom: 1px solid #E5E5E5;
}
.mock-chatgpt .mock-url-bar {
  background: #ECECF1;
  color: #8E8EA0;
}
.mock-chatgpt-body {
  display: flex;
  height: 300px;
}
.mock-chatgpt-sidebar {
  width: 180px;
  background: #202123;
  padding: 12px 8px;
  font-size: 12px;
  color: #ECECF1;
  flex-shrink: 0;
}
.mock-chatgpt-sidebar-item {
  padding: 8px 10px;
  border-radius: 6px;
  margin-bottom: 2px;
  color: #C5C5D2;
  cursor: default;
  transition: background 0.2s;
}
.mock-chatgpt-sidebar-item.active {
  background: #343541;
  color: #ECECF1;
}
.mock-chatgpt-sidebar-item.highlighted {
  background: rgba(16, 163, 127, 0.2);
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.5);
  animation: setupPulse 1.5s ease-in-out infinite;
}
.mock-chatgpt-main {
  flex: 1;
  padding: 20px;
  overflow: hidden;
  position: relative;
}
.mock-chatgpt-form {
  background: #F7F7F8;
  border-radius: 10px;
  padding: 20px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
}
.mock-chatgpt-form.visible {
  opacity: 1;
  transform: translateY(0);
}
.mock-gpt-field-label {
  font-size: 11px;
  font-weight: 600;
  color: #8E8EA0;
  margin-bottom: 4px;
}
.mock-gpt-text-field {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  font-size: 13px;
  color: #343541;
  background: white;
  margin-bottom: 12px;
}
.mock-gpt-text-field.highlighted {
  border-color: #10A37F;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2);
}
.mock-gpt-textarea {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  font-size: 11px;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #6E6E80;
  background: white;
  min-height: 80px;
  line-height: 1.4;
  white-space: pre-wrap;
  overflow: hidden;
  margin-bottom: 12px;
}
.mock-gpt-textarea.highlighted {
  border-color: #10A37F;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2);
}
.mock-gpt-action-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background: white;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  margin-bottom: 4px;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
}
.mock-gpt-action-item.visible { opacity: 1; }
.mock-gpt-action-status {
  font-size: 10px;
  color: #10A37F;
  font-weight: 600;
}

/* ChatGPT chat input */
.mock-chatgpt-chat {
  position: absolute;
  bottom: 16px;
  left: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  align-items: center;
}
.mock-chatgpt-chat-input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 20px;
  border: 1px solid #E5E5E5;
  background: white;
  font-size: 13px;
  color: #343541;
}
.mock-chatgpt-chat-send {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #10A37F;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s;
}
.mock-chatgpt-chat-send.visible { opacity: 1; }

/* ── Setup walkthrough controls ── */
.setup-wt-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 0;
}
.setup-wt-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid var(--pai-light-gray);
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: var(--pai-dark-gray);
  transition: all 0.2s;
}
.setup-wt-btn:hover {
  border-color: var(--pai-primary-blue);
  color: var(--pai-primary-blue);
  background: var(--pai-light-blue);
}
.setup-wt-btn.primary {
  background: var(--pai-primary-blue);
  color: white;
  border-color: var(--pai-primary-blue);
  width: 44px;
  height: 44px;
  font-size: 16px;
}
.setup-wt-btn.primary:hover {
  background: var(--pai-dark-blue);
}
.setup-wt-dots {
  display: flex;
  gap: 6px;
}
.setup-wt-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--pai-light-gray);
  transition: all 0.3s;
}
.setup-wt-dot.active {
  background: var(--pai-primary-blue);
  transform: scale(1.3);
}
.setup-wt-dot.done {
  background: var(--pai-teal);
}

/* Step description below mockup */
.setup-wt-step-desc {
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--pai-dark-blue);
  margin-bottom: 4px;
  min-height: 21px;
}
.setup-wt-step-detail {
  text-align: center;
  font-size: 12px;
  color: var(--pai-dark-gray);
  min-height: 18px;
}

/* Pulse animation for highlighted elements */
@keyframes setupPulse {
  0%, 100% { box-shadow: 0 0 0 2px rgba(191, 131, 62, 0.5); }
  50% { box-shadow: 0 0 0 4px rgba(191, 131, 62, 0.3); }
}
.mock-chatgpt-sidebar-item.highlighted {
  animation-name: setupPulseGreen;
}
@keyframes setupPulseGreen {
  0%, 100% { box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.5); }
  50% { box-shadow: 0 0 0 4px rgba(16, 163, 127, 0.3); }
}

/* Copy button in setup walkthrough */
.setup-wt-copy-btn {
  display: none;
  margin: 12px auto 0;
  padding: 8px 20px;
  border-radius: var(--radius);
  background: var(--pai-primary-blue);
  color: white;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.setup-wt-copy-btn.visible { display: inline-flex; align-items: center; gap: 6px; }
.setup-wt-copy-btn:hover { background: var(--pai-dark-blue); }
```

**Step 2: Verify the styles render**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 -c "import re; t=open('index.html').read(); print('setup-wt' in t, 'mock-claude' in t, 'mock-terminal' in t, 'mock-chatgpt' in t)"`
Expected: `True True True True`

**Step 3: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: add CSS for setup walkthrough platform mockups"
```

---

### Task 2: Add SetupWalkthrough JS Class — Core Structure

**Files:**
- Modify: `docs/index.html` — insert new class after the `SkillWalkthrough` class (which ends around line 1627)

**Context:** The `SkillWalkthrough` class ends with a closing `}`. Insert the new `SetupWalkthrough` class right after it. This class manages platform sub-tabs, step progression, and delegates rendering to platform-specific methods (added in Tasks 3-5).

**Step 1: Add the SetupWalkthrough class**

Insert after the closing `}` of `SkillWalkthrough` class:

```javascript
// ── Setup Walkthrough Component ──
class SetupWalkthrough {
  constructor(skill, container) {
    this.skill = skill;
    this.container = container;
    this.currentStep = -1;
    this.totalSteps = 0;
    this.playing = false;
    this.timer = null;
    this.platformId = null;
    this.mockupEl = null;
  }

  init() {
    // Find available platforms for this skill
    const allPlatforms = catalogData.catalog.platforms;
    this.availablePlatforms = allPlatforms.filter(p =>
      p.status === 'supported' && this.skill.platforms[p.id] !== null
    );

    if (this.availablePlatforms.length === 0) return;

    this.render();
    // Auto-select first platform
    this.selectPlatform(this.availablePlatforms[0].id);
  }

  render() {
    this.container.innerHTML = `
      <h3 style="margin-bottom:16px;color:var(--pai-dark-blue);">Setup Walkthrough</h3>
      <div class="setup-wt">
        <div class="setup-wt-tabs">
          ${this.availablePlatforms.map(p => `
            <div class="setup-wt-tab" data-platform="${p.id}">${p.name}</div>
          `).join('')}
        </div>
        <div class="setup-mockup-area"></div>
        <div class="setup-wt-step-desc"></div>
        <div class="setup-wt-step-detail"></div>
        <button class="setup-wt-copy-btn">Copy Instructions</button>
        <div class="setup-wt-controls">
          <button class="setup-wt-btn" data-action="prev">&#9664;</button>
          <button class="setup-wt-btn primary" data-action="play">&#9654;</button>
          <div class="setup-wt-dots"></div>
          <button class="setup-wt-btn" data-action="next">&#9654;</button>
        </div>
      </div>`;

    // Bind tab clicks
    this.container.querySelectorAll('.setup-wt-tab').forEach(tab => {
      tab.onclick = () => this.selectPlatform(tab.dataset.platform);
    });

    // Bind control clicks
    this.container.querySelector('[data-action="prev"]').onclick = () => this.stepBack();
    this.container.querySelector('[data-action="play"]').onclick = () => this.togglePlay();
    this.container.querySelector('[data-action="next"]').onclick = () => this.stepForward();

    // Bind copy button
    this.container.querySelector('.setup-wt-copy-btn').onclick = () => {
      const data = this.skill.platforms[this.platformId];
      if (data) copyToClipboard(data.instructions);
    };

    this.mockupArea = this.container.querySelector('.setup-mockup-area');
    this.descEl = this.container.querySelector('.setup-wt-step-desc');
    this.detailEl = this.container.querySelector('.setup-wt-step-detail');
    this.dotsEl = this.container.querySelector('.setup-wt-dots');
    this.copyBtn = this.container.querySelector('.setup-wt-copy-btn');
  }

  selectPlatform(platformId) {
    this.stop();
    this.platformId = platformId;
    this.currentStep = -1;

    // Update tab styling
    this.container.querySelectorAll('.setup-wt-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.platform === platformId);
    });

    // Build platform mockup and steps
    this.buildMockup();
    this.renderDots();
    this.updateDesc();
    this.copyBtn.classList.remove('visible');
  }

  buildMockup() {
    this.mockupArea.innerHTML = '';
    if (this.platformId === 'claude-project') {
      this.buildClaudeMockup();
    } else if (this.platformId === 'claude-code') {
      this.buildTerminalMockup();
    } else if (this.platformId === 'chatgpt-gpt') {
      this.buildChatgptMockup();
    }
  }

  // Platform-specific build methods added in Tasks 3-5
  buildClaudeMockup() { this.steps = []; this.totalSteps = 0; }
  buildTerminalMockup() { this.steps = []; this.totalSteps = 0; }
  buildChatgptMockup() { this.steps = []; this.totalSteps = 0; }

  renderDots() {
    let html = '';
    for (let i = 0; i < this.totalSteps; i++) {
      const cls = i === this.currentStep ? 'active' : (i < this.currentStep ? 'done' : '');
      html += `<div class="setup-wt-dot ${cls}"></div>`;
    }
    this.dotsEl.innerHTML = html;
  }

  updateDesc() {
    if (this.currentStep < 0 || this.currentStep >= this.steps.length) {
      this.descEl.textContent = 'Click play or step forward to begin';
      this.detailEl.textContent = '';
      return;
    }
    const step = this.steps[this.currentStep];
    this.descEl.textContent = step.title;
    this.detailEl.textContent = step.detail || '';
  }

  async stepForward() {
    if (this.currentStep >= this.totalSteps - 1) {
      this.stop();
      return;
    }
    this.currentStep++;
    this.renderDots();
    this.updateDesc();

    const step = this.steps[this.currentStep];
    if (step && step.animate) {
      await step.animate();
    }

    // Show copy button on paste step
    if (step && step.showCopy) {
      this.copyBtn.classList.add('visible');
    } else {
      this.copyBtn.classList.remove('visible');
    }
  }

  stepBack() {
    if (this.currentStep <= 0) return;
    this.stop();
    // Reset and replay up to currentStep - 1
    const target = this.currentStep - 1;
    this.currentStep = -1;
    this.buildMockup();
    this.copyBtn.classList.remove('visible');
    // Fast-forward to target step
    const fastForward = async () => {
      for (let i = 0; i <= target; i++) {
        this.currentStep = i;
        this.renderDots();
        this.updateDesc();
        const step = this.steps[i];
        if (step && step.animate) await step.animate();
        if (step && step.showCopy) this.copyBtn.classList.add('visible');
        else this.copyBtn.classList.remove('visible');
      }
    };
    fastForward();
  }

  togglePlay() {
    if (this.playing) {
      this.stop();
    } else {
      this.playing = true;
      this.container.querySelector('[data-action="play"]').innerHTML = '&#9646;&#9646;';
      this.autoStep();
    }
  }

  async autoStep() {
    if (!this.playing) return;
    await this.stepForward();
    if (this.currentStep >= this.totalSteps - 1) {
      this.stop();
      return;
    }
    this.timer = setTimeout(() => this.autoStep(), 2000);
  }

  stop() {
    this.playing = false;
    if (this.timer) clearTimeout(this.timer);
    this.timer = null;
    const btn = this.container.querySelector('[data-action="play"]');
    if (btn) btn.innerHTML = '&#9654;';
  }

  // Shared animation helpers
  async wait(ms) { return new Promise(r => setTimeout(r, ms)); }

  async typeText(el, text, speed = 30) {
    el.textContent = '';
    for (let i = 0; i < text.length; i++) {
      el.textContent = text.substring(0, i + 1);
      await this.wait(speed);
    }
  }

  truncateInstructions(text, lines = 6) {
    const arr = text.split('\n').slice(0, lines);
    return arr.join('\n') + '\n...';
  }
}
```

**Step 2: Verify the class is parseable**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 -c "t=open('index.html').read(); print('class SetupWalkthrough' in t, 'buildClaudeMockup' in t, 'autoStep' in t)"`
Expected: `True True True`

**Step 3: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: add SetupWalkthrough class core structure"
```

---

### Task 3: Implement Claude.ai Project Mockup

**Files:**
- Modify: `docs/index.html` — replace the stub `buildClaudeMockup()` method

**Context:** This renders a CSS mockup of the Claude.ai interface and defines 6 animated steps. The `this.steps` array drives the animation. Each step has `{title, detail, animate, showCopy?}`.

**Step 1: Replace the `buildClaudeMockup` stub**

Find the line `buildClaudeMockup() { this.steps = []; this.totalSteps = 0; }` and replace it with:

```javascript
buildClaudeMockup() {
    const skill = this.skill;
    const instructions = skill.platforms['claude-project']?.instructions || '';
    const truncated = this.truncateInstructions(instructions);
    const files = skill.projectKnowledgeFiles || [];

    this.mockupArea.innerHTML = `
      <div class="setup-mockup mock-claude">
        <div class="mock-browser-bar">
          <div class="mock-dots"><span></span><span></span><span></span></div>
          <div class="mock-url-bar">claude.ai</div>
        </div>
        <div class="mock-claude-body">
          <div class="mock-claude-sidebar">
            <div style="font-weight:700;font-size:11px;color:#8B7E6E;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Projects</div>
            <div class="mock-claude-sidebar-item" data-item="projects">My Projects</div>
            <div class="mock-claude-sidebar-item" data-item="recents">Recents</div>
            <div class="mock-claude-sidebar-item" data-item="starred">Starred</div>
          </div>
          <div class="mock-claude-main">
            <div class="mock-claude-dialog" data-dialog="create">
              <div class="mock-field-label">Project Name</div>
              <div class="mock-text-field" data-field="name"></div>
              <div class="mock-field-label">Custom Instructions</div>
              <div class="mock-textarea" data-field="instructions"></div>
              <div data-section="files" style="display:none;">
                <div class="mock-field-label">Knowledge Files</div>
                <div data-field="files"></div>
              </div>
              <div data-section="mcp" style="display:none;">
                <div class="mock-field-label">Integrations</div>
                <div class="mock-toggle-row">
                  <span style="font-size:12px;">Backstory MCP</span>
                  <div class="mock-toggle" data-toggle="mcp"></div>
                </div>
              </div>
            </div>
            <div class="mock-claude-chat" style="display:none;" data-section="chat">
              <div class="mock-claude-chat-input" data-field="chat"></div>
              <div class="mock-claude-chat-send">&#8593;</div>
            </div>
          </div>
        </div>
      </div>`;

    const sidebar = this.mockupArea.querySelector('[data-item="projects"]');
    const dialog = this.mockupArea.querySelector('[data-dialog="create"]');
    const nameField = this.mockupArea.querySelector('[data-field="name"]');
    const instrField = this.mockupArea.querySelector('[data-field="instructions"]');
    const filesSection = this.mockupArea.querySelector('[data-section="files"]');
    const filesField = this.mockupArea.querySelector('[data-field="files"]');
    const mcpSection = this.mockupArea.querySelector('[data-section="mcp"]');
    const mcpToggle = this.mockupArea.querySelector('[data-toggle="mcp"]');
    const chatSection = this.mockupArea.querySelector('[data-section="chat"]');
    const chatInput = this.mockupArea.querySelector('[data-field="chat"]');
    const chatSend = this.mockupArea.querySelector('.mock-claude-chat-send');

    this.steps = [
      {
        title: 'Open Projects',
        detail: 'Click "Projects" in the sidebar',
        animate: async () => {
          sidebar.classList.add('highlighted');
          await this.wait(600);
          sidebar.classList.remove('highlighted');
          sidebar.classList.add('active');
        }
      },
      {
        title: 'Create New Project',
        detail: `Name your project "${skill.name}"`,
        animate: async () => {
          dialog.classList.add('visible');
          nameField.classList.add('highlighted');
          await this.wait(300);
          await this.typeText(nameField, skill.name);
          nameField.classList.remove('highlighted');
        }
      },
      {
        title: 'Paste Custom Instructions',
        detail: 'Copy and paste the skill instructions',
        showCopy: true,
        animate: async () => {
          instrField.classList.add('highlighted');
          await this.wait(300);
          await this.typeText(instrField, truncated, 10);
          instrField.classList.remove('highlighted');
        }
      },
      {
        title: 'Upload Knowledge Files',
        detail: files.length ? `Upload ${files.length} file(s) from assets/` : 'No knowledge files needed for this skill',
        animate: async () => {
          filesSection.style.display = 'block';
          if (files.length > 0) {
            for (const f of files) {
              const chip = document.createElement('span');
              chip.className = 'mock-file-chip';
              chip.textContent = f;
              filesField.appendChild(chip);
              await this.wait(200);
              chip.classList.add('visible');
            }
          } else {
            filesField.innerHTML = '<span style="font-size:12px;color:#8B7E6E;">No files needed</span>';
          }
        }
      },
      {
        title: 'Connect Backstory MCP',
        detail: 'Enable the MCP integration in project settings',
        animate: async () => {
          mcpSection.style.display = 'block';
          await this.wait(400);
          mcpToggle.classList.add('on');
        }
      },
      {
        title: 'Start Using the Skill',
        detail: 'Type an account name to begin',
        animate: async () => {
          dialog.classList.remove('visible');
          chatSection.style.display = 'flex';
          await this.wait(300);
          const example = skill.walkthrough?.input?.example || 'Acme Corp';
          await this.typeText(chatInput, example);
          chatSend.classList.add('visible');
        }
      }
    ];
    this.totalSteps = this.steps.length;
  }
```

**Step 2: Verify**

Open `http://localhost:8080/#/skill/01-account-plan-agent`, click Setup tab, click the Claude.ai Project sub-tab, and click Play. The Claude.ai mockup should animate through 6 steps.

**Step 3: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: implement Claude.ai Project setup mockup animation"
```

---

### Task 4: Implement Claude Code Terminal Mockup

**Files:**
- Modify: `docs/index.html` — replace the stub `buildTerminalMockup()` method

**Context:** This renders a terminal UI mockup showing 4 steps: open terminal, edit CLAUDE.md, verify MCP, invoke skill.

**Step 1: Replace the `buildTerminalMockup` stub**

Find the line `buildTerminalMockup() { this.steps = []; this.totalSteps = 0; }` and replace it with:

```javascript
buildTerminalMockup() {
    const skill = this.skill;
    const instructions = skill.platforms['claude-code']?.instructions || '';
    const truncated = this.truncateInstructions(instructions, 4);
    const tools = skill.mcpTools || [];

    this.mockupArea.innerHTML = `
      <div class="setup-mockup mock-terminal">
        <div class="mock-browser-bar">
          <div class="mock-dots"><span></span><span></span><span></span></div>
          <div class="mock-url-bar">Terminal — claude-code</div>
        </div>
        <div class="mock-terminal-body" data-body></div>
      </div>`;

    const body = this.mockupArea.querySelector('[data-body]');

    const addLine = (html, cls = '') => {
      const line = document.createElement('div');
      line.className = 'mock-terminal-line ' + cls;
      line.innerHTML = html;
      body.appendChild(line);
      return line;
    };

    this.steps = [
      {
        title: 'Open Terminal',
        detail: 'Launch Claude Code in your project directory',
        animate: async () => {
          const l1 = addLine('<span class="mock-terminal-prompt">$</span> <span class="mock-terminal-cmd">claude</span>');
          l1.classList.add('visible');
          await this.wait(400);
          const l2 = addLine('<span class="mock-terminal-success">Claude Code v1.x loaded</span>');
          l2.classList.add('visible');
          await this.wait(200);
          const l3 = addLine('<span class="mock-terminal-comment"># Ready for instructions</span>');
          l3.classList.add('visible');
        }
      },
      {
        title: 'Add Instructions to CLAUDE.md',
        detail: 'Paste skill instructions into your project config',
        showCopy: true,
        animate: async () => {
          const l1 = addLine('<span class="mock-terminal-prompt">$</span> <span class="mock-terminal-cmd">cat >> CLAUDE.md</span>');
          l1.classList.add('visible');
          await this.wait(300);
          const lines = truncated.split('\n');
          for (const line of lines) {
            const lEl = addLine(`<span class="mock-terminal-file-content">${line}</span>`);
            lEl.classList.add('visible');
            await this.wait(80);
          }
        }
      },
      {
        title: 'Verify MCP Connection',
        detail: 'Confirm Backstory MCP is available',
        animate: async () => {
          const l1 = addLine('<span class="mock-terminal-prompt">$</span> <span class="mock-terminal-cmd">claude mcp list</span>');
          l1.classList.add('visible');
          await this.wait(500);
          const l2 = addLine('<span class="mock-terminal-success">Backstory MCP ✓ Connected</span>');
          l2.classList.add('visible');
          await this.wait(200);
          if (tools.length) {
            const toolStr = tools.slice(0, 5).join(', ');
            const l3 = addLine(`<span class="mock-terminal-comment">  Tools: ${toolStr}</span>`);
            l3.classList.add('visible');
          }
        }
      },
      {
        title: 'Invoke the Skill',
        detail: 'Start using the skill with an account name',
        animate: async () => {
          const example = skill.walkthrough?.input?.example || 'Acme Corp';
          const l1 = addLine(`<span class="mock-terminal-prompt">&gt;</span> <span class="mock-terminal-cmd">${example}</span>`);
          l1.classList.add('visible');
          await this.wait(600);
          const l2 = addLine('<span class="mock-terminal-success">Running skill... ✓</span>');
          l2.classList.add('visible');
        }
      }
    ];
    this.totalSteps = this.steps.length;
  }
```

**Step 2: Verify**

Open `http://localhost:8080/#/skill/01-account-plan-agent`, click Setup tab, click the Claude Code sub-tab, and click Play. The terminal mockup should animate through 4 steps.

**Step 3: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: implement Claude Code terminal setup mockup animation"
```

---

### Task 5: Implement ChatGPT Custom GPT Mockup

**Files:**
- Modify: `docs/index.html` — replace the stub `buildChatgptMockup()` method

**Context:** This renders a ChatGPT GPT builder mockup with 5 steps: explore/create, name, instructions, actions, test.

**Step 1: Replace the `buildChatgptMockup` stub**

Find the line `buildChatgptMockup() { this.steps = []; this.totalSteps = 0; }` and replace it with:

```javascript
buildChatgptMockup() {
    const skill = this.skill;
    const instructions = skill.platforms['chatgpt-gpt']?.instructions || '';
    const truncated = this.truncateInstructions(instructions);
    const tools = skill.mcpTools || [];

    this.mockupArea.innerHTML = `
      <div class="setup-mockup mock-chatgpt">
        <div class="mock-browser-bar">
          <div class="mock-dots"><span></span><span></span><span></span></div>
          <div class="mock-url-bar">chatgpt.com/gpts/editor</div>
        </div>
        <div class="mock-chatgpt-body">
          <div class="mock-chatgpt-sidebar">
            <div style="font-weight:600;font-size:11px;color:#8E8EA0;margin-bottom:8px;padding:0 10px;">ChatGPT</div>
            <div class="mock-chatgpt-sidebar-item" data-item="explore">Explore GPTs</div>
            <div class="mock-chatgpt-sidebar-item" data-item="my-gpts">My GPTs</div>
            <div class="mock-chatgpt-sidebar-item" data-item="create">+ Create</div>
          </div>
          <div class="mock-chatgpt-main">
            <div class="mock-chatgpt-form" data-form="builder">
              <div style="font-weight:700;font-size:15px;margin-bottom:16px;">Create a GPT</div>
              <div class="mock-gpt-field-label">Name</div>
              <div class="mock-gpt-text-field" data-field="name"></div>
              <div class="mock-gpt-field-label">Instructions</div>
              <div class="mock-gpt-textarea" data-field="instructions"></div>
              <div data-section="actions" style="display:none;">
                <div class="mock-gpt-field-label">Actions</div>
                <div data-field="actions"></div>
              </div>
            </div>
            <div class="mock-chatgpt-chat" style="display:none;" data-section="chat">
              <div class="mock-chatgpt-chat-input" data-field="chat"></div>
              <div class="mock-chatgpt-chat-send">&#8593;</div>
            </div>
          </div>
        </div>
      </div>`;

    const createItem = this.mockupArea.querySelector('[data-item="create"]');
    const form = this.mockupArea.querySelector('[data-form="builder"]');
    const nameField = this.mockupArea.querySelector('[data-field="name"]');
    const instrField = this.mockupArea.querySelector('[data-field="instructions"]');
    const actionsSection = this.mockupArea.querySelector('[data-section="actions"]');
    const actionsField = this.mockupArea.querySelector('[data-field="actions"]');
    const chatSection = this.mockupArea.querySelector('[data-section="chat"]');
    const chatInput = this.mockupArea.querySelector('[data-field="chat"]');
    const chatSend = this.mockupArea.querySelector('.mock-chatgpt-chat-send');

    this.steps = [
      {
        title: 'Create a New GPT',
        detail: 'Click "Explore GPTs" then "Create"',
        animate: async () => {
          createItem.classList.add('highlighted');
          await this.wait(600);
          createItem.classList.remove('highlighted');
          createItem.classList.add('active');
          form.classList.add('visible');
        }
      },
      {
        title: 'Name Your GPT',
        detail: `Enter "${skill.name}"`,
        animate: async () => {
          nameField.classList.add('highlighted');
          await this.wait(300);
          await this.typeText(nameField, skill.name);
          nameField.classList.remove('highlighted');
        }
      },
      {
        title: 'Paste Instructions',
        detail: 'Copy the skill instructions and paste them in',
        showCopy: true,
        animate: async () => {
          instrField.classList.add('highlighted');
          await this.wait(300);
          await this.typeText(instrField, truncated, 10);
          instrField.classList.remove('highlighted');
        }
      },
      {
        title: 'Configure Actions',
        detail: 'Add Backstory API endpoints as actions',
        animate: async () => {
          actionsSection.style.display = 'block';
          const actionTools = tools.length > 0 ? tools.slice(0, 6) : ['find_account', 'get_scorecard', 'get_engaged_people'];
          for (const tool of actionTools) {
            const item = document.createElement('div');
            item.className = 'mock-gpt-action-item';
            item.innerHTML = `<span>${tool}</span><span class="mock-gpt-action-status">Configured</span>`;
            actionsField.appendChild(item);
            await this.wait(250);
            item.classList.add('visible');
          }
        }
      },
      {
        title: 'Save & Test',
        detail: 'Try the GPT with an account name',
        animate: async () => {
          form.classList.remove('visible');
          chatSection.style.display = 'flex';
          await this.wait(300);
          const example = skill.walkthrough?.input?.example || 'Acme Corp';
          await this.typeText(chatInput, example);
          chatSend.classList.add('visible');
        }
      }
    ];
    this.totalSteps = this.steps.length;
  }
```

**Step 2: Verify**

Open `http://localhost:8080/#/skill/01-account-plan-agent`, click Setup tab, click the ChatGPT Custom GPT sub-tab, and click Play. The ChatGPT mockup should animate through 5 steps.

**Step 3: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: implement ChatGPT Custom GPT setup mockup animation"
```

---

### Task 6: Wire SetupWalkthrough into the Setup Tab

**Files:**
- Modify: `docs/index.html:1046-1056` — replace the existing setup tab panel content
- Modify: `docs/index.html:1063-1068` — add SetupWalkthrough initialization after walkthrough init

**Context:** The existing Setup tab panel (lines 1046-1056) renders plain `<ol>` lists per platform. Replace this with a container div, then initialize a `SetupWalkthrough` instance when the detail view renders.

**Step 1: Replace the setup tab panel**

Find this block (around lines 1046-1056):

```javascript
      <div class="tab-content" data-panel="setup" style="display:none">
        <h3 style="margin-bottom:16px;color:var(--pai-dark-blue);">Setup by Platform</h3>
        ${allPlatforms.filter(p => skill.platforms[p.id]).map(p => `
          <div style="margin-bottom:20px;">
            <h4 style="margin-bottom:8px;color:var(--pai-primary-blue);">${p.name}</h4>
            <ol class="setup-steps">
              ${skill.platforms[p.id].setupSteps.map(step => `<li>${step}</li>`).join('')}
            </ol>
          </div>
        `).join('')}
      </div>
```

Replace with:

```javascript
      <div class="tab-content" data-panel="setup" style="display:none">
        <div id="setup-walkthrough-container"></div>
      </div>
```

**Step 2: Add SetupWalkthrough initialization**

Find the block that initializes SkillWalkthrough (around lines 1063-1068):

```javascript
  // Initialize walkthrough if available
  if (skill.walkthrough) {
    const wtContainer = document.getElementById('walkthrough-container');
    const wt = new SkillWalkthrough(skill, wtContainer);
    wt.init();
  }
```

Add the SetupWalkthrough initialization right after it:

```javascript
  // Initialize setup walkthrough
  const setupContainer = document.getElementById('setup-walkthrough-container');
  if (setupContainer) {
    const setupWt = new SetupWalkthrough(skill, setupContainer);
    setupWt.init();
  }
```

**Step 3: Verify end-to-end**

Open `http://localhost:8080/#/skill/01-account-plan-agent`, click the Setup tab. Should see platform sub-tabs (Claude.ai Project, Claude Code, ChatGPT Custom GPT) and an animated mockup area with play/step controls.

**Step 4: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "feat: wire SetupWalkthrough into Setup tab replacing plain-text steps"
```

---

### Task 7: Polish and Cross-Skill Testing

**Files:**
- Modify: `docs/index.html` (minor adjustments as needed)

**Context:** Verify the setup walkthrough works across multiple skills, handles edge cases (skills with no ChatGPT instructions, skills with no knowledge files), and looks correct visually.

**Step 1: Test skills with different platform availability**

Test the following skills by navigating to their detail pages and clicking the Setup tab:
1. `01-account-plan-agent` — should have all 3 platforms
2. Check a skill that may only have 1-2 platforms — tabs should only show available ones
3. Check a skill with no `projectKnowledgeFiles` — the upload step should say "No files needed"

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 -c "
import json
data = json.load(open('skills.json'))
for s in data['skills'][:5]:
    platforms = [k for k,v in s['platforms'].items() if v]
    files = s.get('projectKnowledgeFiles', [])
    print(f\"{s['id']}: platforms={platforms}, files={len(files)}\")"`

**Step 2: Fix any visual issues**

Adjust CSS if needed for:
- Mockup height on different screen sizes
- Text truncation in small mockups
- Tab styling alignment with existing tabs

**Step 3: Verify the "See it in action" link and the Setup walkthrough don't conflict**

Both should work independently: the tool walkthrough at the bottom (from `SkillWalkthrough`) and the setup walkthrough inside the Setup tab (from `SetupWalkthrough`).

**Step 4: Commit**

```bash
cd /Users/scottmetcalf/projects/LLMSkills && git add docs/index.html && git commit -m "fix: polish setup walkthrough and verify cross-skill compatibility"
```
