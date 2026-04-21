# Backstory LLM Skills

Shareable Claude skills powered by the Backstory MCP. These skills help customers jump-start their use of the Backstory MCP integration with Claude.

## Start here (customer setup)

**Fastest path: Claude.ai Project**

- Pick a skill folder (e.g. `01-account-plan-agent`)
- Open `claude-project.md`
- Copy the **Custom Instructions** block into a new Claude.ai Project
- Upload any files in that skill’s `assets/` folder (if present)
- Connect **Backstory MCP** in Claude (Settings → Integrations)
- Start a chat in the project and provide the skill input (usually an **account name**)

**Optional: Browse the catalog UI**

The `docs/` folder contains a static catalog page. To run it locally:

```bash
cd docs
python3 build-catalog.py
python3 -m http.server 8080
```

Then open `http://localhost:8080` and click a skill.

## Skills

### Account Research & Planning
| # | Skill | Description |
|---|-------|-------------|
| 01 | Account Plan Agent | Dynamic account plan dashboards with real-time intelligence |
| 02 | External Company News Agent | Market intelligence — financials, earnings, strategic insights |
| 03 | Relationship Map Agent | Interactive stakeholder influence maps |
| 04 | Customer Sentiment Agent | Sentiment trend analysis and risk signal detection |

### Opportunity & Deal Management
| # | Skill | Description |
|---|-------|-------------|
| 05 | Opportunity Agent | Comprehensive deal health dashboards and action plans |
| 06 | MEDDPICC Agent | AI-powered MEDDPICC qualification and coaching |
| 07 | Win Probability Agent | Real-time win probability scoring for deals |
| 10 | Multi-Threading Coach Agent | Identifies single-threaded risk and recommends people to engage |
| 14 | Competitive Battle Card Agent | Live battle cards tailored to deal context and customer concerns |

### Meeting & Review Prep
| # | Skill | Description |
|---|-------|-------------|
| 08 | Meeting Prep Agent | One-page meeting briefing with talking points and risks |
| 09 | QBR Generator Agent | Draft Quarterly Business Review content from engagement data |
| 15 | Executive Briefing Agent | Internal exec summary — Red/Yellow/Green health, revenue at risk, leadership action needed |

### Action & Growth
| # | Skill | Description |
|---|-------|-------------|
| 11 | Next Best Action Agent | Top 3 actions to take right now with specific contacts and messaging |
| 12 | Whitespace Mapper Agent | Expansion opportunities by department — engagement without revenue |
| 13 | Pipeline Review Agent | Portfolio-level pipeline health, coaching priorities, and forecast risks |
| 16 | Renewal Risk Agent | Predicts renewal likelihood with 6-dimension risk scoring and save plans |

### Transitions & Learning
| # | Skill | Description |
|---|-------|-------------|
| 17 | Handoff Agent | Account handoff docs — stakeholder personalities, commitments, landmines |
| 18 | Deal Debrief Agent | Post-close win/loss analysis with lessons learned |

### Engagement Analytics
| # | Skill | Description |
|---|-------|-------------|
| 19 | Engagement Scorecard Agent | Data-driven engagement metrics — who's active, who's going dark, trends |

## Skill Format

Each skill folder contains:
- `SOURCE.md` — Metadata and MCP tool references
- `skill.md` — Claude Code skill version
- `claude-project.md` — Claude.ai project template
- `chatgpt-gpt.md` — ChatGPT Custom GPT template
- `assets/` — Knowledge files and supporting documents

## Validation (for maintainers)

To verify every skill is complete and consistent before publishing:

```bash
python3 docs/validate-skills.py
```

## Prerequisites

- Claude Pro/Team account
- Backstory MCP integration connected ([MCP setup articles](https://help.people.ai/en/?q=mcp))
