# Pipeline Review Agent

## Description
Portfolio-level pipeline review for managers — aggregates deal health, stalled opportunities, coaching priorities, and forecast risks across multiple accounts.

## Audience
Sales managers, Sales leaders

## Input
List of account names (or a single account for deep-dive)

## MCP Tools Used
- find_account
- get_account_status
- get_opportunity_status
- ask_sales_ai_about_opportunity
- ask_sales_ai_about_account

## Project Knowledge Files
- None

## Sample Output

<!--mockup:slack-->
<!--bot:Pipeline Review Agent-->
<!--bot-app:true-->

**Pipeline Review — Q1 FY26**

**Summary**
- Total pipeline value: ===$2,340,000===
- Deal count: 8 opportunities
- Weighted forecast: ===$1,410,000===
- At-risk deals: 3
- Stale deals (no activity 14+ days): 2

**At-Risk Deals**

- **ACME Corp — Enterprise Expansion (===$540,000===, Stage 4)**
  Risk: Security review stalled for 9 days. @Sarah Chen has not received SSO documentation. No executive sponsor engaged since December.
  *Action: Escalate SSO docs to Solutions Engineering today. Schedule EBR with @James Whitfield this week.*

- **Globex Inc — Platform Migration (===$380,000===, Stage 3)**
  Risk: Champion @Tony Reeves left the company 3 weeks ago. New contact @Amanda Briggs has not responded to last 2 outreach attempts.
  *Action: Engage @Amanda Briggs through a warm intro via @Mark Sullivan (CTO). Re-confirm project timeline and budget.*

- **Initech — Analytics Upsell (===$210,000===, Stage 2)**
  Risk: Competitor demo scheduled for next week. ACME's POC results have not been shared with the buying committee.
  *Action: Send POC results summary to @Rachel Nguyen and request a buying committee presentation before Friday.*

**Stale Deals**

- **Wayne Industries — New Business (===$480,000===, Stage 1)** — Last activity: 21 days ago. *Action: Re-engage or move to nurture.*
- **Stark Labs — Renewal (===$330,000===, Stage 5)** — Last activity: 16 days ago. *Action: Confirm redline status with legal and push for signature.*

---

*Powered by Pipeline Review Agent — aggregating deal health, risks, and coaching priorities across your portfolio.*
