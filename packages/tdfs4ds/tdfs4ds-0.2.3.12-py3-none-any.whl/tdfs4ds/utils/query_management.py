import teradataml as tdml
import functools
from packaging import version
def is_version_greater_than(tested_version, base_version="17.20.00.03"):
    """
    Check if the tested version is greater than the base version.

    This function compares two version numbers, the 'tested_version' and the 'base_version',
    to determine if the 'tested_version' is greater. It uses Python's `version.parse` function
    to perform the comparison.

    Args:
        tested_version (str): Version number to be tested.
        base_version (str, optional): Base version number to compare. Defaults to "17.20.00.03".

    Returns:
        bool: True if the 'tested_version' is greater than the 'base_version', False otherwise.

    Example:
        To check if a version is greater than the default base version:
        >>> is_greater = is_version_greater_than("17.20.00.04")

        To check if a version is greater than a custom base version:
        >>> is_greater = is_version_greater_than("18.10.00.01", base_version="18.00.00.00")

    """
    return version.parse(tested_version) > version.parse(base_version)
def execute_query_wrapper(f):
    """
    Decorator to execute a query. It wraps around the function and adds exception handling.

    This decorator is used to wrap around a function that generates a query and execute that query.
    It handles exceptions during query execution and prints the error message along with the query.
    The decorator works with both TeradataML's `tdml` and legacy `tdml.get_context()` execution methods,
    depending on the TeradataML version.

    Args:
        f (function): Function to be decorated.

    Returns:
        function: Decorated function.

    Example:
        To decorate a function that generates and executes a query:
        >>> @execute_query_wrapper
        >>> def my_query_function():
        >>>     return "SELECT * FROM my_table"

        This decorator can be applied to functions that generate and execute queries with ease.
    """
    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        query = f(*args, **kwargs)
        if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
            if type(query) == list:
                for q in query:
                    try:
                        tdml.execute_sql(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.execute_sql(query)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(query)
        else:
            if type(query) == list:
                for q in query:
                    try:
                        tdml.get_context().execute(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.get_context().execute(query)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(query)
        return

    return wrapped_f


def execute_query(query):
    """
    Execute a SQL query or a list of queries using the tdml module.

    This function checks the version of the tdml module and executes the query or queries accordingly.
    For versions greater than 17.20.00.03, it uses `tdml.execute_sql`; otherwise, it uses `tdml.get_context().execute`.

    Args:
        query (str or list): A single SQL query string or a list of SQL query strings.

    Returns:
        The result of the SQL execution if a single query is passed. None if a list of queries is passed or an exception occurs.

    Example:
        To execute a single SQL query and retrieve the result:
        >>> result = execute_query("SELECT * FROM my_table")

        To execute a list of SQL queries:
        >>> execute_query(["UPDATE table1 SET column1 = 42", "DELETE FROM table2 WHERE condition"])

    Note:
        - If a single query is passed, the function returns the result of the SQL execution.
        - If a list of queries is passed, the function executes each query and returns None.
        - If an exception occurs during execution, the error message and the problematic query are printed,
          and the function returns None.

    """
    # Check if the version of tdml is greater than the specified base version
    if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
        # If query is a list, iterate and execute each query
        if type(query) == list:
            for q in query:
                try:
                    tdml.execute_sql(q)  # Execute the query
                except Exception as e:
                    # Print the first line of the exception and the query that caused it
                    print(str(e).split('\n')[0])
                    print(q)
        else:
            # If query is not a list, execute it and return the result
            try:
                return tdml.execute_sql(query)
            except Exception as e:
                # Print the first line of the exception and the query
                print(str(e).split('\n')[0])
                print(query)
    else:
        # For tdml versions not greater than the specified version
        if type(query) == list:
            for q in query:
                try:
                    # Use the older execution method for the query
                    tdml.get_context().execute(q)
                except Exception as e:
                    # Print the first line of the exception and the query
                    print(str(e).split('\n')[0])
                    print(q)
        else:
            try:
                # Execute the single query using the older method and return the result
                return tdml.get_context().execute(query)
            except Exception as e:
                # Print the first line of the exception and the query
                print(str(e).split('\n')[0])
                print(query)

    # No return value if a list of queries is executed or if an exception occurs
    return