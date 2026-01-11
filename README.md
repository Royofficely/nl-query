<h1 align="center">NL Query</h1>

<h4 align="center">Query your PostgreSQL or MySQL database using natural language. No SQL required.</h4>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  </a>
  <a href="https://github.com/Royofficely/nl-query/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Royofficely/nl-query" alt="License">
  </a>
  <a href="https://github.com/Royofficely/nl-query/stargazers">
    <img src="https://img.shields.io/github/stars/Royofficely/nl-query?style=social" alt="Stars">
  </a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-why-nl-query">Why NL Query</a> •
  <a href="#-features">Features</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## Quick Start

```bash
# Clone and configure
git clone https://github.com/Royofficely/nl-query.git
cd nl-query
cp .env.example .env

# Add your database credentials and OpenAI key to .env

# Install and run
pip install -r requirements.txt
python nl_postgres_query.py analyze  # First time: analyze your DB
python nl_postgres_query.py query    # Start querying
```

**That's it.** Ask questions like "Show me all users who signed up last month"

---

## Why NL Query?

| Problem | How We Solve It |
|---------|-----------------|
| **Need SQL knowledge** | Ask questions in plain English |
| **Complex joins** | AI understands table relationships automatically |
| **Learning DB structure** | Analyze command maps your entire schema |
| **Typos in queries** | Smart clarification asks what you meant |
| **Context switching** | Chat history remembers previous queries |
| **Multi-database setup** | Works with PostgreSQL and MySQL |

---

## Features

```
Multi-LLM Support      OpenAI, Claude, Ollama, vLLM, and more
Natural Language       Ask questions in plain English, get SQL results
Multi-Database         PostgreSQL and MySQL support
Schema Analysis        Automatic database structure discovery
Smart Clarification    Suggests alternatives when queries are unclear
Chat History           Context-aware follow-up questions
Query Optimization     AI optimizes generated SQL for performance
Docker Ready           One-command deployment with Docker Compose
Colorful CLI           Rich, informative console output
```

---

## Usage

### 1. Analyze Your Database (First Time)

```bash
python nl_postgres_query.py analyze
```

This will:
- Connect to your database
- Analyze all tables and columns
- Generate a visual schema tree
- Save structure for future queries

### 2. Start Querying

```bash
python nl_postgres_query.py query
```

### Example Queries

| Query Type | Example |
|------------|---------|
| **Simple** | "Show me all users" |
| **Filtered** | "Users who signed up in the last month" |
| **Aggregation** | "Total revenue by product category" |
| **Top N** | "Top 5 customers by order value" |
| **Time-based** | "Daily transactions for the past week" |
| **Follow-up** | "Now filter those by region" |

<details>
<summary><strong>More Examples</strong></summary>

```
> Show me all orders from last week
Generated SQL: SELECT * FROM orders WHERE created_at >= '2024-01-08'...

> What's the average order value?
Generated SQL: SELECT AVG(total_amount) FROM orders...

> Break it down by customer type
Generated SQL: SELECT customer_type, AVG(total_amount)...
```

</details>

---

## Configuration

### Database Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DB_TYPE` | Yes | postgres | Database type (postgres/mysql) |
| `DB_NAME` | Yes | - | Database name |
| `DB_USER` | Yes | - | Database username |
| `DB_PASSWORD` | Yes | - | Database password |
| `DB_HOST` | Yes | localhost | Database host |
| `DB_PORT` | Yes | 5432 | Database port |

### LLM Provider Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | openai | Provider: openai, anthropic, ollama, vllm, openai-compatible |
| `LLM_MODEL` | No | varies | Model name (provider-specific) |
| `LLM_BASE_URL` | No | - | Custom API endpoint |

<details>
<summary><strong>OpenAI (GPT-4, GPT-4o, GPT-3.5)</strong></summary>

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
LLM_MODEL=gpt-4o  # or gpt-4, gpt-3.5-turbo
```

</details>

<details>
<summary><strong>Anthropic (Claude)</strong></summary>

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
LLM_MODEL=claude-sonnet-4-20250514  # or claude-3-opus, claude-3-haiku
```

</details>

<details>
<summary><strong>Ollama (Local Models)</strong></summary>

```bash
# First, install Ollama and pull a model:
# ollama pull llama3.1

LLM_PROVIDER=ollama
LLM_MODEL=llama3.1  # or mistral, codellama, etc.
LLM_BASE_URL=http://localhost:11434
```

</details>

<details>
<summary><strong>vLLM (Self-Hosted)</strong></summary>

```bash
LLM_PROVIDER=vllm
LLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
LLM_BASE_URL=http://localhost:8000/v1
```

</details>

<details>
<summary><strong>OpenAI-Compatible APIs (LM Studio, LocalAI, Groq, Together)</strong></summary>

```bash
LLM_PROVIDER=openai-compatible
LLM_MODEL=your-model-name
LLM_BASE_URL=http://localhost:1234/v1
OPENAI_API_KEY=your-api-key  # or EMPTY for local
```

</details>

<details>
<summary><strong>Docker Setup</strong></summary>

```bash
# Configure
cp .env.example .env
# Edit .env with your settings

# Run with Docker
docker-compose run --rm nlquery analyze
docker-compose run --rm nlquery query
```

Note: Use `host.docker.internal` as DB_HOST to connect to databases on your host machine.

</details>

---

## How It Works

```
User Query          "Show users from California"
     |
     v
Query Optimizer     Analyzes schema, adds context
     |
     v
SQL Generator       SELECT * FROM users WHERE state = 'California'
     |
     v
Query Executor      Runs against your database
     |
     v
Results             Formatted table output
```

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| **Business Analytics** | Query sales data without SQL |
| **Data Exploration** | Quickly understand new databases |
| **Reporting** | Generate insights for non-technical users |
| **Development** | Prototype queries before writing SQL |
| **Support** | Let support teams query customer data |
| **Learning** | Understand SQL by seeing generated queries |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Check DB_HOST and DB_PORT in .env |
| Authentication failed | Verify DB_USER and DB_PASSWORD |
| OpenAI rate limit | Wait a moment or use GPT-3.5-turbo |
| Wrong results | Run `analyze` again to refresh schema |
| Slow queries | Generated SQL shown - optimize manually if needed |

---

## Requirements

- Python 3.9+
- PostgreSQL or MySQL database
- LLM API key (OpenAI, Anthropic) or local model (Ollama, vLLM)

```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## AI Prompt

Copy this to quickly set up NL Query with AI assistants:

```
I need to query my database with natural language. Use NL Query from github.com/Royofficely/nl-query

Setup:
1. Clone repo, copy .env.example to .env
2. Add database credentials (DB_TYPE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
3. Choose LLM provider (LLM_PROVIDER) and add API key
   - OpenAI: OPENAI_API_KEY
   - Claude: ANTHROPIC_API_KEY
   - Ollama: just set LLM_MODEL (e.g., llama3.1)
4. pip install -r requirements.txt
5. python nl_postgres_query.py analyze (first time)
6. python nl_postgres_query.py query (start querying)

Example: "Show me all users who signed up last month"
```

---

<p align="center">
  <sub>Built by <a href="https://github.com/Royofficely">Roy Nativ</a> at <a href="https://officely.ai">Officely AI</a></sub>
</p>

<p align="center">
  <a href="https://github.com/Royofficely/nl-query/issues">Report Bug</a> •
  <a href="https://github.com/Royofficely/nl-query/issues">Request Feature</a>
</p>
