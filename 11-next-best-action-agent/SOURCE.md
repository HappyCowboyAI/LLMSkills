# Next Best Action Agent

## Description
Surfaces the top 3 actions to take today across your accounts — prioritized by urgency, deal value, and risk signals from recent activity.

## Audience
AEs, CSMs

## Input
Account name (or "my accounts" for portfolio scan)

## MCP Tools Used
- find_account
- get_account_status
- get_recent_account_activity
- ask_sales_ai_about_account
- get_opportunity_status

## Project Knowledge Files
- None

## Sample Output

<!--mockup:slack-->
<!--bot:Next Best Action Agent-->
<!--bot-app:true-->

**Next Best Actions — ACME Corp**

Here are your top 3 prioritized actions for ACME Corp today:

- **1. Follow up on security review (Urgency: HIGH)**
  @Sarah Chen from ACME's InfoSec team opened a ticket requesting SSO configuration docs 2 days ago — no response yet. This is blocking the ===$540,000=== enterprise expansion deal currently in legal review.
  *Expected impact: Unblocks deal progression and keeps close date on track for Q1.*

- **2. Schedule executive business review (Urgency: MEDIUM)**
  @James Whitfield (VP Engineering) has not had an EBR in 4 months. Recent activity shows declining product usage in the engineering org (-18% MAU over 60 days). Proactive outreach now reduces churn risk on the ===$210,000=== annual contract renewing in 45 days.
  *Expected impact: Strengthens executive alignment and protects renewal revenue.*

- **3. Share case study with procurement (Urgency: LOW)**
  @Maria Lopez (Procurement Lead) requested ROI benchmarks during last week's call. Sending the FinServ case study positions ACME for a multi-year commitment and supports the ===$120,000=== upsell opportunity in Stage 3.
  *Expected impact: Accelerates procurement approval and increases deal confidence.*

---

*Powered by Next Best Action Agent — actions prioritized by urgency, deal value, and risk signals.*
