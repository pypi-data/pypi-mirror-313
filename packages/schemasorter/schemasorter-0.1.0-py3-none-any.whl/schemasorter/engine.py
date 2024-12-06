from collections import defaultdict, deque


def parse_sql_tables(sql_input: str) -> dict:
    """
    Parse SQL CREATE TABLE statements and extract table dependencies.

    Args:
        sql_input (str): SQL statements as a string

    Returns:
        dict: Dictionary containing table names as keys, with their references and statements
              Format: {table_name: {'references': [referenced_tables], 'stmt': [sql_statements]}}
    """
    sql_lines = sql_input.splitlines()
    sql_statements: list[list[str]] = []

    current_statement: list[str] = []
    for line in sql_lines:
        if line:
            current_statement.append(line)
        if not line.startswith("--") and line.endswith(";"):
            sql_statements.append(current_statement)
            current_statement = []

    table_definitions = {}
    for statement in sql_statements:
        table_name = None
        current_lines = []
        for line in statement:
            current_lines.append(line)
            if line.lower().startswith("create table"):
                table_name = line.split(" ")[2]
                table_definitions[table_name] = {"references": [], "stmt": []}
            if "constraint" in line.lower() and "foreign key" in line.lower():
                tokens = line.lower().split(" ")
                referenced_table = tokens[tokens.index("references") + 1]
                table_definitions[table_name]["references"].append(referenced_table)
            if line.endswith(");"):
                table_definitions[table_name]["stmt"] = current_lines
                table_name = None
                current_lines = []
    return table_definitions


def topological_sort_khan(table_definitions: dict) -> list:
    """
    Performs Khan's algorithm for topological sorting on table definitions.

    Args:
        table_definitions (dict): Dictionary containing table definitions and their dependencies
            Format: {table_name: {'references': [referenced_tables], 'stmt': [sql_statements]}}

    Returns:
        list: List of dictionaries containing sorted table definitions
            Format: [{'table_name': name, 'references': [refs], 'stmt': [stmts]}]

    Raises:
        ValueError: If the dependency graph contains a cycle
    """
    dependency_graph = defaultdict(list)
    dependency_count = defaultdict(int)

    for table_name, table_info in table_definitions.items():
        dependency_count[table_name]
        for referenced_table in table_info["references"]:
            dependency_graph[referenced_table].append(table_name)
            dependency_count[table_name] += 1

    tables_without_deps = deque(
        [table for table, count in dependency_count.items() if count == 0]
    )

    sorted_tables = []
    while tables_without_deps:
        current_table = tables_without_deps.popleft()
        sorted_tables.append(current_table)

        for dependent_table in dependency_graph[current_table]:
            dependency_count[dependent_table] -= 1
            if dependency_count[dependent_table] == 0:
                tables_without_deps.append(dependent_table)

    if len(sorted_tables) != len(table_definitions):
        raise ValueError("The graph contains a cycle - cannot perform topological sort")

    result_tables = []
    for table in sorted_tables:
        table_entry = {"table_name": table, **table_definitions[table]}
        result_tables.append(table_entry)
    return result_tables
