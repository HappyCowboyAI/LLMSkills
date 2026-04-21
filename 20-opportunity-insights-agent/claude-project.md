# Claude Project Setup — Opportunity Insights Agent

## Project URL
https://claude.ai/project/019d21b3-2c4e-71e2-8f9d-87e44191d9ee

## Setup Instructions

1. Open Claude.ai → Projects → Create New Project
2. Name it "Opportunity Insights"
3. Under **Custom Instructions**, paste the full system prompt from `skill.md`
4. Under **MCP Servers**, connect the Backstory MCP
5. Optionally upload `PeopleaiMetricLibrary.csv` as project knowledge for metric slug lookups

## How to Use
Type "Build my pipeline dashboard" or "Analyze my pipeline" and press Enter. The agent will pull live data from Backstory MCP, classify deals, and render an interactive dashboard.

## Deployment Toolkit
Full deployment guide with EDB tables, custom metrics, SalesAI signals, and Slack bot setup:
https://happycowboyai.github.io/opp-insights-guide/
