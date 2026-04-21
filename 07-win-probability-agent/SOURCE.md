# Win Probability Agent

## Description
Real-time, time-sensitive win probability scoring for sales opportunities. Factors in timeline pressure — same qualification gaps have different impact based on time available.

## Audience
AEs, Sales leaders

## Input
Account name

## MCP Tools Used
- find_account
- get_opportunity_status
- get_recent_opportunity_activity
- ask_sales_ai_about_opportunity

## Project Knowledge Files
- winprob.md (scoring methodology, time-sensitive business logic, and validation results)

## Sample Output

<!--mockup:slack-->
<!--bot:Win Probability Agent-->
<!--bot-app:true-->

**Win Probability: ACME Corp Enterprise Renewal**
===$485,000=== | Stage: Negotiation | Close: 2026-04-15

**Win Probability: 62%** (Moderate confidence)

**Positive Factors**
- Strong technical fit — passed evaluation with highest score among vendors
- Quantified pain validated by multiple stakeholders (12+ hrs/week manual work)
- Active legal review in progress — redlines received 2026-03-08
- Existing relationship — ACME is a current customer with 2-year history
- Stage progression on track — moved from Evaluation to Negotiation in 14 days

**Negative Factors**
- Champion @Lisa Park silent for 9 days — activity drop signals potential risk (-8%)
- Economic buyer @James Morton not engaged in 3 weeks (-6%)
- Active competitor still in play with pricing pressure (-5%)
- Finance team not yet looped in — budget approval unconfirmed (-4%)
- 35 days until procurement freeze — limited time to recover gaps (-3%)

**Comparison to Similar Deals**
- Deals at this stage with similar engagement patterns close at 68% on average
- However, deals with silent champions at this stage drop to 51% win rate
- Renewal deals with existing customers in this segment close at 74%

**Recommendations to Improve Odds**
- Re-engage @Lisa Park immediately — reactivating the champion could push probability to 70%+
- Get @James Morton into a live meeting this week — economic buyer engagement adds ~8% historically
- Loop in Finance with a business case summary — removing budget uncertainty adds ~5%
- Lock in a mutual close plan with defined dates before 2026-03-20
- Prepare a competitive counter-offer to neutralize pricing objection

---

*Win Probability Agent - powered by Backstory activity data*

