# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the "T-Minus-15: Secrets of an Elite DevOps Team" book repository. It contains:
- **Book content**: AsciiDoc files for chapters, appendices, and supporting content
- **AI Agents**: Configuration and deployment for AI agents (Edmund, Danny, Ollie, Pepper, Poppy, Teddy)
- **Build system**: GitHub Actions workflows for book compilation and agent deployment
- **Themes**: Custom PDF styling for book output

## Key Commands

### Book Building
```bash
# Build PDF book (requires asciidoctor and asciidoctor-pdf)
sudo apt-get install -y asciidoctor
sudo gem install asciidoctor-pdf
asciidoctor-pdf -a pdf-theme=tminus15-theme.yml -a pdf-themesdir=themes book.adoc -o book.pdf --trace -v
```

### Azure AI Agent Deployment (Unified Project)
```bash
# Install Azure CLI (one-time setup)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Deploy all T-Minus-15 agents to unified project
gh workflow run deploy-tminus15-agents.yml -f environment=development

# Agents auto-deploy on push to main when agent files or book content changes
# The T-Minus-15 PDF is built and used as shared knowledge source
```

### Agent Testing (Edmund)
```bash
cd agents/edmund
python -m pip install -r requirements.txt
python test_edmund_local.py
python test_config.py
```

### Configuration Validation
```bash
# Validate JSON configurations
python -m json.tool agents/edmund/agent-config.json

# Validate YAML files
python -c "import yaml; yaml.safe_load(open('agents/edmund/deployment.yaml'))"
```

## Architecture

### Book Structure
- `book.adoc`: Main book file that includes all chapters and appendices
- `chapters/`: Individual chapter files in AsciiDoc format
- `appendices/`: Supporting appendices with metadata definitions
- `themes/`: PDF styling theme (`tminus15-theme.yml`)
- `images/`: Book illustrations and diagrams

### AI Agents (The Avengers of Agile)
All T-Minus-15 agents are deployed to a unified Azure AI Foundry project for seamless collaboration:

- **Edmund (the Engineer)**: Development, DevOps, and infrastructure (GPT-4o)
- **Danny (the Designer)**: UX/UI design and architecture (GPT-4o + DALL-E)
- **Ollie (the Operator)**: Operations, monitoring, and SRE (GPT-4o-mini)
- **Pepper (the Planner)**: Requirements analysis and planning (GPT-4o)
- **Poppy (the PM)**: Project management and coordination (GPT-4o-mini)
- **Teddy (the Tester)**: Quality assurance and testing (GPT-4o-mini)

### Unified Deployment Architecture
- **Shared AI Foundry Project**: `tminus15-agents-project` houses all agents
- **Shared Knowledge Base**: T-Minus-15 PDF (built from this repo) + GitHub repository
- **AutoGen Ready**: All agents can collaborate in multi-agent conversations
- **Specialized Models**: Each agent uses optimal model for their role
- **Resource Group**: `rg-tminus15-agents` contains all shared infrastructure

### Deployment Workflows
- **Book Build**: `.github/workflows/build-book.yml` - Compiles book to PDF and creates GitHub releases
- **Unified Agent Deploy**: `.github/workflows/deploy-tminus15-agents.yml` - Deploys all T-Minus-15 agents to shared Azure AI Foundry project with PDF knowledge source

## File Formats
- **Content**: AsciiDoc (`.adoc`) for all book content
- **Configuration**: JSON for agent configs, YAML for deployments
- **Themes**: YAML-based PDF theme configuration

## Important Notes
- Book builds are triggered automatically on pushes to main (excluding agents directory)
- Agent deployments are triggered by changes to `agents/edmund/**`
- The book uses custom chapter numbering (Steps instead of Chapters)
- All book proceeds are donated to Bitcoin Smiles charity