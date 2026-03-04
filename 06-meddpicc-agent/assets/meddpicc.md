# SalesAI MEDDPICC Agent - Knowledge Document

## Overview

The **SalesAI MEDDPICC Agent** is an AI-powered qualification system that leverages People.ai communication intelligence to automatically assess and improve MEDDPICC qualification for any B2B opportunity. This agent transforms raw communication data into actionable qualification insights with personalized coaching and prioritized action plans.

### Core Principle
Transform People.ai data into intelligent MEDDPICC qualification with specific ownership, evidence-based insights, and AI-powered coaching recommendations for any account or opportunity.

---

## MEDDPICC Framework Integration

### Scoring Methodology

Based on the standard MEDDPICC scorecard template, the agent uses a weighted scoring system:

| Element | Max Points | Weight % | Description |
|---------|------------|----------|-------------|
| **M** - Metrics | 5 | 10.87% | Success metrics and quantifiable targets |
| **E** - Economic Buyer | 7 | 15.22% | Budget authority identification and access |
| **D** - Decision Criteria | 5 | 10.87% | Required capabilities for evaluation |
| **D** - Decision Process | 5 | 10.87% | Evaluation, selection, and purchase process |
| **P** - Paper Process | 5 | 10.87% | Contract and legal approval timeline |
| **I** - Identify Pain | 7 | 15.22% | Pain points and compelling events |
| **C** - Champion | 7 | 15.22% | Internal advocate with influence |
| **C** - Competition | 5 | 10.87% | Competitive landscape and positioning |

**Total Maximum Score:** 46 points

### Scoring Scale

- **0-20 points (0-43%):** Critical Risk - Immediate intervention required
- **21-30 points (44-65%):** High Risk - Significant gaps need addressing  
- **31-38 points (66-82%):** Moderate Risk - Some improvements needed
- **39-46 points (83-100%):** Low Risk - Well qualified opportunity

---

## Agent Architecture

### 1. Universal Account Discovery

```python
def discover_account_opportunities(account_name):
    # Find account and all available opportunities
    account_data = find_account(account_name=account_name)
    
    # Filter and present opportunity selection menu
    opportunities = account_data["opportunities"]
    active_opportunities = [
        opp for opp in opportunities 
        if opp.get("stage") not in ["Closed Won", "Closed Lost"] 
        and opp.get("amount", 0) > 10000  # Material deals only
    ]
    
    return {
        "account": account_data,
        "opportunities": active_opportunities,
        "selection_menu": format_opportunity_menu(active_opportunities)
    }
```

### 2. Intelligence Gathering Engine

```python
def gather_meddpicc_intelligence(opportunity_id, account_id):
    intelligence = {
        "opportunity_status": get_opportunity_status(opportunity_id),
        "recent_activity": get_recent_opportunity_activity(opportunity_id),
        "account_context": get_account_status(account_id),
        "ai_analysis": ask_sales_ai_about_opportunity(
            question="Provide comprehensive MEDDPICC analysis including stakeholder engagement, qualification gaps, and recommended next steps",
            opportunity_id=opportunity_id
        )
    }
    return intelligence
```

### 3. MEDDPICC Assessment Engine

```python
def assess_meddpicc_elements(opportunity_intelligence):
    assessments = {
        "metrics": assess_metrics(opportunity_intelligence),
        "economic_buyer": assess_economic_buyer(opportunity_intelligence),
        "decision_criteria": assess_decision_criteria(opportunity_intelligence),
        "decision_process": assess_decision_process(opportunity_intelligence),
        "paper_process": assess_paper_process(opportunity_intelligence),
        "identify_pain": assess_pain_points(opportunity_intelligence),
        "champion": assess_champion_strength(opportunity_intelligence),
        "competition": assess_competitive_position(opportunity_intelligence)
    }
    
    total_score = sum([elem["score"] for elem in assessments.values()])
    health_percentage = (total_score / 46) * 100
    
    return {
        "elements": assessments,
        "total_score": total_score,
        "health_percentage": health_percentage,
        "risk_level": classify_risk_level(health_percentage)
    }
```

### 4. AI Coaching Engine

```python
def generate_coaching_insights(meddpicc_assessment, opportunity_intelligence):
    coaching_insights = []
    
    for element, assessment in meddpicc_assessment["elements"].items():
        if assessment["score"] < assessment["max_score"] * 0.6:  # Below 60% threshold
            insight = {
                "element": element,
                "current_score": assessment["score"],
                "max_score": assessment["max_score"],
                "priority": calculate_priority(assessment, opportunity_intelligence),
                "evidence": extract_evidence(element, opportunity_intelligence),
                "recommendation": generate_recommendation(element, assessment, opportunity_intelligence),
                "next_action": define_next_action(element, assessment, opportunity_intelligence)
            }
            coaching_insights.append(insight)
    
    return sorted(coaching_insights, key=lambda x: x["priority"], reverse=True)
```

---

## People.ai Brand Integration

### Color Palette Implementation

```css
:root {
    /* Primary Colors */
    --primary-blue: #006885;
    --off-black: #641225;
    --dark-blue: #00204E;
    --blue: #0A41AA;
    --med-blue: #8CB8ED;
    --light-blue: #CDE6FF;
    
    /* Secondary Colors */
    --teal: #00D9D3;
    --light-teal: #7FECE9;
    --dark-gray: #54667D;
    --med-gray: #A9B2BE;
    --light-gray: #D4D9DE;
    --white: #FFFFFF;
    
    /* Support Colors */
    --yellow: #E8C031;
    --orange: #EB8D35;
    --red: #F8544D;
    --magenta: #FC458A;
    --violet: #743FCF;
    --turquoise: #019E9B;
}
```

### Typography Standards

```css
/* Primary Typeface - Headers */
.agent-title, .meddpicc-name, .coaching-category {
    font-family: 'Proxima Nova Bold', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-weight: 700;
}

/* Secondary Typeface - Body Copy */
.agent-subtitle, .meddpicc-status, .coaching-recommendation {
    font-family: 'Proxima Nova Regular', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-weight: 400;
}
```

### Brand-Compliant Gradients

```css
/* Primary Gradient: Teal + Primary Blue + Magenta */
.agent-header {
    background: linear-gradient(135deg, var(--teal) 0%, var(--primary-blue) 50%, var(--magenta) 100%);
}

/* BG 01: Primary Blue + Medium Blue */
.meddpicc-assessment .assessment-header {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--med-blue) 100%);
}

/* Blue-Teal Gradient */
.coaching-panel .coaching-header {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--teal) 100%);
}
```

---

## MEDDPICC Element Assessment Logic

### Economic Buyer Assessment

```python
def assess_economic_buyer(intelligence):
    score = 0
    evidence = []
    
    # Extract stakeholder information
    stakeholders = extract_stakeholders(intelligence)
    
    # Check for budget authority indicators
    for stakeholder in stakeholders:
        if has_budget_keywords(stakeholder["communications"]):
            score += 1
            evidence.append(f"Budget discussions with {stakeholder['name']}")
        
        if has_executive_title(stakeholder["title"]):
            score += 1
            evidence.append(f"Executive level: {stakeholder['name']} - {stakeholder['title']}")
    
    # Check for confirmed economic buyer
    if confirmed_economic_buyer(intelligence):
        score += 3
        evidence.append("Economic buyer confirmed and accessible")
    
    return {
        "score": min(score, 7),  # Cap at maximum
        "max_score": 7,
        "evidence": evidence,
        "status": get_status_text(score, 7),
        "recommendations": generate_eb_recommendations(score, evidence)
    }
```

### Champion Assessment

```python
def assess_champion_strength(intelligence):
    score = 0
    evidence = []
    
    # Identify potential champions
    champions = identify_champions(intelligence)
    
    for champion in champions:
        engagement_level = calculate_engagement_level(champion, intelligence)
        
        if engagement_level > 70:
            score += 2
            evidence.append(f"High engagement: {champion['name']} ({engagement_level}%)")
        
        if shows_advocacy_behavior(champion, intelligence):
            score += 2
            evidence.append(f"Advocacy behavior detected: {champion['name']}")
        
        if has_internal_influence(champion, intelligence):
            score += 1
            evidence.append(f"Internal influence confirmed: {champion['name']}")
    
    return {
        "score": min(score, 7),
        "max_score": 7,
        "evidence": evidence,
        "status": get_status_text(score, 7),
        "recommendations": generate_champion_recommendations(score, evidence)
    }
```

---

## AI Coaching Framework

### Priority Calculation Algorithm

```python
def calculate_priority(assessment, opportunity_intelligence):
    base_priority = (assessment["max_score"] - assessment["score"]) / assessment["max_score"]
    
    # Weight by element importance for deal closure
    importance_weights = {
        "economic_buyer": 1.0,      # Highest priority
        "decision_process": 0.9,
        "paper_process": 0.9,
        "champion": 0.8,
        "decision_criteria": 0.7,
        "metrics": 0.6,
        "identify_pain": 0.5,
        "competition": 0.4
    }
    
    # Adjust for days to close urgency
    days_to_close = extract_days_to_close(opportunity_intelligence)
    urgency_multiplier = 1.0 + (1.0 - min(days_to_close / 180, 1.0))  # Higher priority as close date approaches
    
    final_priority = base_priority * importance_weights.get(assessment["element"], 0.5) * urgency_multiplier
    
    return final_priority
```

### Recommendation Engine

```python
def generate_recommendation(element, assessment, intelligence):
    templates = {
        "economic_buyer": {
            "score_0": "No economic buyer identified. Use stakeholder mapping to identify budget authority through current contacts.",
            "score_1-2": "Potential economic buyer identified but not confirmed. Schedule direct meeting to validate budget authority.",
            "score_3-5": "Economic buyer access confirmed. Validate budget availability and purchase commitment."
        },
        "champion": {
            "score_0": "No champion identified. Assess stakeholders for potential advocates and begin champion development.",
            "score_1-3": "Potential champion identified but influence unclear. Test commitment with specific advocacy requests.",
            "score_4-6": "Champion confirmed but needs strengthening. Provide success tools and internal selling support."
        },
        "decision_process": {
            "score_0": "Decision process unknown. Map evaluation, selection and approval workflow with key stakeholders.",
            "score_1-2": "Basic process understanding. Validate steps, timeline and required approvals with economic buyer.",
            "score_3-4": "Process mapped but needs validation. Create mutual success plan aligned to their workflow."
        }
        # ... additional element templates
    }
    
    score_range = get_score_range(assessment["score"], assessment["max_score"])
    return templates[element][score_range]
```

---

## Action Plan Generation

### Intelligent Prioritization

```python
def generate_action_plan(coaching_insights, opportunity_timeline):
    critical_actions = []
    high_priority_actions = []
    medium_priority_actions = []
    
    for insight in coaching_insights:
        action = {
            "element": insight["element"],
            "action": insight["next_action"],
            "owner": determine_owner(insight["element"]),
            "timeline": calculate_timeline(insight["priority"], opportunity_timeline),
            "success_criteria": define_success_criteria(insight["element"], insight["current_score"])
        }
        
        if insight["priority"] >= 0.8:
            critical_actions.append(action)
        elif insight["priority"] >= 0.6:
            high_priority_actions.append(action)
        else:
            medium_priority_actions.append(action)
    
    return {
        "week_1": critical_actions,
        "week_2": high_priority_actions,
        "week_3": medium_priority_actions
    }
```

---

## Messaging Template System

### Dynamic Template Generation

```python
def generate_meddpicc_messages(element, stakeholder_context, opportunity_context):
    message_templates = {
        "economic_buyer_discovery": {
            "subject": f"{opportunity_context['type']} planning discussion - budget and decision process",
            "opening": f"Hi {stakeholder_context['name']},\n\nWith our {opportunity_context['close_date_formatted']} {opportunity_context['type'].lower()} approaching...",
            "body": generate_eb_discovery_body(stakeholder_context, opportunity_context),
            "cta": "Available this week for a 30-minute process alignment discussion.",
            "signature": get_sender_signature("AE")
        },
        "champion_testing": {
            "subject": f"Strategic {opportunity_context['type'].lower()} support - executive introduction request", 
            "opening": f"Hi {stakeholder_context['name']},\n\nYour advocacy has been instrumental in our partnership success...",
            "body": generate_champion_testing_body(stakeholder_context, opportunity_context),
            "cta": f"Could we discuss your thoughts on {opportunity_context['type'].lower()} strategy this week?",
            "signature": get_sender_signature("CSM")
        },
        "decision_process_validation": {
            "subject": f"{opportunity_context['type']} timeline planning - process confirmation",
            "opening": f"Hi {stakeholder_context['name']},\n\nThank you for the introduction. I'd like to ensure our timeline aligns with your internal requirements...",
            "body": generate_process_validation_body(stakeholder_context, opportunity_context),
            "cta": "Available for a brief process alignment call this week.",
            "signature": get_sender_signature("AE")
        }
        # ... additional templates
    }
    
    return message_templates[element]
```

---

## Universal Opportunity Selection

### Opportunity Menu Generation

```python
def format_opportunity_menu(opportunities):
    menu_items = []
    
    for i, opp in enumerate(opportunities):
        # Calculate health indicators
        engagement_level = opp.get("engagement_level", 0)
        days_to_close = calculate_days_to_close(opp.get("close_date"))
        
        # Determine status indicator
        status_indicator = get_status_indicator(engagement_level, days_to_close, opp.get("amount"))
        
        menu_item = {
            "index": i + 1,
            "name": opp.get("opportunity_name"),
            "amount": format_currency(opp.get("amount")),
            "close_date": format_date(opp.get("close_date")),
            "days_remaining": days_to_close,
            "engagement_level": engagement_level,
            "status": status_indicator,
            "type": opp.get("type"),
            "owner": opp.get("owner", {}).get("name")
        }
        menu_items.append(menu_item)
    
    return menu_items

def get_status_indicator(engagement, days_to_close, amount):
    if engagement >= 80 and days_to_close < 120:
        return "ðŸ”¥ HOT DEAL"
    elif engagement == 0 or days_to_close > 365:
        return "ðŸš¨ CRITICAL - NO ENGAGEMENT"
    elif engagement < 30 or days_to_close > 300:
        return "âš ï¸ STALLED"
    elif engagement >= 60:
        return "âš¡ ACTIVE"
    else:
        return "âš ï¸ NEEDS ATTENTION"
```

---

## Dashboard Implementation

### Visual Component Structure

```html
<div class="agent-container">
    <header class="agent-header">
        <div class="agent-title">
            ðŸ¤– SalesAI MEDDPICC Agent
            <div class="ai-badge">AI-POWERED</div>
        </div>
        <div class="opportunity-info">
            <div class="info-item">
                <div class="info-label">Opportunity</div>
                <div class="info-value">{opportunity_name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Deal Value</div>
                <div class="info-value">{formatted_amount}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Days to Close</div>
                <div class="info-value pulse">{days_to_close} Days</div>
            </div>
            <div class="info-item">
                <div class="info-label">Account Team</div>
                <div class="info-value">{team_members}</div>
            </div>
        </div>
    </header>
    
    <main class="main-dashboard">
        <section class="meddpicc-assessment">
            <!-- Dynamic MEDDPICC scoring with progress bars -->
        </section>
        
        <section class="coaching-panel">
            <!-- AI-generated coaching insights -->
        </section>
    </main>
    
    <section class="action-plan-section">
        <!-- Prioritized action timeline -->
    </section>
    
    <section class="messaging-section">
        <!-- MEDDPICC-specific templates -->
    </section>
</div>
```

---

## Integration Points

### People.ai MCP Tools Required

1. **find_account** - Universal account discovery and opportunity selection
2. **get_opportunity_status** - Strategic overview with risks and next steps
3. **get_recent_opportunity_activity** - Communication history analysis
4. **ask_sales_ai_about_opportunity** - AI-powered comprehensive analysis
5. **get_account_status** - Account-level context and intelligence

### Universal Data Processing Pipeline

```python
def process_any_opportunity_for_meddpicc(account_name, opportunity_selection):
    # 1. Discover all opportunities for account
    discovery = discover_account_opportunities(account_name)
    
    # 2. Present selection menu if multiple opportunities
    if len(discovery["opportunities"]) > 1:
        selected_opportunity = handle_opportunity_selection(discovery["opportunities"], opportunity_selection)
    else:
        selected_opportunity = discovery["opportunities"][0]
    
    # 3. Gather intelligence for selected opportunity
    intelligence = gather_meddpicc_intelligence(
        selected_opportunity["opportunity_id"], 
        discovery["account"]["account_id"]
    )
    
    # 4. Process MEDDPICC assessment
    assessment = assess_meddpicc_elements(intelligence)
    
    # 5. Generate AI coaching
    coaching = generate_coaching_insights(assessment, intelligence)
    
    # 6. Create action plan
    actions = generate_action_plan(coaching, intelligence)
    
    # 7. Generate messaging
    messages = generate_targeted_messaging(coaching, intelligence)
    
    # 8. Render dashboard
    return render_meddpicc_dashboard(
        account=discovery["account"],
        opportunity=selected_opportunity,
        assessment=assessment,
        coaching=coaching,
        actions=actions,
        messages=messages
    )
```

---

## Success Metrics

### Qualification Improvement KPIs

- **MEDDPICC Score Progression** - Track improvement over time across all accounts
- **Element Completion Rate** - Percentage of elements above 60% threshold  
- **Critical Gap Resolution** - Time to address 0-score elements
- **Action Plan Execution** - Percentage of recommended actions completed

### Business Impact Metrics

- **Win Rate Improvement** - Opportunities with MEDDPICC Agent vs. control group
- **Sales Cycle Acceleration** - Average time reduction for qualified opportunities  
- **Forecast Accuracy** - Improved prediction based on qualification health
- **Champion Development** - Number of champions identified and developed per account

---

## Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Set up People.ai MCP tool access
- [ ] Implement universal account discovery
- [ ] Create opportunity selection interface
- [ ] Build MEDDPICC scoring engine
- [ ] Test with 3-5 pilot accounts across different industries

### Phase 2: Intelligence (Week 2) 
- [ ] Build AI coaching recommendation engine
- [ ] Implement priority calculation algorithm
- [ ] Create action plan generation system
- [ ] Add dynamic messaging template library
- [ ] Test coaching accuracy across different deal types

### Phase 3: Optimization (Week 3)
- [ ] Integrate People.ai brand guidelines
- [ ] Add responsive design and mobile support
- [ ] Implement progress tracking and analytics
- [ ] Create team collaboration features
- [ ] Validate across enterprise, mid-market, and SMB segments

### Phase 4: Scale (Week 4)
- [ ] Multi-account management dashboard
- [ ] Team performance analytics
- [ ] Integration with CRM systems
- [ ] Advanced AI coaching features
- [ ] White-label customization options

---

## Usage Examples

### Enterprise Software Renewal Example

**Input:** Account Name = "Global Manufacturing Corp"
**Opportunity Selected:** #1 - Software Renewal - $750K - 120 days to close

**MEDDPICC Assessment Results:**
- Overall Score: 18/46 (39%) - High Risk
- Critical Gaps: Economic Buyer (0/7), Decision Criteria (1/5), Paper Process (0/5)
- Strengths: Identify Pain (6/7), Champion (4/7)

**AI Coaching Generated:**
1. **Economic Buyer Priority:** "Multiple stakeholders engaged but no confirmed budget authority"
2. **Paper Process Gap:** "120 days to close but contract process unmapped"  
3. **Decision Criteria Weakness:** "Renewal criteria assumptions not validated"

---

### New Business SaaS Deal Example

**Input:** Account Name = "Regional Bank Corp"  
**Opportunity Selected:** #2 - Platform Implementation - $250K - 180 days to close

**MEDDPICC Assessment Results:**
- Overall Score: 25/46 (54%) - High Risk
- Critical Gaps: Champion (1/7), Economic Buyer (2/7), Decision Process (1/5)
- Strengths: Competition (4/5), Identify Pain (5/7)

**AI Coaching Generated:**
1. **Champion Development:** "Technical contacts engaged but no business champion identified"
2. **Economic Buyer Access:** "IT stakeholders active but budget holder unknown"
3. **Process Mapping:** "Technical evaluation progressing but business approval process unclear"

---

This universal knowledge document provides the complete foundation for implementing the SalesAI MEDDPICC Agent with any account or opportunity, ensuring scalable qualification improvement across diverse sales scenarios.