# Using uv with Polix

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. Polix is configured to work with uv for faster dependency management.

## Installation

### Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip:**
```bash
pip install uv
```

## Usage

### Initial Setup

1. **Create virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

   Or if you prefer using pyproject.toml:
   ```bash
   uv pip install -e .
   ```

3. **Generate lock file (optional):**
   ```bash
   uv lock
   ```

   This creates `uv.lock` with pinned versions for reproducible builds.

### Running the Application

**Run backend with uv:**
```bash
uv run uvicorn backend.app.main:app --reload
```

**Run scripts:**
```bash
uv run python backend/app/main.py
```

### Sync Dependencies

To sync your environment with requirements.txt:
```bash
uv pip sync requirements.txt
```

### Add New Dependencies

**Add a package:**
```bash
uv pip install package-name
```

**Add and update requirements.txt:**
```bash
uv pip install package-name
uv pip freeze > requirements.txt
```

## Benefits of uv

- **10-100x faster** than pip for dependency resolution
- Drop-in replacement for pip
- Better dependency resolution
- Works with existing requirements.txt and pyproject.toml
- Built-in virtual environment management

## Docker with uv

The Dockerfile is already configured to use uv for faster builds. The uv binary is copied from the official uv Docker image, making installations much faster than traditional pip.

