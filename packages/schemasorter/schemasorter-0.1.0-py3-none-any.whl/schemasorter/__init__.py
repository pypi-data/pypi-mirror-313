import sqlparse

from schemasorter.engine import parse_sql_tables, topological_sort_khan


def sort_tables(sql_ddl: str, should_format: bool = True) -> str:
    """Sort SQL table definitions topologically based on foreign key dependencies.

    Args:
        sql_ddl (str): SQL DDL string containing CREATE TABLE statements
        should_format (bool, optional): Whether to format and uppercase SQL keywords. Defaults to True.

    Returns:
        str: Sorted and formatted DDL statements with tables ordered by dependencies
    """
    if should_format:
        sql_ddl = sqlparse.format(sql_ddl, keyword_case="upper")
    parsed_tables = parse_sql_tables(sql_ddl)
    sorted_tables = topological_sort_khan(parsed_tables)

    formatted_output = ""
    for table in sorted_tables:
        for sql_line in table["stmt"]:
            formatted_output += sql_line + "\n"
            if sql_line == ");":
                formatted_output += "\n\n"
    return formatted_output
