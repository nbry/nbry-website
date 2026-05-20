# NBRY Multi-Site Platform

A collection of independent websites under the NBRY domain, built with FastAPI and subdomain routing.

## Architecture Overview

This project hosts multiple independent websites under a single deployment:

- **nbry.com** - Main landing page with links to all sub-sites
- **lifting.nbry.com** - Strength training program and resources
- **coffee.nbry.com** - Coffee content (coming soon)
- **career.nbry.com** - Career portfolio (coming soon)

Each site is a self-contained FastAPI application with its own templates, static files, and routes. The master app uses subdomain-based routing to delegate requests to the appropriate site.

## Directory Structure

```
src/nbry_website/
├── main.py                    # Master app with subdomain routing middleware
├── config.py                  # Shared configuration (Pydantic settings)
├── sites/                     # Independent site applications
│   ├── landing/              # nbry.com
│   │   ├── app.py
│   │   ├── templates/
│   │   └── static/
│   └── lifting/              # lifting.nbry.com
│       ├── app.py
│       ├── routes.py
│       ├── templates/
│       ├── static/
│       ├── configs/         # TOML program configurations
│       └── lib/             # Site-specific utilities
└── shared/                   # Shared utilities across all sites
    └── config_loader.py     # Generic TOML loader
```

## Development Setup

### Prerequisites

- Python 3.14
- uv (Python package manager)
- PostgreSQL 16
- Redis 7

### Installation

1. Clone the repository
2. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Start services (Docker):
   ```bash
   docker-compose -f .devcontainer/docker-compose.yml up -d postgres redis
   ```

## Running the Application

### Option 1: Multi-Port Development (Recommended)

Run each site independently on different ports:

```bash
# Terminal 1: Landing page
uv run nbry-landing --reload --port 8000

# Terminal 2: Lifting site
uv run nbry-lifting --reload --port 8001
```

Access sites:
- Landing: http://localhost:8000
- Lifting: http://localhost:8001

**Best for:** Daily development, fastest iteration, no subdomain configuration needed.

### Option 2: Local Subdomains

Test the full subdomain routing locally:

1. Edit `/etc/hosts` (requires sudo):
   ```
   127.0.0.1  nbry.local
   127.0.0.1  lifting.nbry.local
   127.0.0.1  coffee.nbry.local
   127.0.0.1  career.nbry.local
   ```

2. Run the master app:
   ```bash
   uv run nbry-web --reload --host 0.0.0.0 --port 8000
   ```

3. Access sites:
   - http://nbry.local:8000 - Landing page
   - http://lifting.nbry.local:8000 - Lifting site

**Best for:** Testing subdomain routing, integration testing, pre-deployment validation.

### Option 3: Docker Compose

Full environment with all services:

```bash
docker-compose -f .devcontainer/docker-compose.yml up
```

## Environment Configuration

Environment variables are configured in `.env` (copy from `.env.example`):

- `SITE_MODE` - `development` or `production`
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ROOT_DOMAIN` - Production domain (e.g., `nbry.com`)
- `LOCAL_DOMAIN` - Local development domain (e.g., `nbry.local`)
- `ALLOWED_SUBDOMAINS` - Comma-separated list of valid subdomains
- `LIFTING_SITE_ENABLED` - Enable/disable lifting site
- `COFFEE_SITE_ENABLED` - Enable/disable coffee site
- `CAREER_SITE_ENABLED` - Enable/disable career site

## How Subdomain Routing Works

The `SubdomainRoutingMiddleware` in `main.py` extracts the subdomain from the `Host` header and routes requests to the appropriate site app:

1. Request arrives: `lifting.nbry.com/philosophy`
2. Middleware extracts subdomain: `"lifting"`
3. Looks up site app in `SITE_APPS` mapping
4. Delegates request to `lifting_app`
5. Site app handles route and returns response

Unknown subdomains redirect to the landing page.
