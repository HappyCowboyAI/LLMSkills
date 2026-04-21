# MEDDPICC Agent

## Description
AI-powered MEDDPICC qualification system that automatically assesses and improves qualification status from communication data.

## Audience
AEs, Sales managers

## Input
Account name

## MCP Tools Used
- find_account
- get_opportunity_status
- get_recent_opportunity_activity
- ask_sales_ai_about_opportunity
- get_account_status

## Project Knowledge Files
- meddpicc.md (MEDDPICC scoring methodology, coaching framework, and assessment logic)

## Sample Output

<!--mockup:slack-->
<!--bot:MEDDPICC Agent-->
<!--bot-app:true-->

**MEDDPICC Scorecard: ACME Corp Enterprise Renewal**
===$485,000=== | Stage: Negotiation | Close: 2026-04-15

**Overall Score: B-**

- **Metrics — A**: Quantified ROI presented; ACME confirmed 3.2x projected return and 40% reduction in manual workflows. Strong alignment to their FY26 efficiency targets.
- **Economic Buyer — C**: @James Morton (VP Ops) identified but has not directly engaged in last 3 weeks. No meeting or email activity since 2026-02-20. Needs re-confirmation.
- **Decision Criteria — B+** : Technical requirements validated. ACME shared evaluation rubric; we score highest on integration and support SLAs. Minor gap on reporting customization.
- **Decision Process — B** : Procurement steps mapped through @Lisa Park. Legal is reviewing redlines. Missing: finance sign-off sequence and final approver confirmation.
- **Identify Pain — A** : Pain well-documented — current platform causing 12+ hrs/week of manual reconciliation. @Lisa Park cited this as a top-3 department priority for Q2.
- **Champion — C+** : @Lisa Park has been an active champion but has gone silent for 9 days. No internal advocacy activity detected recently. Risk of losing momentum.
- **Competition — C** : Competitor remains shortlisted. ACME referenced "alternative pricing" on last call. Limited intel on competitor's proposal details or discount strategy.

**Top Actions to Improve Score**
- Re-engage @James Morton with an executive business review to solidify Economic Buyer
- Check in with @Lisa Park to understand silence and reactivate champion engagement
- Gather competitive intel — ask @Lisa Park directly what the alternative is offering
- Confirm remaining decision process steps with a mutual close plan

---

*MEDDPICC Agent - powered by Backstory activity data*

