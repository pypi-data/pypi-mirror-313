# CogniDB

A utility that provides seamless database access to your agents with a single line of code.

## Installation

```bash
pip install cognidb
```

## Configuration

### Using Environment Variables (.env)

```bash
# Database Settings
HOST=localhost
PORT=3306
DATABASE=your_database
USER=your_username
PASSWORD=your_password

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key
```

### Using Python Code

```python
from cognidb import CogniDB

db = CogniDB(
    db_type="mysql",  # or "postgresql"
    host="localhost",
    port=3306,
    dbname="your_database",
    user="your_username",
    password="your_password",
    api_key="your-openai-api-key"  # Optional if set in .env
)
```

## Quick Start

```python
from cognidb import CogniDB

# Initialize using environment variables
db = CogniDB(db_type="mysql")

# Simple query
result = db.query("Show me all customers")

# Query with potential clarification
result = db.query("Show transactions from last month")
```

## Example Queries

```python
# Basic queries
customers = db.query("List all premium customers")

# Aggregations
summary = db.query("Total sales by product category")

# Complex queries
analysis = db.query("Find customers who spent more than average")
```

## Error Handling

```python
try:
    db = CogniDB(db_type="mysql")
    result = db.query("Show customer accounts")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Query error: {e}")
```

## Dependencies

- openai
- psycopg2
- mysql-connector-python
- sqlparse
- psycopg2-binary

## License

MIT License © 2024

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For support or questions, contact:
Rishabh Kumar
[rishabh.vaaiv@gmail.com](mailto:rishabh.vaaiv@gmail.com)
