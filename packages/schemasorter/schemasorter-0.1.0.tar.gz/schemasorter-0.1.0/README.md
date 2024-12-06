# SchemaSorter

SchemaSorter is a Python library that automatically sorts SQL CREATE TABLE statements based on their foreign key dependencies using topological sorting. This ensures that tables are created in the correct order, preventing foreign key constraint violations during schema creation.

## Features

- Automatically sorts CREATE TABLE statements based on dependencies
- Handles foreign key relationships
- Detects circular dependencies
- Optionally formats SQL with uppercase keywords
- Maintains original SQL formatting and comments

## Installation

```bash
pip install schemasorter
```

## Usage

```python
from schemasorter import sort_tables

# Example SQL DDL
sql_ddl = """
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);
"""

# Sort tables based on dependencies
sorted_ddl = sort_tables(sql_ddl)
print(sorted_ddl)
```

The above example will output the CREATE TABLE statements in the correct order, with `customers` table first (since `orders` depends on it).

## How It Works

1. The library parses the input SQL DDL and extracts table definitions and their foreign key relationships
2. It builds a dependency graph based on the foreign key constraints
3. Uses Khan's algorithm to perform topological sorting on the tables
4. Returns the sorted CREATE TABLE statements in the correct order

## Parameters

`sort_tables(sql_ddl: str, should_format: bool = True) -> str`

- `sql_ddl`: SQL DDL string containing CREATE TABLE statements
- `should_format`: Whether to format and uppercase SQL keywords (default: True)

## Error Handling

The library will raise a `ValueError` if it detects circular dependencies between tables.

## Limitations

- Currently only handles CREATE TABLE statements
- Foreign key relationships must be explicitly defined using FOREIGN KEY constraints
- Does not handle ALTER TABLE statements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
