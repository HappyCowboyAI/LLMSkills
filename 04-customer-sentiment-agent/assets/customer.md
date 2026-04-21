# Customer Sentiment Analysis Using Backstory MCP
*Knowledge Document for Claude Project*

## Overview
This document provides a comprehensive framework for analyzing customer sentiment using Backstory MCP (Model Control Protocol) data sources. The analysis produces a quantified sentiment score (0-10) with detailed breakdown across multiple dimensions.

## Sentiment Analysis Framework

### Overall Sentiment Score Calculation
The overall score is a weighted average of 5 components:
- **Communication Sentiment (20%)**: Tone, collaboration, solution-orientation
- **Engagement Level (25%)**: Meeting frequency, stakeholder involvement, participation
- **Strategic Value Recognition (25%)**: ROI metrics, executive adoption, business impact
- **Technical Satisfaction (20%)**: Platform performance, user experience, issue resolution
- **Risk Assessment (10%)**: Competitive threats, churn indicators, concerning behaviors

**Formula**: `Overall Score = (Communication Ã— 0.20) + (Engagement Ã— 0.25) + (Strategic Value Ã— 0.25) + (Technical Satisfaction Ã— 0.20) + ((10 - Risk Level) Ã— 0.10)`

## Data Collection Workflow

### Step 1: Find Account
```
Use: Backstory MCP:find_account
Input: account_name (e.g., "Redis", "Anaplan")
Output: Account ID, domain, name, opportunities list
```

### Step 2: Gather Core Activity Data  
```
Use: Backstory MCP:get_recent_account_activity
Input: account_id
Output: 30-day communication summaries, meeting insights, key facts
```

### Step 3: Get Strategic Overview
```
Use: Backstory MCP:get_account_status  
Input: account_id
Output: Risks, next steps, trending topics from recent communications
```

### Step 4: Check Company News (Public Companies Only)
```
Use: Backstory MCP:account_company_news
Input: account_id  
Output: Recent M&A, organizational changes, financial performance
```

### Step 5: Supplementary Data (Optional)
- **Gmail Search**: `from:domain.com OR to:domain.com` for email sentiment
- **Calendar Search**: Account name for meeting frequency and attendance
- **Google Drive**: Search for account-specific documents, QBRs, contracts

## Sentiment Component Analysis Guide

### 1. Communication Sentiment (0-10)
**Scoring Criteria:**
- **9-10**: Highly collaborative, appreciative language, solution-focused
- **7-8**: Positive tone, professional engagement, constructive feedback
- **5-6**: Neutral communication, transactional interactions
- **3-4**: Some frustration, direct complaints, formal tone
- **1-2**: Hostile, threatening, disengagement language

**Key Indicators:**
- Positive language: "Thanks for", "This is great", "Appreciate", "Helpful"
- Negative language: "Broken", "Useless", "Disappointed", "Frustrated"
- Response times and proactive communications
- Solution-oriented vs. blame-oriented discussions

### 2. Engagement Level (0-10)
**Scoring Criteria:**
- **9-10**: Weekly+ meetings, multiple stakeholders, high attendance
- **7-8**: Regular meetings, good participation, responsive communications  
- **5-6**: Standard meeting cadence, moderate participation
- **3-4**: Infrequent meetings, low attendance, delayed responses
- **1-2**: Minimal engagement, cancelled meetings, unresponsive

**Key Indicators:**
- Meeting frequency and duration
- Number of active stakeholders involved
- Attendance rates and participation levels
- Executive involvement and escalation patterns
- Response times to issues and requests

### 3. Strategic Value Recognition (0-10)
**Scoring Criteria:**
- **9-10**: Quantified ROI, executive adoption, core business process integration
- **7-8**: Clear value statements, leadership usage, expansion discussions
- **5-6**: Standard usage, some value recognition, routine operations
- **3-4**: Limited value articulation, basic usage, cost concerns
- **1-2**: No clear value, considering alternatives, cost-cutting focus

**Key Indicators:**
- Documented ROI metrics and productivity savings
- Executive and leadership platform usage
- Integration into core business processes
- Expansion discussions and new use cases
- References to platform value in communications

### 4. Technical Satisfaction (0-10)
**Scoring Criteria:**
- **9-10**: No issues, praise for functionality, smooth operations
- **7-8**: Minor issues quickly resolved, overall positive experience
- **5-6**: Some technical challenges, standard support needs
- **3-4**: Frequent issues, user complaints, functionality problems
- **1-2**: Major technical problems, system described as "broken"

**Key Indicators:**
- System error reports and resolution times
- User experience feedback and complaints
- Technical support ticket volume and complexity
- Platform adoption rates and usage metrics
- Data accuracy and integration issues

### 5. Risk Assessment (0-10, where 10 = highest risk)
**Scoring Criteria:**
- **8-10**: Exploring alternatives, executive dissatisfaction, budget cuts
- **6-7**: Some concerns raised, competitive evaluation, contract discussions
- **4-5**: Normal business risks, standard renewal cycle
- **2-3**: Minor concerns, easily addressable issues
- **0-1**: No significant risks identified

**Key Risk Indicators:**
- Mentions of competitive alternatives or evaluations
- Budget constraints or cost reduction initiatives
- Executive turnover or strategic shifts
- Contract renewal delays or term renegotiation requests
- Reduced usage or stakeholder disengagement

## Output Format Template

Use this exact structure for all sentiment analyses:

```markdown
# [Account Name] Customer Sentiment Analysis Report
*Analysis Period: [Date Range]*

## Executive Summary
**Overall Sentiment Score: X.X/10 ([Sentiment Category])**

[2-3 sentence summary of key findings and overall relationship health]

## Sentiment Components Analysis

### 1. Communication Sentiment (X/10)
**[Positive/Negative] Indicators:**
- [Bullet point findings]
- [Quote examples if available]

### 2. Engagement Level (X/10)
**[High/Low] Engagement Indicators:**
- [Meeting frequency, stakeholder involvement]
- [Participation metrics]

### 3. Strategic Value Recognition (X/10)
**Value Recognition:**
- [ROI metrics, executive usage]
- [Business impact examples]

### 4. Technical Satisfaction (X/10)
**Technical [Strengths/Challenges]:**
- [System performance indicators]
- [User feedback examples]

### 5. Risk Assessment (X/10)
**[Low/Medium/High] Risk Factors:**
- [Specific risk indicators]
- [Competitive threats or concerns]

## Key Relationship Dynamics

### Champions & Influencers
**Strong Champions:**
- [Name and role]: [Specific advocacy examples]

**Key Stakeholders:**
- [Names and engagement levels]

### Success Factors
1. [Primary success indicator]
2. [Secondary success indicator]
3. [Additional factors]

### Concern Areas
1. [Primary concern]
2. [Secondary concern]
3. [Additional issues]

## Recommendations

### Immediate Actions (0-30 days)
1. [Urgent action items]

### Strategic Actions (30-90 days)  
1. [Medium-term improvements]

### Long-term Growth (90+ days)
1. [Strategic initiatives]

## Conclusion
**Renewal Probability**: [XX-XX%] based on [key factors]
**Strategic Importance**: [High/Medium/Low] - [Justification]
```

## Sentiment Categories
- **9.0-10.0**: Exceptional Partnership
- **8.0-8.9**: Strong Positive
- **7.0-7.9**: Positive with Cautious Optimism  
- **6.0-6.9**: Cautiously Positive
- **5.0-5.9**: Neutral/Mixed
- **4.0-4.9**: Concerning
- **3.0-3.9**: At Risk
- **0.0-2.9**: Critical Risk

## Usage Instructions

When given an account name:

1. **Find Account**: Use find_account tool with the provided name
2. **Gather Data**: Collect all available data using the MCP tools
3. **Analyze Components**: Score each of the 5 sentiment components  
4. **Calculate Overall**: Apply the weighted formula for final score
5. **Generate Report**: Use the exact template format above
6. **Provide Sources**: List all data sources used in analysis

## Important Notes

- Always check for opportunities list before analysis (may need specific opportunity focus)
- Public companies: Use company news tool for external factors
- Private companies: Company news will return no results (expected)
- Quote sparingly: Use only short, relevant quotes (under 15 words)
- Focus on recent data: Emphasize last 30-60 days of activity
- Be objective: Balance positive and negative indicators equally
- Quantify when possible: Include specific metrics and numbers

## Quality Checklist

Before delivering analysis, ensure:
- [ ] All 5 sentiment components are scored and justified
- [ ] Overall score calculation is accurate  
- [ ] Key stakeholders are identified by name and role
- [ ] Specific examples support each scoring decision
- [ ] Recommendations are actionable and timebound
- [ ] Data sources are comprehensive and recent
- [ ] Output follows exact template format