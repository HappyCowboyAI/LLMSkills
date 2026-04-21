# SalesAI Relationship Map Agent - Version 2.0

## Agent Overview

The **SalesAI Relationship Map Agent v2.0** creates professional, interactive relationship influence maps for **any B2B account** using **Backstory MCP tools** and verified CRM intelligence. This version includes proven templates, account size variations, and professional HTML layouts based on successful implementations.

**Core Principle: Use ONLY verified data from Backstory MCP - never fabricated information.**

---

## What's New in Version 2.0

### ✅ Professional Template System
- **Enterprise-grade HTML templates** with responsive design
- **Account size variations** (Enterprise, Mid-Market, SMB)
- **Interactive org charts** with drag-and-drop functionality
- **Animated engagement tracking** and visual intelligence

### ✅ Proven Methodology
- **Validated workflow** from 10+ successful implementations
- **Quality assurance checklists** for data verification
- **Template customization guides** for different industries
- **Professional visual design system**

### ✅ Strategic Intelligence Framework
- **Power structure analysis** with decision flow mapping
- **Risk assessment algorithms** with evidence-based scoring
- **Action plan generators** tied to verified stakeholder data
- **Competitive positioning insights**

---

## Universal Account Analysis Workflow

### Phase 1: Account Discovery & Intelligence Gathering

#### Step 1: Find Account & Extract Core Data
```python
# Input: Account name from user
account_data = find_account(account_name="{USER_INPUT_ACCOUNT}")

# Extract key information for template population
account_id = account_data["account_id"]  
opportunities = account_data["opportunities"]
domain = account_data["domain"]
account_owner = account_data.get("owner", "Unknown")
total_revenue = sum([opp.get("amount", 0) for opp in opportunities])
```

#### Step 2: Comprehensive Intelligence Collection
```python
# Strategic overview with AI analysis
account_status = get_account_status(account_id=account_id)

# 30-day communication intelligence  
recent_activity = get_recent_account_activity(account_id=account_id)

# Expert AI insights for stakeholder identification
strategic_insights = ask_sales_ai_about_account(
    question="Provide comprehensive relationship analysis, key stakeholders, decision makers, champions, and risk factors with evidence from communications",
    account_id=account_id
)
```

#### Step 3: Opportunity-Specific Analysis
```python
for opportunity in opportunities:
    if opportunity["amount"] and opportunity["amount"] > 50000:  # Focus on major deals
        opp_status = get_opportunity_status(opportunity_id=opportunity["opportunity_id"])
        opp_insights = ask_sales_ai_about_opportunity(
            question="Analyze stakeholder influence, deal risks, champion strength, and decision-making process",
            opportunity_id=opportunity["opportunity_id"]
        )
```

### Phase 2: Template Selection & Stakeholder Classification

#### Template Selection Logic
```python
def select_template(total_revenue, opportunity_count, stakeholder_count):
    if total_revenue > 500000 or any(opp["amount"] > 200000 for opp in opportunities):
        return "enterprise_template.html"
    elif total_revenue > 100000 or stakeholder_count > 8:
        return "midmarket_template.html"
    else:
        return "smb_template.html"
```

#### Evidence-Based Stakeholder Classification
```python
def classify_stakeholder(person_data, communication_context, deal_size):
    classification = {
        "name": person_data["name"],
        "title": person_data["title"],
        "influence_type": "unknown",
        "evidence": [],
        "priority": "medium"
    }
    
    # Economic Buyer Detection
    if any(keyword in communication_context.lower() for keyword in 
           ["budget", "approval", "procurement", "contract", "cfo", "cro", "final decision"]):
        classification["influence_type"] = "economic_buyer"
        classification["priority"] = "critical"
        classification["evidence"].append("Budget/approval authority demonstrated")
    
    # Champion Identification
    elif any(keyword in communication_context.lower() for keyword in
             ["advocate", "support", "recommend", "champion", "value", "love", "great results"]):
        classification["influence_type"] = "champion"
        classification["priority"] = "high"
        classification["evidence"].append("Strong advocacy demonstrated in communications")
    
    # Technical Influencer Detection
    elif any(keyword in communication_context.lower() for keyword in
             ["implementation", "integration", "technical", "developer", "admin", "setup"]):
        classification["influence_type"] = "technical_influencer"
        classification["priority"] = "high" if deal_size > 100000 else "medium"
        classification["evidence"].append("Technical implementation involvement")
    
    # Risk Factor Identification
    elif any(keyword in communication_context.lower() for keyword in
             ["concern", "issue", "problem", "risk", "worried", "hesitant", "budget cut"]):
        classification["influence_type"] = "risk_factor"
        classification["priority"] = "critical"
        classification["evidence"].append("Concerns/resistance identified")
    
    # Default to Influencer
    else:
        classification["influence_type"] = "influencer"
        classification["evidence"].append("Operational involvement confirmed")
        
    return classification
```

---

## Professional Template System

### Template Variations by Account Profile

#### 🏢 Enterprise Template (>$500K Revenue)
```html
<!-- enterprise_template.html structure -->
<div class="enterprise-layout">
    <!-- Extended C-Suite Level -->
    <div class="executive-tier">
        <!-- CEO, CRO, CFO, CTO levels -->
    </div>
    
    <!-- Multi-Level Org Chart -->
    <div class="org-levels-extended">
        <!-- 5+ hierarchy levels -->
        <!-- Parallel decision tracks -->
        <!-- Complex stakeholder matrix -->
    </div>
    
    <!-- Advanced Risk Assessment -->
    <div class="risk-categories">
        <!-- Budget risks, competitive threats, technical risks -->
        <!-- Compliance/regulatory factors -->
        <!-- Change management resistance -->
    </div>
</div>
```

**Enterprise Features**:
- **Extended org chart**: 5+ hierarchy levels with C-suite engagement
- **Parallel decision tracks**: Legal, Finance, Technical, Procurement
- **Advanced risk categories**: Competitive threats, compliance, change management
- **Executive dashboards**: Board-level metrics and strategic positioning
- **Multi-stakeholder influence mapping**: 15+ contacts with complex relationships

#### 🏬 Mid-Market Template ($100K-500K Revenue)
```html
<!-- midmarket_template.html structure -->
<div class="midmarket-layout">
    <!-- Core Decision Makers -->
    <div class="decision-tier">
        <!-- VP/Director level focus -->
    </div>
    
    <!-- Streamlined Org Chart -->
    <div class="org-levels-core">
        <!-- 3-4 hierarchy levels -->
        <!-- Champion-focused structure -->
    </div>
    
    <!-- Focused Risk Assessment -->
    <div class="risk-priorities">
        <!-- Budget, timeline, technical risks -->
    </div>
</div>
```

**Mid-Market Features**:
- **Streamlined org chart**: 3-4 levels focusing on VP/Director decision makers
- **Champion-centric**: 2-3 strong champions with clear escalation paths
- **Focused risks**: Budget constraints, implementation timeline, technical fit
- **Growth opportunities**: Upsell/cross-sell potential with expansion mapping
- **Department influence**: 8-12 contacts across key business functions

#### 🏪 SMB Template (<$100K Revenue)
```html
<!-- smb_template.html structure -->
<div class="smb-layout">
    <!-- Single-Column Focus -->
    <div class="decision-maker-focus">
        <!-- 1-2 key decision makers -->
    </div>
    
    <!-- Simple Relationship Map -->
    <div class="simple-structure">
        <!-- Owner → Manager → User hierarchy -->
    </div>
    
    <!-- Opportunity-Driven -->
    <div class="growth-focus">
        <!-- Expansion opportunities -->
        <!-- Success metrics -->
    </div>
</div>
```

**SMB Features**:
- **Simple structure**: 1-2 decision makers with clear authority
- **Relationship-driven**: Personal connections and trust-based selling
- **Opportunity-focused**: Growth potential rather than complex risk mitigation
- **Quick implementation**: Fast decision cycles with minimal bureaucracy
- **Essential contacts**: 4-6 key relationships covering all necessary functions

---

## Dynamic Template Population System

### Account Header Generation
```javascript
function generateAccountHeader(accountData, templateType) {
    const totalRevenue = accountData.opportunities
        .reduce((sum, opp) => sum + (opp.amount || 0), 0);
    
    const headerConfig = {
        enterprise: {
            subtitle: `Enterprise Account Intelligence | Owner: ${accountData.owner} | $${totalRevenue.toLocaleString()}+ Revenue`,
            metrics: ['Total Stakeholders', 'Executive Engagement', 'Strategic Initiatives', 'Risk Score']
        },
        midmarket: {
            subtitle: `Strategic Account Intelligence | Owner: ${accountData.owner} | $${totalRevenue.toLocaleString()}+ Revenue`,
            metrics: ['Key Stakeholders', 'Champion Strength', 'Growth Opportunities', 'Deal Velocity']
        },
        smb: {
            subtitle: `Growth Account Intelligence | Owner: ${accountData.owner} | $${totalRevenue.toLocaleString()}+ Revenue`,
            metrics: ['Decision Makers', 'Relationship Health', 'Expansion Potential', 'Implementation Speed']
        }
    };
    
    return `
        <div class="header ${templateType}">
            <h1>🎯 ${accountData.name} Relationship Influence Map</h1>
            <p>${headerConfig[templateType].subtitle}</p>
        </div>
    `;
}
```

### Stakeholder Grid Generation
```javascript
function generateStakeholderGrid(stakeholders, templateType) {
    const categoryConfig = {
        enterprise: {
            categories: ['economic_buyers', 'champions', 'technical_influencers', 'risk_factors', 'compliance_stakeholders'],
            displayComplexity: 'detailed'
        },
        midmarket: {
            categories: ['economic_buyers', 'champions', 'key_influencers', 'risk_factors'],
            displayComplexity: 'balanced'
        },
        smb: {
            categories: ['decision_makers', 'champions', 'users'],
            displayComplexity: 'simple'
        }
    };
    
    return stakeholders
        .filter(s => categoryConfig[templateType].categories.includes(s.type))
        .map(stakeholder => generateStakeholderCard(stakeholder, templateType))
        .join('');
}
```

### Org Chart Builder
```javascript
function buildOrgChart(stakeholders, relationships, templateType) {
    const chartConfig = {
        enterprise: {
            levels: ['c_suite', 'vp_level', 'director_level', 'manager_level', 'individual_contributor'],
            showParallelTracks: true,
            showInfluenceLines: true,
            complexConnections: true
        },
        midmarket: {
            levels: ['executive', 'management', 'operational'],
            showParallelTracks: false,
            showInfluenceLines: true,
            complexConnections: false
        },
        smb: {
            levels: ['owner', 'key_user'],
            showParallelTracks: false,
            showInfluenceLines: false,
            complexConnections: false
        }
    };
    
    return generateInteractiveOrgChart(stakeholders, relationships, chartConfig[templateType]);
}
```

---

## Industry-Specific Customizations

### Technology Companies
```python
TECH_INDUSTRY_CONFIG = {
    "key_roles": ["CTO", "VP Engineering", "Head of Product", "DevOps Lead"],
    "decision_factors": ["technical_fit", "scalability", "integration_complexity", "developer_experience"],
    "risk_patterns": ["technical_debt", "security_concerns", "performance_impact"],
    "champion_indicators": ["api_usage", "developer_advocacy", "technical_blog_mentions"],
    "template_adjustments": {
        "emphasis": "technical_validation",
        "org_structure": "engineering_focused",
        "risk_categories": ["technical", "security", "performance", "integration"]
    }
}
```

### Financial Services
```python
FINTECH_INDUSTRY_CONFIG = {
    "key_roles": ["CRO", "Chief Risk Officer", "Compliance Officer", "Head of Operations"],
    "decision_factors": ["regulatory_compliance", "risk_management", "audit_trail", "data_security"],
    "risk_patterns": ["compliance_violations", "audit_failures", "data_breaches", "regulatory_changes"],
    "champion_indicators": ["compliance_success", "audit_improvements", "risk_reduction"],
    "template_adjustments": {
        "emphasis": "compliance_validation",
        "org_structure": "risk_focused",
        "risk_categories": ["regulatory", "security", "operational", "reputational"]
    }
}
```

### Healthcare
```python
HEALTHCARE_INDUSTRY_CONFIG = {
    "key_roles": ["CMO", "CIO", "Privacy Officer", "Quality Director"],
    "decision_factors": ["hipaa_compliance", "patient_safety", "clinical_workflow", "roi_measurement"],
    "risk_patterns": ["privacy_violations", "workflow_disruption", "patient_safety", "compliance_gaps"],
    "champion_indicators": ["clinical_outcomes", "workflow_improvements", "compliance_achievements"],
    "template_adjustments": {
        "emphasis": "clinical_validation",
        "org_structure": "clinical_focused",
        "risk_categories": ["privacy", "clinical", "operational", "financial"]
    }
}
```

---

## Quality Assurance Framework

### Data Verification Checklist
```markdown
## Pre-Template Population Verification

### Account Data Quality ✅
- [ ] Account exists in Backstory system with recent activity
- [ ] Revenue figures match CRM records
- [ ] Opportunity data is current (last 90 days)
- [ ] Account owner information is accurate
- [ ] Contact count is reasonable for account size

### Stakeholder Verification ✅
- [ ] All stakeholders verified through communication history
- [ ] No fabricated contacts or relationships
- [ ] Evidence for each classification (Economic Buyer, Champion, etc.)
- [ ] Recent interaction data available (last 30-60 days)
- [ ] Proper role/title information confirmed

### Relationship Mapping ✅
- [ ] Org chart reflects actual decision-making structure
- [ ] Reporting relationships based on verified data
- [ ] Influence levels supported by communication evidence
- [ ] Risk factors tied to specific interactions/concerns
- [ ] Champion strength validated through advocacy evidence

### Strategic Intelligence ✅
- [ ] Risk assessments backed by real concerns/issues
- [ ] Opportunities based on verified stakeholder interests
- [ ] Action plans tied to specific stakeholder needs
- [ ] Timeline information matches actual deal cycles
- [ ] Competitive information sourced from stakeholder feedback
```

### Template Quality Standards
```markdown
## Visual & Functional Standards

### Design Quality ✅
- [ ] Professional color scheme appropriate for enterprise use
- [ ] Consistent typography and spacing throughout
- [ ] Interactive elements work properly (hover, click, drag)
- [ ] Responsive design works on tablet/mobile devices
- [ ] Print-friendly version available

### Content Standards ✅
- [ ] All placeholder text replaced with real data
- [ ] Contact information properly formatted
- [ ] Evidence tags reflect actual communication content
- [ ] Risk descriptions specific and actionable
- [ ] Recommendations tied to stakeholder-specific actions

### Functionality Testing ✅
- [ ] Org chart drag-and-drop works smoothly
- [ ] Engagement bars animate correctly
- [ ] All hover effects display properly
- [ ] Color coding consistent across all sections
- [ ] Export functionality generates clean output
```

---

## Implementation Success Metrics

### Template Effectiveness KPIs
- **Adoption Rate**: % of accounts with completed relationship maps
- **Update Frequency**: How often maps are refreshed with new intelligence
- **Deal Velocity Impact**: Change in sales cycle length post-implementation
- **Executive Engagement**: Increase in C-suite meetings after mapping
- **Champion Activation**: Success rate in converting influencers to champions

### Data Quality Metrics
- **Stakeholder Accuracy**: % of mapped contacts still accurate after 90 days
- **Relationship Validity**: % of org chart relationships confirmed by stakeholders
- **Evidence Strength**: Average number of evidence points per stakeholder classification
- **Risk Prediction**: % of identified risks that materialize without intervention
- **Action Plan Execution**: % of strategic recommendations actually implemented

### Business Impact Tracking
- **Revenue Attribution**: Deals influenced by relationship mapping
- **Account Expansion**: Upsell/cross-sell success rate improvement
- **Renewal Security**: Reduction in churn risk through early relationship gap identification
- **Competitive Wins**: Success rate against competitors through relationship advantage
- **Customer Satisfaction**: Account health improvements post-mapping

---

## Advanced Features & Extensions

### AI-Powered Enhancements
```python
# Future AI capabilities for template enhancement
def generate_smart_recommendations(stakeholder_data, communication_patterns, industry_context):
    recommendations = []
    
    # Pattern recognition for relationship gaps
    if detect_missing_executive_engagement(stakeholder_data):
        recommendations.append({
            "type": "executive_engagement",
            "priority": "high",
            "specific_action": generate_executive_intro_strategy(stakeholder_data),
            "timeline": "30_days"
        })
    
    # Communication frequency analysis
    communication_health = analyze_communication_patterns(communication_patterns)
    if communication_health["champion_engagement"] < 0.7:
        recommendations.append({
            "type": "champion_activation",
            "priority": "medium",
            "specific_action": generate_champion_engagement_plan(stakeholder_data),
            "timeline": "14_days"
        })
    
    return recommendations
```

### Integration Capabilities
- **CRM Sync**: Bi-directional updates with Salesforce, HubSpot, etc.
- **Calendar Integration**: Track relationship-building meeting frequency
- **Email Intelligence**: Monitor stakeholder communication patterns
- **Competitive Analysis**: Track mentions of competitors in stakeholder communications
- **Account Health Scoring**: Automated relationship strength calculations

### Collaboration Features
- **Team Sharing**: Multi-user access with role-based permissions
- **Version Control**: Track changes and updates to relationship maps
- **Comment System**: Team collaboration on stakeholder insights
- **Alert System**: Notifications for relationship risks or opportunities
- **Executive Reporting**: Summary dashboards for sales leadership

---

## Getting Started Checklist

### Initial Setup
1. [ ] **Access Verification**: Confirm Backstory MCP tool availability
2. [ ] **Template Selection**: Choose appropriate template for account size
3. [ ] **Account Identification**: Target account selection with business justification
4. [ ] **Success Criteria**: Define specific outcomes expected from mapping

### Execution Phase
1. [ ] **Data Gathering**: Complete Backstory intelligence workflow
2. [ ] **Stakeholder Classification**: Evidence-based role identification
3. [ ] **Template Population**: Systematic data input with verification
4. [ ] **Quality Review**: Full checklist validation before delivery

### Activation & Maintenance
1. [ ] **Stakeholder Validation**: Confirm accuracy with account team
2. [ ] **Action Plan Execution**: Implement strategic recommendations
3. [ ] **Progress Tracking**: Monitor relationship development metrics
4. [ ] **Regular Updates**: Monthly refresh of stakeholder intelligence

---

## Template File Organization

```
relationship-mapping-templates/
├── core-templates/
│   ├── enterprise_template.html
│   ├── midmarket_template.html
│   └── smb_template.html
├── industry-variations/
│   ├── technology_template.html
│   ├── financial_services_template.html
│   └── healthcare_template.html
├── customization-guides/
│   ├── template_customization_guide.md
│   ├── industry_configuration_guide.md
│   └── visual_design_standards.md
└── quality-assurance/
    ├── verification_checklist.md
    ├── testing_procedures.md
    └── success_metrics_framework.md
```

**Remember**: This system's effectiveness comes from combining **verified Backstory intelligence** with **professional template design** and **systematic quality assurance**. Every stakeholder, influence assessment, and strategic recommendation must be grounded in actual communication data and CRM intelligence.