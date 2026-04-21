# Setup Walkthrough Design

## Goal
Add an animated setup walkthrough to each skill's Setup tab, replacing the current plain-text steps with a visual, step-by-step simulation of each platform's UI (Claude.ai Project, Claude Code, ChatGPT Custom GPT).

## Architecture
A new `SetupWalkthrough` class (mirroring `SkillWalkthrough`) renders CSS-drawn platform UI mockups inside the existing Setup tab. Each platform tab triggers a platform-specific animation sequence showing users exactly where to click, what to paste, and how to connect MCP. No images required - all UI mockups are pure CSS/HTML.

## Platform UI Mockups

### Claude.ai Project
- Browser chrome with address bar ("claude.ai")
- Sidebar with Projects section
- Project creation dialog (name field, instructions textarea)
- Integrations/MCP settings panel
- Theme: warm beige/brown tones

### Claude Code
- Terminal window with dark background
- Shows file editing (CLAUDE.md), config commands
- MCP connection verification output
- Theme: dark terminal with green/white text

### ChatGPT Custom GPT
- Browser chrome ("chatgpt.com")
- GPT Builder interface (name, instructions, actions panels)
- Action configuration dialog
- Theme: dark sidebar, white content area

## Animation Steps Per Platform

### Claude.ai Project (6 steps)
1. Click "Projects" in sidebar - project panel slides open
2. Click "Create Project" - name field appears, skill name types in
3. Paste custom instructions - textarea fills with animated typing (abbreviated)
4. Upload knowledge files - file chips appear (from projectKnowledgeFiles)
5. Connect Backstory MCP - integrations panel, toggle animates on
6. Start conversation - chat input with example account name

### Claude Code (4 steps)
1. Open terminal - prompt appears
2. Add instructions to CLAUDE.md - file content animates in
3. Verify MCP connection - `claude mcp list` output shows Backstory
4. Invoke skill - example command and response

### ChatGPT Custom GPT (5 steps)
1. Click "Explore GPTs" > "Create" button
2. Name the GPT - name field fills with skill name
3. Paste instructions - instructions box fills
4. Configure Actions - action panel with tool endpoints listed
5. Save and test - chat interface with example input

## Component: SetupWalkthrough

### API
- `init(skill, platformId)` - loads skill data + platform setup steps
- `render()` - draws platform UI mockup + step controls
- `animateStep(n)` - transitions mockup to show step n
- `stepForward()` / `stepBack()` / `togglePlay()` / `reset()`

### Controls
- Play/Pause button
- Step forward/back arrows
- Progress dots showing current step
- Copy button on instructions step

### Animation
- Auto-play on tab switch (2s delay per step)
- Active UI elements get pulsing border/glow highlight
- Smooth CSS transitions between steps (fade/slide)
- Animated typing for text input steps

## Data Source
All data already exists in skills.json:
- `skill.platforms[platformId].setupSteps` - step titles
- `skill.platforms[platformId].instructions` - actual prompt text for paste steps
- `skill.name` - for project/GPT naming steps
- `skill.projectKnowledgeFiles` - for upload steps
- `skill.mcpTools` - for action configuration steps

## Implementation Scope
- All changes in `docs/index.html` (CSS + JS)
- No build pipeline changes needed
- No new files
- ~150 lines CSS for platform mockups
- ~300 lines JS for SetupWalkthrough class
- Replace existing setup tab rendering to use new component
