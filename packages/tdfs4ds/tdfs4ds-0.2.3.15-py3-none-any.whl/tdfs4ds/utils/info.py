import re

import tdfs4ds


def get_column_types(df, columns):
    """
    Retrieve the column types for specified columns from a TeradataML DataFrame.

    This function retrieves the data types of specified columns in a TeradataML DataFrame. It is tailored to work with
    DataFrames that have specific attributes like `_td_column_names_and_types` and `_td_column_names_and_sqlalchemy_types`,
    which are not standard in typical pandas DataFrames.

    Parameters:
    - df (DataFrame): The TeradataML DataFrame from which to get the column types.
    - columns (list or str): A list of column names or a single column name whose types are to be retrieved.

    Returns:
    dict: A dictionary where keys are column names and values are their types, including character set for VARCHAR columns.

    Notes:
    - This function is designed to work with TeradataML DataFrames, which may have extended column type information.
    - For VARCHAR columns, it retrieves the detailed type information, including the character set.

    Dependencies:
    - TeradataML DataFrame containing attributes '_td_column_names_and_types' and '_td_column_names_and_sqlalchemy_types'.
    """

    # Convert columns to a list if it's not already a list
    if type(columns) != list:
        columns = [columns]

    # Build a dictionary of column types for the specified columns
    col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}
    types_ = {x.split()[0]: ''.join(x.split()[1::]) for x in str(df.tdtypes).split('\n')}
    col_type_ = {k: v for k,v in types_.items() if k in columns}

    # Iterate over the column types
    for k, v in col_type.items():
        # Special handling for columns of type VARCHAR
        if 'VARCHAR' in v.upper():
            # Retrieve detailed type information, including character set
            temp = df._td_column_names_and_sqlalchemy_types[k.lower()]
            col_type[k] = f"{temp.compile()} CHARACTER SET {temp.charset}"

    return col_type



def get_column_types_simple(df, columns):
    """
    Retrieve simplified column types for specified columns from a DataFrame.

    This function simplifies the data types of the specified columns in a DataFrame, translating database-specific data types
    (such as INTEGER, BYTEINT, etc.) into more generalized Python data types (e.g., int, float). It assumes the DataFrame has
    a specific attribute '_td_column_names_and_types' that stores column names and their types.

    Parameters:
    - df (DataFrame): The DataFrame from which to get the column types.
    - columns (list or str): A list of column names or a single column name whose types are to be retrieved.

    Returns:
    dict: A dictionary where keys are column names and values are simplified Python data types.

    Notes:
    - This function is designed to work with DataFrames that have a specific attribute '_td_column_names_and_types'.
    - It uses a mapping from specific database column types to simplified Python data types for simplification.

    Dependencies:
    - DataFrame containing the '_td_column_names_and_types' attribute.
    """

    # Ensure that the columns parameter is in list format
    if type(columns) != list:
        columns = [columns]

    # Extract the column types for the specified columns
    #col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}
    types_ = {x.split()[0]: ''.join(x.split()[1::]) for x in str(df.tdtypes).split('\n')}
    col_type = {k: v for k,v in types_.items() if k in columns}

    # Define a mapping from specific database column types to simplified Python data types
    mapping = {'INTEGER': 'int',
               'BYTEINT': 'int',
               'BIGINT': 'int',
               'FLOAT': 'float'
               }

    # Update the column types in the dictionary using the mapping
    for k, v in col_type.items():
        if v in mapping:
            col_type[k] = mapping[v]

    return col_type

def seconds_to_dhms(seconds):
    """
    Converts a duration in seconds to a formatted string representing days, hours, minutes, and seconds with three decimal places.

    Args:
        seconds (float): The duration in seconds.

    Returns:
        str: A formatted string representing the duration in days, hours, minutes, and seconds with three decimal places.
    """
    minutes = int(seconds // 60) % 60
    hours = int(seconds // (60 * 60)) % 24
    days = int(seconds // (60 * 60 * 24))
    seconds = seconds % 60

    # Construct a list of time parts to include in the formatted string
    time_parts = []
    if days > 0:
        time_parts.append(f"{days}d")
    if hours > 0:
        time_parts.append(f"{hours}h")
    if minutes > 0:
        time_parts.append(f"{minutes}m")
    time_parts.append(f"{seconds:.3f}s")

    # Join the time parts into a single string
    formatted_time = " ".join(time_parts)
    return formatted_time

def extract_partition_content(partitioning):
    """
    Extracts the content within the parentheses after 'PARTITION BY' in the given partitioning string.

    Parameters:
        partitioning (str): The input string containing 'PARTITION BY'.

    Returns:
        str: The content within the parentheses after 'PARTITION BY', or None if no match is found.
    """
    # First extraction: Get the content within parentheses after 'PARTITION BY'
    pattern = r'PARTITION\s+BY\s*\(\s*(.*?)\s*\)'
    match = re.search(pattern, partitioning, re.DOTALL)

    if match:
        result = match.group(1)
        # Second extraction: Get the content within the inner parentheses
        inner_pattern = r'\((.*)\)'
        inner_match = re.search(inner_pattern, result, re.DOTALL)
        if inner_match:
            return inner_match.group(1)
        else:
            return result
    else:
        return None

def generate_partitioning_clause(partitioning):
    """
    Generates a partitioning clause by ensuring the presence of 'FEATURE_ID' partitioning.

    Parameters:
        partitioning (str or list): The input partitioning string or list of partitioning clauses.

    Returns:
        str: A partitioning clause string with 'FEATURE_ID' partitioning included.
    """

    # Check if the input is a string
    if isinstance(partitioning, str):
        # Check if the string contains 'partition by'
        if 'partition by' in partitioning.lower():
            # Check if 'feature_id' is already in the partitioning clause
            if 'feature_id' in partitioning.lower():
                return partitioning
            else:
                # Extract existing partition content and add 'FEATURE_ID' partitioning
                substr = extract_partition_content(partitioning.upper())
                if len(substr) > 0:
                    return f"""PARTITION BY (
    RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH}),
    {substr}
)"""
                else:
                    return f"""PARTITION BY (
    RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH})
)"""
        else:
            partitioning = f"""PARTITION BY (
{partitioning}
)"""
            return generate_partitioning_clause(partitioning)
    # Check if the input is a list
    elif isinstance(partitioning, list):
        # Check if 'feature_id' is not in any of the partitioning clauses
        if 'feature_id' not in ','.join(partitioning).lower():
            partitioning = [f'RANGE_N(FEATURE_ID BETWEEN 0 AND {tdfs4ds.FEATURE_PARTITION_N} EACH {tdfs4ds.FEATURE_PARTITION_EACH})'] + partitioning
            partitioning = ',\n'.join(partitioning)
        return f"""PARTITION BY (
{partitioning}
)"""
