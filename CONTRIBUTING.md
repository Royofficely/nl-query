# Contributing to NL Query

Thank you for your interest in contributing!

## How to Contribute

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
4. **Make your changes**
5. **Test** your changes work correctly
6. **Commit** with a clear message (`git commit -m 'Add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/nl-query.git
cd nl-query
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your test database credentials
```

## Code Style

- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Follow PEP 8 guidelines

## Testing

Before submitting a PR, ensure:
- [ ] `python nl_postgres_query.py analyze` works
- [ ] `python nl_postgres_query.py query` responds correctly
- [ ] No hardcoded credentials or API keys

## Reporting Issues

When reporting issues, please include:
- Python version
- Database type (PostgreSQL/MySQL)
- Error message
- Steps to reproduce

## Questions?

Open an issue or reach out to [@Royofficely](https://github.com/Royofficely)
