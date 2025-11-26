# Polix - AI Compliance Audit System

Polix is a full-stack agentic AI system for automated compliance auditing. It uses RAG, LangChain agents, LangGraph workflows, and MCP tools to analyze policies and perform compliance checks.

## Features

- 📋 **Policy Analysis**: Understand and extract requirements from policy documents
- 🔍 **Compliance Auditing**: Automated compliance checks against policies
- 📊 **Report Generation**: Comprehensive audit reports with recommendations
- 🤖 **Agent-Based Workflows**: Orchestrated multi-agent workflows using LangGraph
- 🔎 **RAG System**: Retrieve relevant context from knowledge base
- 🛠️ **MCP Tools**: Extend capabilities with GitHub and file system access

## Project Structure

```
polix/
├── backend/
│   └── app/
│       ├── api/              # API routes
│       ├── core/             # Configuration and logging
│       ├── rag/              # RAG system
│       ├── agents/           # LangChain agents
│       ├── graph/            # LangGraph workflows
│       ├── mcp/              # MCP tools
│       ├── utils/            # Utility functions
│       └── main.py           # FastAPI application
├── frontend/
│   └── src/
│       ├── components/       # React components
│       ├── pages/            # React pages
│       └── App.jsx           # Main app component
├── docs/                     # Documentation
├── pyproject.toml           # Python project config (for uv)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Backend Docker image
├── docker-compose.yml       # Multi-container setup
└── .env.example            # Environment variables template
```

## Prerequisites

- Python 3.11+
- **uv** (recommended) or pip for Python package management - [Installation Guide](./uv-setup.md)
- Node.js 18+
- Docker and Docker Compose (optional, for containerized deployment)
- OpenAI API key (or configure local Qwen model)

## Installation

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd polix
   ```

2. **Install uv** (if not already installed):
   ```bash
   # On macOS/Linux:
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows (PowerShell):
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip:
   pip install uv
   ```

3. **Install dependencies using uv**:
   ```bash
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   
   # Or use uv directly (no venv needed):
   uv pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Create necessary directories**:
   ```bash
   mkdir -p data/vectorstore logs
   ```

6. **Run the backend**:
   ```bash
   cd backend
   python -m app.main
   # Or use uvicorn directly:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   # Or with uv:
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`.

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and start all services**:
   ```bash
   docker-compose up -d
   ```

This will start:
- Backend API on port 8000
- ChromaDB on port 8001
- Frontend on port 3000

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop services**:
   ```bash
   docker-compose down
   ```

### Individual Docker Containers

1. **Build backend image**:
   ```bash
   docker build -t polix-backend .
   ```

2. **Run backend container**:
   ```bash
   docker run -p 8000:8000 --env-file .env polix-backend
   ```

## Usage

### API Endpoints

#### Health Check
```bash
GET http://localhost:8000/health/
```

#### RAG Query
```bash
POST http://localhost:8000/query/
Content-Type: application/json

{
  "question": "What are the data privacy requirements?",
  "top_k": 5
}
```

#### Audit Workflow
```bash
POST http://localhost:8000/agent/audit
Content-Type: application/json

{
  "query": "Check compliance with GDPR",
  "policy_document": "Policy text here...",
  "external_data_source": "External data here..."
}
```

### Frontend Usage

1. **Home Page**: Use the chat interface to ask questions about compliance
2. **Upload Page**: Upload policy documents (PDF, TXT, DOC)
3. **Audit Page**: Run automated compliance audits and view results

## Configuration

### Environment Variables

Key configuration options in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `VECTOR_STORE_TYPE`: `chromadb` or `faiss`
- `EMBEDDING_MODEL`: Embedding model name
- `LLM_MODEL`: LLM model name
- `MCP_ENABLED`: Enable/disable MCP tools
- `GITHUB_TOKEN`: GitHub token for repository access

See `.env.example` for all available options.

## Development

### Backend Development

- Use `uvicorn app.main:app --reload` for auto-reload during development
- Logs are stored in `logs/polix.log`
- Vector store data is stored in `data/vectorstore/`

### Frontend Development

- Use `npm run dev` for Vite dev server with hot module replacement
- API proxy is configured in `vite.config.js`

### Running Tests

(Add test commands once tests are implemented)

## Troubleshooting

### Backend Issues

- **Import errors**: Ensure `PYTHONPATH` includes the project root
- **Vector store errors**: Check that `data/vectorstore/` directory exists
- **OpenAI errors**: Verify `OPENAI_API_KEY` is set correctly

### Frontend Issues

- **API connection errors**: Check backend is running on port 8000
- **Build errors**: Clear `node_modules` and reinstall dependencies

### Docker Issues

- **Port conflicts**: Change ports in `docker-compose.yml`
- **Volume permissions**: Ensure directories are writable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `docs/`
- Review the architecture documentation in `docs/architecture.md`

## Roadmap

- [ ] Human approval workflow integration
- [ ] Real-time workflow updates via WebSockets
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard
- [ ] More MCP tool integrations
- [ ] Unit and integration tests
- [ ] CI/CD pipeline

