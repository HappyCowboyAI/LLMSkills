# Renewal Risk Agent

## Description
Predicts renewal likelihood by scoring engagement decay, sentiment shifts, stakeholder turnover, and competitive mentions — then generates a save plan for at-risk accounts.

## Audience
CSMs, Sales leaders

## Input
Account name

## MCP Tools Used
- find_account
- get_account_status
- get_recent_account_activity
- get_engaged_people
- account_company_news
- ask_sales_ai_about_account
- get_opportunity_status

## Project Knowledge Files
- None

## Sample Output

<!--mockup:slack-->
<!--bot:Renewal Risk Agent-->
<!--bot-app:true-->

**Renewal Risk Assessment: ACME Corp**

**Overall Risk Score: 72/100 (High Risk)**

- **Account:** ACME Corp
- **Current ARR:** ===$340,000===
- **Renewal Date:** Jun 15, 2026 (96 days out)
- **Contract Term:** 2-year agreement, first renewal cycle
- **Account Owner:** @Lisa Tran | **CSM:** @Maria Santos

**Risk Factors**

- **Champion Departure (Critical):** @Janet Liu (VP Revenue Operations), our primary champion, departed ACME on Feb 20, 2026. Replacement @Kevin Briggs has no prior relationship with our team and has not responded to 3 outreach attempts.
- **Engagement Decline (High):** Monthly active users dropped from 185 to 112 over the last 90 days (-39%). Executive logins have fallen to zero since Jan 2026. Weekly meeting cadence with @Maria Santos was cancelled in February.
- **Competitive Threat (Medium):** Gong sales team identified in recent ACME meeting activity. @Kevin Briggs previously used Gong at his last company (TerraFlow Inc.). Two Gong calendar invites detected on ACME stakeholder calendars in late February.
- **Sentiment Shift (Medium):** Last NPS response from ACME (Dec 2025) dropped from 8 to 5. Support ticket volume increased 40% in Q1 2026, with 2 escalations still unresolved.
- **Budget Pressure (Low-Medium):** ACME announced a 10% OpEx reduction in Q1 2026 earnings call. Technology vendor consolidation review is underway per @Robert Nakamura's LinkedIn post.

**Mitigating Factors**

- ACME's data analytics team (28 users) remains highly active — 4.2 sessions/user/week, above benchmark
- Integration with ACME's Salesforce instance is deep (14 custom workflows) — high switching cost
- @Robert Nakamura (CTO) deployed our platform at his previous company and has expressed long-term strategic interest
- ACME realized $1.2M in documented ROI from pipeline acceleration in Year 1

**Recommended Save Plays**

- **Immediate (This Week):** @Maria Santos and @Lisa Tran to schedule an intro meeting with @Kevin Briggs — bring a refreshed value summary and Year 1 ROI report. Escalate to @Michael Reeves for exec air cover if no response by Mar 18.
- **Week 2:** Resolve the 2 open support escalations and send a formal remediation summary to @Kevin Briggs. Demonstrate responsiveness before renewal conversations begin.
- **Week 3-4:** Propose an Executive Business Review with @Robert Nakamura and @Kevin Briggs — present usage analytics, ROI outcomes, and a Year 2 success roadmap. Include the expansion use case for the CS team (===$220,000=== potential) as a value-add incentive.
- **Contingency:** If engagement does not recover by Apr 15, prepare a right-sizing proposal (reduce seats to active user count) to protect ===$240,000=== in core ARR rather than risking full churn.

---
*Risk assessment generated from engagement telemetry, CRM activity, stakeholder tracking, and sentiment analysis. Assessed: Mar 11, 2026.*
