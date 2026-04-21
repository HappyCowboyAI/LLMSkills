# Skill Walkthrough Component — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add animated, interactive walkthroughs to each skill's detail page in the catalog, auto-generated from skill.md files, with an MCP connection simulation as Step 0.

**Architecture:** Build-time extraction of walkthrough structure from skill.md into skills.json, client-side JS component renders step-by-step animation with auto-generated mock data (overridable per skill via walkthrough-data.json).

**Tech Stack:** Python 3 (build script), vanilla JS/CSS (catalog UI), JSON (data)

---

### Task 1: Add `extract_walkthrough()` to build-catalog.py

**Files:**
- Modify: `docs/build-catalog.py:42-85` (add new function after `get_category`)
- Modify: `docs/build-catalog.py:150-195` (call it in `build_catalog`)

**Step 1: Add the `extract_walkthrough` function**

Add this function after `get_category()` (after line 46) in `docs/build-catalog.py`:

```python
def extract_walkthrough(skill_dir: Path) -> dict | None:
    """Extract walkthrough structure from skill.md."""
    skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        return None

    text = skill_md.read_text()

    # Extract input type from SOURCE.md
    source_meta = parse_source_md(skill_dir / "SOURCE.md")
    input_label = source_meta.get("input", "Account name")

    # Map input labels to example values
    input_examples = {
        "account name": "Acme Corp",
        "opportunity name": "Acme Enterprise Renewal",
        "account name and opportunity": "Acme Corp",
        "account name, then opportunity selection": "Acme Corp",
    }
    example_input = input_examples.get(input_label.lower(), "Acme Corp")

    # Extract workflow steps from ### Step N headings
    step_pattern = r"### Step (\d+):?\s*(.+?)(?=\n)"
    step_matches = re.finditer(step_pattern, text)

    steps = []
    for match in step_matches:
        step_num = int(match.group(1))
        step_title = match.group(2).strip()

        # Get the content between this step heading and the next ### heading
        start = match.end()
        next_heading = re.search(r"\n### ", text[start:])
        end = start + next_heading.start() if next_heading else len(text)
        step_content = text[start:end]

        # Check if this step mentions parallel execution
        parallel = bool(re.search(r"parallel|simultaneous", step_content, re.IGNORECASE))

        # Extract backticked tool names (Backstory MCP tool pattern)
        tool_names = re.findall(r"`((?:find_|get_|ask_|account_|top_)\w+)`", step_content)

        if tool_names:
            for tool_name in tool_names:
                # Extract description: text after the tool name on the same line
                desc_match = re.search(
                    rf"`{re.escape(tool_name)}`\s*[—\-]+\s*(.+?)(?:\n|$)",
                    step_content,
                )
                desc = desc_match.group(1).strip() if desc_match else step_title
                steps.append({
                    "type": "tool",
                    "name": tool_name,
                    "description": desc,
                    "parallel": parallel,
                    "stepNum": step_num,
                })
        else:
            # Non-tool step (analysis, scoring, output generation)
            steps.append({
                "type": "analysis",
                "title": step_title,
                "stepNum": step_num,
            })

    # Extract output section headings (#### or ##### in the output template area)
    # Look for content after "Deliver" or "Report Format" or "Dashboard" step
    output_pattern = r"(?:####|#####)\s+(.+?)(?:\n)"
    output_sections = re.findall(output_pattern, text)
    # Filter out common non-output headings
    output_sections = [
        s.strip() for s in output_sections
        if not re.match(r"step\s+\d+", s, re.IGNORECASE)
    ]

    # Check for optional walkthrough-data.json
    has_custom_data = (skill_dir / "assets" / "walkthrough-data.json").exists()

    if not steps:
        return None

    return {
        "input": {"label": input_label, "example": example_input},
        "steps": steps,
        "outputSections": output_sections,
        "hasCustomData": has_custom_data,
    }
```

**Step 2: Wire it into `build_catalog()`**

In `docs/build-catalog.py`, inside the `for skill_dir in skill_dirs:` loop, after the `"projectKnowledgeFiles"` line (around line 192), add the walkthrough extraction:

```python
        # Extract walkthrough structure
        walkthrough = extract_walkthrough(skill_dir)
```

And add it to the skill dict (after `"platforms": platforms,`):

```python
            "walkthrough": walkthrough,
```

**Step 3: Run the build script and verify output**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 build-catalog.py`

Expected: Script runs without errors, prints 19 skills. Verify with:

Run: `python3 -c "import json; d=json.load(open('skills.json')); s=d['skills'][0]; print(json.dumps(s.get('walkthrough'), indent=2))"`

Expected: JSON output showing steps with `find_account`, `get_account_status`, etc. for the Account Plan Agent.

**Step 4: Commit**

```bash
git add docs/build-catalog.py docs/skills.json
git commit -m "feat: extract walkthrough structure from skill.md into skills.json

Adds extract_walkthrough() to build-catalog.py that parses each skill.md
for workflow steps, MCP tool calls, parallel execution markers, and output
section headings. Data is added as a 'walkthrough' key per skill in
skills.json.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: Add walkthrough CSS to index.html

**Files:**
- Modify: `docs/index.html:496-503` (add CSS before closing `</style>`)

**Step 1: Add walkthrough styles**

Insert before the closing `</style>` tag (line 503) in `docs/index.html`:

```css
  /* Walkthrough */
  .walkthrough {
    background: var(--pai-dark-blue);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 20px;
    color: #E8EDF2;
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.6;
    max-height: 600px;
    overflow-y: auto;
    position: relative;
  }
  .walkthrough-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-family: 'Roboto', -apple-system, sans-serif;
  }
  .walkthrough-title {
    font-size: 15px;
    font-weight: 700;
    color: white;
  }
  .walkthrough-controls {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .walkthrough-btn {
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.1);
    color: white;
    transition: all 0.2s;
  }
  .walkthrough-btn:hover { background: rgba(255,255,255,0.2); }
  .walkthrough-btn.active { background: var(--pai-teal); color: var(--pai-dark-blue); border-color: var(--pai-teal); }

  /* MCP Connection Step 0 */
  .wt-mcp-step {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 6px;
    background: rgba(255,255,255,0.05);
    border-left: 3px solid var(--pai-teal);
  }
  .wt-mcp-step.collapsed {
    padding: 8px 16px;
    cursor: pointer;
    opacity: 0.7;
  }
  .wt-mcp-step.collapsed:hover { opacity: 1; }
  .wt-mcp-connected {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: var(--pai-teal);
    font-weight: 600;
    font-size: 12px;
    font-family: 'Roboto', -apple-system, sans-serif;
  }
  .wt-mcp-tools {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
  }
  .wt-mcp-tool {
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    background: rgba(0,217,211,0.1);
    color: var(--pai-teal);
    opacity: 0;
    transition: opacity 0.3s;
  }
  .wt-mcp-tool.lit { opacity: 1; }

  /* Walkthrough steps */
  .wt-step {
    margin-bottom: 12px;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.4s, transform 0.4s;
  }
  .wt-step.visible { opacity: 1; transform: translateY(0); }

  .wt-user-input {
    color: var(--pai-teal);
    margin-bottom: 8px;
  }
  .wt-user-input .wt-prompt { color: var(--pai-med-gray); margin-right: 8px; }
  .wt-user-input .wt-typed { border-right: 2px solid var(--pai-teal); padding-right: 2px; }

  .wt-tool-call {
    padding: 8px 12px;
    border-radius: 4px;
    background: rgba(255,255,255,0.03);
    border-left: 2px solid var(--pai-med-blue);
    margin-bottom: 4px;
  }
  .wt-tool-call.parallel { border-left-color: var(--pai-yellow); }
  .wt-tool-name { color: var(--pai-med-blue); font-weight: 600; }
  .wt-tool-call.parallel .wt-tool-name { color: var(--pai-yellow); }
  .wt-tool-desc { color: var(--pai-med-gray); margin-left: 8px; font-size: 12px; }
  .wt-tool-status {
    float: right;
    font-size: 11px;
    font-family: 'Roboto', -apple-system, sans-serif;
  }
  .wt-tool-status.loading { color: var(--pai-yellow); }
  .wt-tool-status.done { color: var(--pai-teal); }

  .wt-tool-response {
    margin-top: 6px;
    padding: 8px;
    border-radius: 3px;
    background: rgba(0,0,0,0.2);
    font-size: 11px;
    color: var(--pai-med-gray);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s;
    cursor: pointer;
  }
  .wt-tool-response.expanded { max-height: 200px; overflow-y: auto; }
  .wt-tool-response-toggle {
    font-size: 11px;
    color: var(--pai-med-gray);
    cursor: pointer;
    margin-top: 4px;
    font-family: 'Roboto', -apple-system, sans-serif;
  }
  .wt-tool-response-toggle:hover { color: white; }

  /* Analysis steps */
  .wt-analysis {
    padding: 8px 12px;
    color: var(--pai-light-teal);
    font-style: italic;
    font-family: 'Roboto', -apple-system, sans-serif;
    font-size: 13px;
  }

  /* Output sections */
  .wt-output {
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-family: 'Roboto', -apple-system, sans-serif;
  }
  .wt-output-section {
    padding: 4px 0;
    color: white;
    font-size: 13px;
    opacity: 0;
    transition: opacity 0.4s;
  }
  .wt-output-section.visible { opacity: 1; }
  .wt-output-section-name { font-weight: 600; }
  .wt-output-bar {
    height: 3px;
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
    margin-top: 4px;
    overflow: hidden;
  }
  .wt-output-bar-fill {
    height: 100%;
    background: var(--pai-teal);
    border-radius: 2px;
    width: 0;
    transition: width 0.6s;
  }

  /* Parallel indicator */
  .wt-parallel-group {
    border-left: 2px solid var(--pai-yellow);
    padding-left: 12px;
    margin-left: 4px;
    position: relative;
  }
  .wt-parallel-label {
    font-size: 10px;
    color: var(--pai-yellow);
    font-family: 'Roboto', -apple-system, sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
```

**Step 2: Commit**

```bash
git add docs/index.html
git commit -m "feat: add walkthrough CSS styles to catalog

Terminal-style panel with animations for MCP connection, tool calls,
parallel execution groups, and streaming output sections.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: Add mock data generator JS

**Files:**
- Modify: `docs/index.html` (add JS after the `wizardCopy` function, around line 1047)

**Step 1: Add the mock data generator**

Insert after the `wizardCopy()` function (after line 1047) in `docs/index.html`:

```javascript
// ── Walkthrough Mock Data Generator ──
const MOCK_DATA = {
  find_account: (input) => JSON.stringify({
    name: input, peopleai_account_id: "acc_" + Math.floor(Math.random()*90000+10000),
    domain: input.toLowerCase().replace(/\s+/g, '') + ".com",
    opportunities: [
      { name: `${input} Enterprise Renewal`, amount: "$450,000", stage: "Negotiation", close_date: "2026-04-15" },
      { name: `${input} Platform Expansion`, amount: "$180,000", stage: "Discovery", close_date: "2026-06-30" }
    ]
  }, null, 2),

  get_account_status: (input) => JSON.stringify({
    risks: [
      { risk: "Executive sponsor changing roles Q2", flagged_by: "Sarah Chen (AE)" },
      { risk: "Competitor POC running in parallel", flagged_by: "Mike Torres (CSM)" }
    ],
    next_steps: [
      { action: "Schedule QBR with new VP Engineering", owner: "Sarah Chen", due: "2026-03-15" },
      { action: "Send updated ROI analysis", owner: "Mike Torres", due: "2026-03-10" }
    ],
    topics: ["Budget approval timeline", "Integration requirements", "Q2 roadmap alignment"]
  }, null, 2),

  get_opportunity_status: (input) => JSON.stringify({
    opportunity: `${input} Enterprise Renewal`,
    amount: "$450,000", stage: "Negotiation", probability: "65%",
    risks: ["Decision maker not yet engaged", "Competing priorities in Q2"],
    next_steps: ["Send revised proposal by Friday", "Schedule technical deep-dive"],
    days_to_close: 40
  }, null, 2),

  get_scorecard: (input) => JSON.stringify({
    overall_completion: "62%", target: "75%", gap: "13%",
    sections: [
      { name: "Business Overview", score: 8, max: 10, status: "Needs Update" },
      { name: "Key Stakeholders", score: 7, max: 10, status: "Complete" },
      { name: "Competitive Landscape", score: 3, max: 10, status: "Critical Gap" },
      { name: "Technology Stack", score: 0, max: 10, status: "Undervalued" },
      { name: "Success Metrics", score: 6, max: 10, status: "Needs Update" }
    ]
  }, null, 2),

  get_engaged_people: (input) => JSON.stringify({
    external: [
      { name: "Jennifer Walsh", title: "VP Engineering", emails_30d: 12, meetings_30d: 3, role: "Economic Buyer" },
      { name: "David Park", title: "Director of Platform", emails_30d: 24, meetings_30d: 5, role: "Champion" },
      { name: "Lisa Huang", title: "Sr. Engineer", emails_30d: 8, meetings_30d: 2, role: "Key Stakeholder" },
      { name: "Tom Bradley", title: "Procurement Manager", emails_30d: 3, meetings_30d: 1, role: "Operational Contact" }
    ],
    internal: [
      { name: "Sarah Chen", title: "Account Executive", emails_30d: 31, meetings_30d: 8 },
      { name: "Mike Torres", title: "CSM", emails_30d: 18, meetings_30d: 4 }
    ]
  }, null, 2),

  get_recent_account_activity: (input) => JSON.stringify({
    period: "Last 30 days",
    summary: `Active engagement with ${input}. 47 emails exchanged, 12 meetings held. Key topics: renewal terms, platform expansion, Q2 roadmap.`,
    highlights: [
      "Technical deep-dive on March 1 — positive feedback on new API features",
      "Procurement initiated contract review on Feb 28",
      "Champion (David Park) requested executive intro for budget approval"
    ]
  }, null, 2),

  get_recent_opportunity_activity: (input) => JSON.stringify({
    period: "Last 30 days",
    summary: "Deal momentum increasing. 3 key meetings in past 2 weeks.",
    highlights: [
      "Proposal review meeting — client requested custom pricing tier",
      "Technical validation complete — passed security review",
      "Next: Executive alignment meeting scheduled March 12"
    ]
  }, null, 2),

  ask_sales_ai_about_account: (input) => JSON.stringify({
    analysis: `${input} shows strong engagement signals with 65% increase in meeting frequency over the past quarter. The champion (David Park) is actively advocating internally, but economic buyer (Jennifer Walsh) has had limited direct engagement. Key risk: competitor POC running in parallel. Recommended strategy: secure executive alignment meeting within 2 weeks and present updated ROI tied to their Q2 infrastructure modernization initiative.`
  }, null, 2),

  ask_sales_ai_about_opportunity: (input) => JSON.stringify({
    analysis: `This opportunity is progressing well through Negotiation stage with 65% probability. MEDDPICC gaps: Economic Buyer access is limited (2 interactions), Decision Process not fully mapped, and Competition not well understood. Strongest elements: Champion strength (David Park, 29 touchpoints) and Identified Pain (clear budget allocation for platform modernization). Recommend focusing next 2 weeks on economic buyer engagement and competitive differentiation.`
  }, null, 2),

  account_company_news: (input) => JSON.stringify({
    news: [
      { date: "2026-02-28", headline: `${input} announces Q4 earnings beat — revenue up 18% YoY`, source: "SEC Filing" },
      { date: "2026-02-15", headline: `${input} expands engineering team with 50 new hires`, source: "Press Release" },
      { date: "2026-01-20", headline: `${input} partners with major cloud provider for infrastructure modernization`, source: "TechCrunch" }
    ]
  }, null, 2),

  top_records: (input) => JSON.stringify({
    top_accounts: [
      { name: input, score: 92, trend: "up" },
      { name: "Globex Industries", score: 87, trend: "stable" },
      { name: "Initech Solutions", score: 74, trend: "down" }
    ]
  }, null, 2),

  find_record_by_crm_id: (input) => JSON.stringify({
    record_type: "Account", name: input, crm_id: "001ABC123", status: "Active"
  }, null, 2),
};

function getMockResponse(toolName, inputValue) {
  // Direct match
  if (MOCK_DATA[toolName]) return MOCK_DATA[toolName](inputValue);

  // Pattern match for get_*_status, get_recent_*_activity, ask_sales_ai_*
  for (const [pattern, generator] of Object.entries(MOCK_DATA)) {
    if (toolName.startsWith(pattern.split('_')[0]) && toolName.includes(pattern.split('_').pop())) {
      return generator(inputValue);
    }
  }

  // Fallback
  return JSON.stringify({ result: `Response from ${toolName}`, status: "success" }, null, 2);
}
```

**Step 2: Commit**

```bash
git add docs/index.html
git commit -m "feat: add mock data generator for walkthrough tool responses

Keyed on Backstory MCP tool name patterns with plausible enterprise
sales data. Falls back gracefully for unknown tools.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: Add SkillWalkthrough JS component

**Files:**
- Modify: `docs/index.html` (add JS after mock data generator)

**Step 1: Add the walkthrough component**

Insert after the `getMockResponse` function in `docs/index.html`:

```javascript
// ── Skill Walkthrough Component ──
class SkillWalkthrough {
  constructor(skill, container) {
    this.skill = skill;
    this.container = container;
    this.wt = skill.walkthrough;
    this.currentStep = -1; // -1 = not started
    this.playing = false;
    this.timer = null;
    this.mcpSeen = localStorage.getItem('wt-mcp-seen') === 'true';
    this.customData = null;
    this.inputValue = this.wt.input.example;
  }

  async init() {
    // Load custom walkthrough data if available
    if (this.wt.hasCustomData) {
      try {
        const res = await fetch(`../data/${this.skill.id}/walkthrough-data.json`);
        if (res.ok) this.customData = await res.json();
      } catch (e) { /* use auto-generated */ }
    }
    this.render();
  }

  render() {
    const el = document.createElement('div');
    el.className = 'walkthrough';
    el.innerHTML = `
      <div class="walkthrough-header">
        <div class="walkthrough-title">See it in action</div>
        <div class="walkthrough-controls">
          <button class="walkthrough-btn" data-action="play">&#9654; Play</button>
          <button class="walkthrough-btn" data-action="step">Step &#8594;</button>
          <button class="walkthrough-btn" data-action="reset">Reset</button>
        </div>
      </div>
      <div class="wt-body"></div>
    `;

    el.querySelector('[data-action="play"]').onclick = () => this.togglePlay();
    el.querySelector('[data-action="step"]').onclick = () => this.stepForward();
    el.querySelector('[data-action="reset"]').onclick = () => this.reset();

    this.container.appendChild(el);
    this.el = el;
    this.body = el.querySelector('.wt-body');
    this.buildSteps();
  }

  buildSteps() {
    this.body.innerHTML = '';
    this.stepElements = [];

    // Step 0: MCP Connection
    const mcpEl = document.createElement('div');
    mcpEl.className = 'wt-mcp-step' + (this.mcpSeen ? ' collapsed' : '');
    mcpEl.innerHTML = this.mcpSeen ? this.renderMcpCollapsed() : this.renderMcpFull();
    if (this.mcpSeen) {
      mcpEl.onclick = () => { mcpEl.className = 'wt-mcp-step'; mcpEl.innerHTML = this.renderMcpFull(); mcpEl.onclick = null; };
    }
    this.body.appendChild(mcpEl);
    this.mcpEl = mcpEl;

    // User input step
    const inputEl = document.createElement('div');
    inputEl.className = 'wt-step';
    inputEl.innerHTML = `<div class="wt-user-input"><span class="wt-prompt">&gt;</span> <span class="wt-typed"></span></div>`;
    this.body.appendChild(inputEl);
    this.stepElements.push({ el: inputEl, type: 'input' });

    // Tool call steps — group parallel ones
    let i = 0;
    const toolSteps = this.wt.steps.filter(s => s.type === 'tool');
    const analysisSteps = this.wt.steps.filter(s => s.type === 'analysis');

    while (i < toolSteps.length) {
      const step = toolSteps[i];
      if (step.parallel) {
        // Collect all parallel steps with same stepNum
        const group = [];
        const groupNum = step.stepNum;
        while (i < toolSteps.length && toolSteps[i].parallel && toolSteps[i].stepNum === groupNum) {
          group.push(toolSteps[i]);
          i++;
        }
        const groupEl = document.createElement('div');
        groupEl.className = 'wt-step';
        let inner = '<div class="wt-parallel-group"><div class="wt-parallel-label">Parallel execution</div>';
        group.forEach(g => {
          inner += this.renderToolCall(g);
        });
        inner += '</div>';
        groupEl.innerHTML = inner;
        this.body.appendChild(groupEl);
        this.stepElements.push({ el: groupEl, type: 'parallel', tools: group });
      } else {
        const toolEl = document.createElement('div');
        toolEl.className = 'wt-step';
        toolEl.innerHTML = this.renderToolCall(step);
        this.body.appendChild(toolEl);
        this.stepElements.push({ el: toolEl, type: 'tool', tool: step });
        i++;
      }
    }

    // Analysis steps
    analysisSteps.forEach(step => {
      const aEl = document.createElement('div');
      aEl.className = 'wt-step';
      aEl.innerHTML = `<div class="wt-analysis">&#9881; ${step.title}...</div>`;
      this.body.appendChild(aEl);
      this.stepElements.push({ el: aEl, type: 'analysis' });
    });

    // Output sections
    if (this.wt.outputSections.length > 0) {
      const outEl = document.createElement('div');
      outEl.className = 'wt-step';
      let outHtml = '<div class="wt-output">';
      this.wt.outputSections.forEach((section, idx) => {
        outHtml += `<div class="wt-output-section" data-idx="${idx}">
          <div class="wt-output-section-name">${section}</div>
          <div class="wt-output-bar"><div class="wt-output-bar-fill"></div></div>
        </div>`;
      });
      outHtml += '</div>';
      outEl.innerHTML = outHtml;
      this.body.appendChild(outEl);
      this.stepElements.push({ el: outEl, type: 'output' });
    }
  }

  renderToolCall(step) {
    const mock = this.getToolResponse(step.name);
    return `<div class="wt-tool-call ${step.parallel ? 'parallel' : ''}">
      <span class="wt-tool-name">${step.name}</span>
      <span class="wt-tool-desc">— ${step.description}</span>
      <span class="wt-tool-status"></span>
      <div class="wt-tool-response-toggle" onclick="this.nextElementSibling.classList.toggle('expanded')">&#9660; View response</div>
      <div class="wt-tool-response"><pre>${mock}</pre></div>
    </div>`;
  }

  getToolResponse(toolName) {
    if (this.customData && this.customData.tools && this.customData.tools[toolName]) {
      return JSON.stringify(this.customData.tools[toolName].response, null, 2);
    }
    const input = this.customData ? this.customData.input : this.inputValue;
    return getMockResponse(toolName, input);
  }

  renderMcpFull() {
    const tools = this.wt.steps.filter(s => s.type === 'tool').map(s => s.name);
    const uniqueTools = [...new Set(tools)];
    return `
      <div style="font-family:'Roboto',-apple-system,sans-serif;font-size:13px;">
        <div style="font-weight:700;margin-bottom:8px;color:white;">Step 0: Connect Backstory MCP</div>
        <div style="color:var(--pai-med-gray);margin-bottom:8px;">Settings &rarr; Integrations &rarr; Backstory MCP</div>
        <div class="wt-mcp-connected" style="display:none;" data-connected>
          &#10003; Connected — tools available:
        </div>
        <div class="wt-mcp-tools">
          ${uniqueTools.map(t => `<span class="wt-mcp-tool" data-tool="${t}">${t}</span>`).join('')}
        </div>
      </div>`;
  }

  renderMcpCollapsed() {
    return `<div class="wt-mcp-connected">&#10003; Backstory MCP Connected <span style="color:var(--pai-med-gray);font-weight:400;margin-left:8px;">(click to replay)</span></div>`;
  }

  async animateMcp() {
    if (this.mcpSeen) return;
    const connectedEl = this.mcpEl.querySelector('[data-connected]');
    const toolEls = this.mcpEl.querySelectorAll('.wt-mcp-tool');

    await this.wait(600);
    if (connectedEl) connectedEl.style.display = 'inline-flex';
    for (const toolEl of toolEls) {
      toolEl.classList.add('lit');
      await this.wait(150);
    }
    await this.wait(400);
    localStorage.setItem('wt-mcp-seen', 'true');
    this.mcpSeen = true;
  }

  async stepForward() {
    this.currentStep++;
    if (this.currentStep === 0) {
      await this.animateMcp();
    }
    if (this.currentStep >= this.stepElements.length) {
      this.currentStep = this.stepElements.length - 1;
      this.stop();
      return;
    }
    const step = this.stepElements[this.currentStep];
    step.el.classList.add('visible');

    if (step.type === 'input') {
      await this.animateTyping(step.el.querySelector('.wt-typed'), this.inputValue);
    } else if (step.type === 'tool' || step.type === 'parallel') {
      await this.animateToolCalls(step.el);
    } else if (step.type === 'output') {
      await this.animateOutput(step.el);
    }
  }

  async animateTyping(el, text) {
    el.textContent = '';
    for (let i = 0; i <= text.length; i++) {
      el.textContent = text.substring(0, i);
      await this.wait(50);
    }
    await this.wait(300);
  }

  async animateToolCalls(el) {
    const calls = el.querySelectorAll('.wt-tool-call');
    for (const call of calls) {
      const status = call.querySelector('.wt-tool-status');
      status.textContent = 'calling...';
      status.className = 'wt-tool-status loading';
    }
    await this.wait(800);
    for (const call of calls) {
      const status = call.querySelector('.wt-tool-status');
      status.textContent = 'done';
      status.className = 'wt-tool-status done';
    }
    await this.wait(200);
  }

  async animateOutput(el) {
    const sections = el.querySelectorAll('.wt-output-section');
    for (const section of sections) {
      section.classList.add('visible');
      const bar = section.querySelector('.wt-output-bar-fill');
      if (bar) bar.style.width = (60 + Math.random() * 40) + '%';
      await this.wait(400);
    }
  }

  async togglePlay() {
    if (this.playing) {
      this.stop();
    } else {
      this.playing = true;
      this.el.querySelector('[data-action="play"]').classList.add('active');
      this.el.querySelector('[data-action="play"]').innerHTML = '&#9646;&#9646; Pause';
      while (this.playing && this.currentStep < this.stepElements.length - 1) {
        await this.stepForward();
        if (this.playing) await this.wait(800);
      }
      this.stop();
    }
  }

  stop() {
    this.playing = false;
    const btn = this.el.querySelector('[data-action="play"]');
    btn.classList.remove('active');
    btn.innerHTML = '&#9654; Play';
  }

  reset() {
    this.stop();
    this.currentStep = -1;
    this.stepElements.forEach(s => s.el.classList.remove('visible'));
    // Reset tool statuses
    this.el.querySelectorAll('.wt-tool-status').forEach(s => { s.textContent = ''; s.className = 'wt-tool-status'; });
    this.el.querySelectorAll('.wt-output-section').forEach(s => s.classList.remove('visible'));
    this.el.querySelectorAll('.wt-output-bar-fill').forEach(b => b.style.width = '0');
    this.el.querySelectorAll('.wt-tool-response').forEach(r => r.classList.remove('expanded'));
    // Reset MCP if needed
    if (!this.mcpSeen) {
      const connectedEl = this.mcpEl.querySelector('[data-connected]');
      if (connectedEl) connectedEl.style.display = 'none';
      this.mcpEl.querySelectorAll('.wt-mcp-tool').forEach(t => t.classList.remove('lit'));
    }
  }

  wait(ms) { return new Promise(r => setTimeout(r, ms)); }
}
```

**Step 2: Commit**

```bash
git add docs/index.html
git commit -m "feat: add SkillWalkthrough JS component

Animated step-by-step simulation with MCP connection (Step 0), typed
user input, tool call animations with expandable mock responses,
parallel execution groups, and streaming output sections. Supports
auto-play, manual stepping, and reset.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: Wire walkthrough into the detail view

**Files:**
- Modify: `docs/index.html` — `renderDetail()` function (around line 752-853)

**Step 1: Add walkthrough rendering to `renderDetail()`**

In the `renderDetail()` function, after the detail header `</div>` and before the tabs `<div class="tabs">`, insert the walkthrough section. Find this line (around line 789):

```javascript
    </div>

    <div class="tabs" id="detail-tabs">
```

And insert between them:

```javascript
    ${skill.walkthrough ? `<div id="walkthrough-container"></div>` : ''}
```

Then at the bottom of `renderDetail()`, after `document.getElementById('detail-content').innerHTML = html;` (around line 852), add:

```javascript
  // Initialize walkthrough if available
  if (skill.walkthrough) {
    const wtContainer = document.getElementById('walkthrough-container');
    const wt = new SkillWalkthrough(skill, wtContainer);
    wt.init();
  }
```

**Step 2: Commit**

```bash
git add docs/index.html
git commit -m "feat: wire walkthrough component into skill detail view

Renders walkthrough panel between the detail header and platform tabs
when a skill has walkthrough data in skills.json.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: Rebuild skills.json and verify end-to-end

**Files:**
- Run: `docs/build-catalog.py`
- Verify: `docs/index.html` in browser

**Step 1: Run the build**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 build-catalog.py`

Expected: `Generated skills.json with 19 skills` — all 19 print successfully.

**Step 2: Verify walkthrough data for multiple skills**

Run: `python3 -c "
import json
d = json.load(open('skills.json'))
for s in d['skills'][:5]:
    wt = s.get('walkthrough')
    steps = len(wt['steps']) if wt else 0
    out = len(wt['outputSections']) if wt else 0
    print(f\"{s['number']} {s['name']}: {steps} steps, {out} output sections\")
"`

Expected: Each skill shows >0 steps. Something like:
```
01 Account Plan Agent: 5 steps, 8 output sections
02 External Company News Agent: 5 steps, 6 output sections
03 Relationship Map Agent: 4 steps, 5 output sections
...
```

**Step 3: Open in browser and test**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 -m http.server 8080`

Open `http://localhost:8080` in browser. Click on Account Plan Agent card. Verify:
- Walkthrough panel appears between header and tabs
- "Play" button starts the animation
- MCP connection Step 0 shows tools lighting up
- User input types out "Acme Corp"
- Tool calls show loading → done with expandable responses
- Parallel tools show grouped with yellow border
- Output sections stream in

**Step 4: Commit final state**

```bash
git add docs/skills.json
git commit -m "feat: rebuild skills.json with walkthrough data for all 19 skills

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7: Add walkthrough-data.json for Account Plan Agent (optional enrichment)

**Files:**
- Create: `01-account-plan-agent/assets/walkthrough-data.json`

**Step 1: Create the custom mock data file**

```json
{
  "input": "Globex Industries",
  "tools": {
    "find_account": {
      "response": {
        "name": "Globex Industries",
        "peopleai_account_id": "acc_99871",
        "domain": "globexindustries.com",
        "opportunities": [
          { "name": "Globex Platform Modernization", "amount": "$720,000", "stage": "Proposal", "close_date": "2026-05-01" },
          { "name": "Globex Analytics Add-On", "amount": "$95,000", "stage": "Closed Won", "close_date": "2026-01-15" }
        ]
      }
    },
    "get_scorecard": {
      "response": {
        "overall_completion": "58%",
        "target": "75%",
        "gap": "17%",
        "sections": [
          { "name": "Business Overview", "score": 9, "max": 10, "status": "Complete" },
          { "name": "Key Stakeholders", "score": 5, "max": 10, "status": "Needs Update" },
          { "name": "Competitive Landscape", "score": 2, "max": 10, "status": "Critical Gap" },
          { "name": "Technology Stack", "score": 0, "max": 10, "status": "Undervalued" },
          { "name": "Success Metrics", "score": 7, "max": 10, "status": "Needs Update" },
          { "name": "Growth Strategy", "score": 6, "max": 10, "status": "Needs Update" }
        ]
      }
    },
    "get_engaged_people": {
      "response": {
        "external": [
          { "name": "Rachel Kim", "title": "CTO", "emails_30d": 4, "meetings_30d": 2, "role": "Economic Buyer" },
          { "name": "James Okafor", "title": "VP Platform Engineering", "emails_30d": 22, "meetings_30d": 6, "role": "Champion" },
          { "name": "Priya Sharma", "title": "Director of Data", "emails_30d": 15, "meetings_30d": 3, "role": "Key Stakeholder" },
          { "name": "Carlos Mendez", "title": "Senior Architect", "emails_30d": 18, "meetings_30d": 4, "role": "Key Stakeholder" },
          { "name": "Amy Liu", "title": "Procurement Lead", "emails_30d": 6, "meetings_30d": 1, "role": "Operational Contact" }
        ],
        "internal": [
          { "name": "Ben Alvarez", "title": "Enterprise AE", "emails_30d": 38, "meetings_30d": 9 },
          { "name": "Keiko Tanaka", "title": "Solutions Engineer", "emails_30d": 14, "meetings_30d": 5 },
          { "name": "Ryan O'Brien", "title": "CSM", "emails_30d": 12, "meetings_30d": 3 }
        ]
      }
    }
  }
}
```

**Step 2: Rebuild skills.json to pick up the custom data flag**

Run: `cd /Users/scottmetcalf/projects/LLMSkills/docs && python3 build-catalog.py`

Verify: `python3 -c "import json; d=json.load(open('skills.json')); print(d['skills'][0]['walkthrough']['hasCustomData'])"`

Expected: `True`

**Step 3: Commit**

```bash
git add 01-account-plan-agent/assets/walkthrough-data.json docs/skills.json
git commit -m "feat: add hand-crafted walkthrough data for Account Plan Agent

Richer Globex Industries example with detailed scorecard, stakeholder
map, and opportunity data for a more polished demo experience.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
