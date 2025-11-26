# Polix - AI Compliance Audit System

Polix is a full-stack agentic AI system for automated compliance auditing, combining RAG, LangChain agents, LangGraph workflows, and MCP tools.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Installation

1. **Backend**:
   ```bash
   # Install uv (if not installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv pip install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   # Edit .env with your OpenAI API key
   
   # Run backend
   uv run uvicorn backend.app.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Docker (Recommended)**:
   ```bash
   docker-compose up -d
   ```

## Documentation

- **[Full Documentation](./docs/readme.md)** - Complete setup and usage guide
- **[Architecture](./docs/architecture.md)** - System architecture and design
- **[Models](./docs/models.md)** - AI models used in Polix
- **[Using uv](./docs/uv-setup.md)** - Guide for using uv package manager

## Features

- 📋 Policy Analysis
- 🔍 Compliance Auditing  
- 📊 Automated Reporting
- 🤖 Agent-Based Workflows
- 🔎 RAG System
- 🛠️ MCP Tools

## Project Structure

```
polix/
├── backend/       # FastAPI backend
├── frontend/      # React frontend
├── docs/         # Documentation
├── pyproject.toml # Python project configuration (for uv)
└── requirements.txt
```

## License

[Add your license here]

