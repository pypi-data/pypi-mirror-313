import teradataml as tdml
import tdfs4ds
from teradataml.context.context import _get_database_username
from tdfs4ds.utils.visualization import display_table
from tdfs4ds.utils.query_management import execute_query
from tdfs4ds.utils.info import seconds_to_dhms
import time
import re
import pandas as pd

def generate_on_clause(entity_id, entity_null_substitute, left_name, right_name):
    res = []
    for k in entity_id.keys():
        if 'varchar' in entity_id[k] and k in entity_null_substitute.keys():
            res.append(
                f"COALESCE({left_name}.{k},'{entity_null_substitute[k]}') = COALESCE({right_name}.{k},'{entity_null_substitute[k]}')")
        elif k in entity_null_substitute.keys():
            res.append(
                f"COALESCE({left_name}.{k},{entity_null_substitute[k]}) = COALESCE({right_name}.{k},{entity_null_substitute[k]})")
        else:
            res.append(f"{left_name}.{k} = {right_name}.{k}")

    return '\nAND '.join(res)


def generate_collect_stats(entity_id, primary_index='', partitioning=''):
    """
    Generate a COLLECT STATISTICS SQL query based on specified entity identifiers, primary index,
    and partitioning information. The query collects statistics for columns relevant to the data
    structure, including partitioning and entity identifiers, for optimized query performance.

    Parameters:
    entity_id (list or dict): A list of entity IDs or a dictionary where keys represent entity IDs.
                              Used to identify the columns requiring statistical collection.
    primary_index (str or list, optional): The primary index column(s) for the table, provided as
                                           a single string or list of strings. Defaults to an empty string.
    partitioning (str, optional): A string defining partitioning information, used to identify
                                  additional columns for statistical collection. Defaults to an empty string.

    Returns:
    tuple: A tuple containing two strings:
           - The base COLLECT STATISTICS SQL query.
           - The extended COLLECT STATISTICS SQL query with sampling and thresholds applied.
    """

    # Convert entity_id dictionary keys to a list if it's provided as a dictionary
    if isinstance(entity_id, dict):
        entity_id_list = list(entity_id.keys())
    else:
        entity_id_list = entity_id

    # Sort entity ID list and primary_index once to ensure consistent order
    entity_id_list.sort()
    if isinstance(primary_index, str):
        primary_index = [primary_index]
    primary_index.sort()

    # Identify partitioning columns that match any entity IDs using case-insensitive search
    partitioning_names = [k for k in entity_id_list if
                          re.search(r'\b' + re.escape(k.upper()) + r'\b', partitioning.upper())]

    # Include 'FEATURE_ID' as a default partitioning column for statistics collection
    partitioning_names = list(set(partitioning_names + ['FEATURE_ID']))

    # Initialize the base query with statistics collection on the PARTITION column
    query = ['COLLECT STATISTICS COLUMN(PARTITION)']

    # Append additional partitioning columns, if any, to the base query
    query += ['COLUMN(' + c + ')' for c in partitioning_names]

    # Add fixed columns that are always included in the statistics collection
    query.extend(['COLUMN(FEATURE_VERSION)', 'COLUMN(ValidStart)', 'COLUMN(ValidEnd)'])

    # Initialize the extended query with sampling and threshold settings for statistics collection
    query_extension_header = 'COLLECT STATISTICS USING SAMPLE 25 PERCENT AND THRESHOLD 15 PERCENT'
    query_extension = []

    # Add primary index columns to the extended query
    if primary_index:
        query_extension.append(f"COLUMN({','.join(primary_index)})")

    # Include entity ID columns in the extended query if they differ from the primary index columns
    if entity_id_list != primary_index:
        query_extension.append(f"COLUMN({','.join(entity_id_list)})")

    # Join the base and extended query parts with a newline separator and return as a tuple
    if len(query_extension) > 0:
        return '\n,'.join(query), query_extension_header + '\n' + '\n,'.join(query_extension)
    else:
        return '\n,'.join(query), None

def prepare_feature_ingestion(df, entity_id, feature_names, feature_versions=None, primary_index=None, entity_null_substitute={}, **kwargs):
    """
    Transforms and prepares a DataFrame for feature ingestion into a feature store by unpivoting it.

    This function accepts a DataFrame along with the specifications for entity IDs, feature names, and optionally,
    feature versions. It generates a new DataFrame with the data unpivoted to align with the requirements of a feature
    store ingestion process. Additionally, it creates a volatile table in the database to facilitate the transformation.

    Parameters:
    - df (tdml.DataFrame): The input DataFrame containing the feature data.
    - entity_id (list/dict/other): Specifies the entity IDs. If a dictionary, the keys are used as entity IDs.
                                   If a list or another type, it is used directly as the entity ID.
    - feature_names (list): Names of features to be unpivoted.
    - feature_versions (dict, optional): Maps feature names to their versions. If not provided, a default version is applied.
    - primary_index (list/str, optional): Primary index(es) for the volatile table. If not specified, entity IDs are used.
    - **kwargs: Additional keyword arguments for customization.

    Returns:
    tuple: A tuple containing:
           1. A tdml.DataFrame with the transformed data ready for ingestion.
           2. The name of the volatile table created in the database.

    Raises:
    Exception: If the function encounters an issue during the database operations or data transformations.

    Note:
    - The function handles different data types for 'entity_id' to ensure correct SQL query formation.
    - It assumes a specific structure for 'df' to properly execute SQL commands for data transformation.

    Example:
    >>> df = tdml.DataFrame(...)
    >>> entity_id = {'customer_id': 'INTEGER'}
    >>> feature_names = ['feature1', 'feature2']
    >>> transformed_df, volatile_table_name = prepare_feature_ingestion(df, entity_id, feature_names)
    """

    # Record the start time
    start_time = time.time()



    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]
    list_entity_id.sort()
    ENTITY_ID__ = ','.join([k for k in list_entity_id])
    FEATURE_NAMES__ = ','.join(["'"+k+"'" for k in feature_names])
    feature_id_names = tdml.execute_sql(f"""
    SELECT FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}
    WHERE DATA_DOMAIN = '{tdfs4ds.DATA_DOMAIN}'
    AND ENTITY_NAME = '{ENTITY_ID__}'
    AND FEATURE_NAME IN ({FEATURE_NAMES__})
    """).fetchall()


    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('feature_id_names : ', feature_id_names)

    conversion_name2id = {x[1] : x[0] for x in feature_id_names}

    features_infos = pd.DataFrame(feature_id_names, columns = ['FEATURE_ID','FEATURE_NAME','FEATURE_TABLE','FEATURE_DATABASE'])
    features_infos['FEATURE_VERSION'] = [feature_versions[k] for k in features_infos.FEATURE_NAME.values]
    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('conversion_name2id : ', conversion_name2id)
        print('feature_names : ', feature_names)

    # Create the UNPIVOT clause for the specified feature columns
    unpivot_columns = ", \n".join(["(" + x + ") as '" + str(conversion_name2id[x]) + "'" for x in feature_names])

    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('unpivot_columns : ', unpivot_columns)
    # Create the output column list including entity IDs, feature names, and feature values

    output_columns = ', \n'.join(list_entity_id + ['CAST(FEATURE_ID AS BIGINT) AS FEATURE_ID', 'FEATURE_VALUE'])
    if primary_index is None:
        primary_index = ','.join(list_entity_id)
    else:
        if type(primary_index) == list:
            primary_index = primary_index
        else:
            primary_index = [primary_index]
        primary_index = ','.join(primary_index)

    # Create a dictionary to store feature versions, using the default version if not specified
    versions = {f: tdfs4ds.FEATURE_VERSION_DEFAULT for f in feature_names}
    if feature_versions is not None:
        for k, v in feature_versions.items():
            versions[k] = v

    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('versions : ', versions)

    # Create the CASE statement to assign feature versions based on feature names
    version_query = ["CASE"] + [f"WHEN FEATURE_ID = '{conversion_name2id[k]}' THEN '{v}' " for k, v in versions.items()] + [
        "END AS FEATURE_VERSION"]
    version_query = '\n'.join(version_query)

    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('version_query : ', version_query)

    # Create a volatile table name based on the original table's name, ensuring it is unique.
    volatile_table_name = df._table_name.split('.')[1].replace('"', '')
    volatile_table_name = f'temp_{volatile_table_name}'

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]


    # get the character set of varchars
    res = {x.split()[0]:''.join(x.split()[1::]) for x in str(df[feature_names].tdtypes).split('\n')}
    var_temp2 = []
    for k,v in res.items():
        if 'UNICODE' in v:
            #var_temp2.append(f'TRANSLATE({k} USING UNICODE_TO_LATIN) AS {k}')
            var_temp2.append(f'{k}')
        elif 'LATIN' in v:
            #var_temp2.append(f'{k}')
            var_temp2.append(f'TRANSLATE({k} USING LATIN_TO_UNICODE) AS {k}')
        else:
            var_temp2.append(f'CAST({k} AS VARCHAR(2048) CHARACTER SET UNICODE) AS {k}')
    var_temp2 = ', \n'.join(var_temp2)
    # query casting in varchar everything
    var_temp = "'%UNICODE%'"
    #var_temp2 = ', \n'.join([f'CAST({x} AS VARCHAR(2048)) AS {x}' for x in feature_names])
    var_temp3 = []
    for e in list_entity_id:
        if e in entity_null_substitute.keys():
            if type(entity_null_substitute[e]) == str:
                var_temp3.append(f"coalesce({e},'{entity_null_substitute[e]}') AS {e}")
            else:
                var_temp3.append(f"coalesce({e},{entity_null_substitute[e]}) AS {e}")
        else:
            var_temp3.append(e)

    var_temp3 = ', \n'.join(var_temp3)


    nested_query = f"""
    CREATE MULTISET VOLATILE TABLE {volatile_table_name} AS
    (
    SELECT 
    {output_columns},
    {version_query}
    FROM
        (SELECT 
        {var_temp3},
        {var_temp2}
        FROM {df._table_name}
        ) A
    UNPIVOT INCLUDE NULLS ((FEATURE_VALUE )  FOR  FEATURE_ID 
    IN ({unpivot_columns})) Tmp
    ) WITH DATA
    PRIMARY INDEX ({primary_index})
    PARTITION BY RANGE_N(FEATURE_ID  BETWEEN 0  AND 2000  EACH 1 )
    ON COMMIT PRESERVE ROWS
    """

    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('var_temp2 : ', var_temp2)
        print('var_temp3 : ', var_temp3)
        print('nested_query :', nested_query)



    # Execute the SQL query to create the volatile table.
    try:
        tdml.execute_sql(nested_query)
    except Exception as e:
        if tdfs4ds.DISPLAY_LOGS:
            print(str(e).split('\n')[0])
        tdml.execute_sql(f'DROP TABLE {volatile_table_name}')
        tdml.execute_sql(nested_query)


    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print(tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name)).tdtypes)


    # Record the end time
    end_time = time.time()


    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time
    formatted_elapsed_time = seconds_to_dhms(elapsed_time)
    if tdfs4ds.DISPLAY_LOGS:
        print(f'Feature preparation for ingestion : {formatted_elapsed_time} ({elapsed_time}s)')
    try:
        df_out = tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name))
        return df_out, volatile_table_name, features_infos
    except Exception as e:
        print(str(e).split()[0])
        print(df[feature_names].tdtypes)
        if 'TD_Unpivot contract function' in str(e).split()[0]:
            raise('Error : you may have string with UNICODE encoding as feature, please convert them to latin first')

    return None, None, None


def _store_feature_update_insert(entity_id, volatile_table_name, entity_null_substitute={},primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Stores prepared feature data in specific feature tables within a Teradata database. This function performs updates and inserts
    on the feature tables based on the provided entity IDs and prepared feature data.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments that can include:
        - schema (str): The schema name where the feature tables are located.
        - feature_catalog_name (str, optional): The name of the feature catalog table, defaulting to 'FS_FEATURE_CATALOG'.

    Returns:
    None: This function does not return any value but performs database operations.

    Note:
    - The function uses the Teradata temporal feature (VALIDTIME) for handling the valid time of the records.
    - It constructs SQL queries to update existing feature values and insert new ones based on the entity ID.
    - The function handles the entity ID, feature IDs, and versions for inserting and updating records.
    - It utilizes additional settings from the tdfs4ds module for configuring the feature store time and display logs.
    - This function assumes that the necessary database tables and schema are correctly set up and accessible.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    #feature_catalog = tdml.DataFrame(tdml.in_schema(tdfs4ds.SCHEMA, tdfs4ds.FEATURE_CATALOG_NAME))

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_statement2 = validtime_statement
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"
        validtime_statement2 = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"


    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()
    ENTITY_ID = ','.join([k for k in sorted_entity_id])


    # Group the target tables by feature table and feature database and count the number of occurrences
    target_tables = features_infos[['FEATURE_TABLE', 'FEATURE_DATABASE', 'FEATURE_ID']].groupby(
        ['FEATURE_TABLE', 'FEATURE_DATABASE']).count()
    if tdfs4ds.DISPLAY_LOGS:
        display_table(target_tables[['FEATURE_DATABASE', 'FEATURE_TABLE', 'FEATURE_ID']])


    ENTITY_ID = ', \n'.join([k for k in sorted_entity_id])
    #ENTITY_ID_ON = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k in sorted_entity_id])
    ENTITY_ID_ON = generate_on_clause(entity_id, entity_null_substitute, left_name='NEW_FEATURES', right_name='EXISTING_FEATURES')
    ENTITY_ID_WHERE_INS = ' OR '.join([f'EXISTING_FEATURES.{k} IS NOT NULL' for k in sorted_entity_id])
    ENTITY_ID_WHERE_UP = ' OR '.join([f'EXISTING_FEATURES.{k} IS NULL' for k in sorted_entity_id])

    ENTITY_ID_SELECT = ', \n'.join(['NEW_FEATURES.' + k for k in sorted_entity_id])
    # Iterate over target tables and perform update and insert operations

    query_collect_stats, query_collect_stats_extension = generate_collect_stats(sorted_entity_id, primary_index=primary_index,
                                                 partitioning=partitioning)

    feature_id_list = ','.join([str(x) for x in list(set(features_infos.FEATURE_ID.values))])
    for i, row in target_tables.iterrows():

        ENTITY_ID_WHERE_ = ' AND '.join([f'{row.iloc[0]}.{k}   = UPDATED_FEATURES.{k}' for k in sorted_entity_id])
        # SQL query to update existing feature values
        query_update = f"""
        {validtime_statement} 
        UPDATE {row.iloc[1]}.{row.iloc[0]}
        FROM (
            {validtime_statement2} 
            SELECT
                {ENTITY_ID_SELECT},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION
            FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
            LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            WHERE 
            --({ENTITY_ID_WHERE_INS})
            --AND
             EXISTING_FEATURES.FEATURE_VERSION IS NOT NULL
             AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
            AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
        ) UPDATED_FEATURES
        SET
            FEATURE_VALUE = UPDATED_FEATURES.FEATURE_VALUE
        WHERE     {ENTITY_ID_WHERE_}
        AND {row.iloc[0]}.FEATURE_ID          = UPDATED_FEATURES.FEATURE_ID
            AND {row.iloc[0]}.FEATURE_VERSION = UPDATED_FEATURES.FEATURE_VERSION;
        """

        # SQL query to insert new feature values
        if validtime_statement == 'CURRENT VALIDTIME':
            query_insert = f"""
            {validtime_statement} 
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION
                FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON 
                -- {ENTITY_ID_ON}
                --AND 
                EXISTING_FEATURES.FEATURE_VERSION IS NULL
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE ({ENTITY_ID_WHERE_UP})
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """
        elif tdfs4ds.FEATURE_STORE_TIME is not None:
            if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
                end_period_ = '9999-01-01 00:00:00'
            else:
                end_period_ = tdfs4ds.END_PERIOD
            query_insert = f"""
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION, ValidStart, ValidEnd)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION,
                    TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                    TIMESTAMP '{end_period_}'
                FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON {ENTITY_ID_ON}
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE 
                --({ENTITY_ID_WHERE_UP})
                EXISTING_FEATURES.FEATURE_VERSION IS NULL
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """

        entity_id_str = ', \n'.join([k for k in sorted_entity_id])

        if tdfs4ds.DISPLAY_LOGS: print(
            f'insert feature values of new {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_insert)
        execute_query(query_insert)
        if tdfs4ds.DISPLAY_LOGS: print(
            f'update feature values of existing {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_update)
        execute_query(query_update)
        execute_query(query_collect_stats + f' ON {row.iloc[1]}.{row.iloc[0]}')
        print(query_collect_stats + f' ON {row.iloc[1]}.{row.iloc[0]}')
        if query_collect_stats_extension is not None:
            execute_query(query_collect_stats_extension + f' ON {row.iloc[1]}.{row.iloc[0]}')
            print(query_collect_stats_extension + f' ON {row.iloc[1]}.{row.iloc[0]}')

    return

def _store_feature_merge(entity_id, volatile_table_name, entity_null_substitute= {}, primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Stores prepared feature data in specific feature tables within a Teradata database. This function performs updates and inserts
    on the feature tables based on the provided entity IDs and prepared feature data.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments that can include:
        - schema (str): The schema name where the feature tables are located.
        - feature_catalog_name (str, optional): The name of the feature catalog table, defaulting to 'FS_FEATURE_CATALOG'.

    Returns:
    None: This function does not return any value but performs database operations.

    Note:
    - The function uses the Teradata temporal feature (VALIDTIME) for handling the valid time of the records.
    - It constructs SQL queries to update existing feature values and insert new ones based on the entity ID.
    - The function handles the entity ID, feature IDs, and versions for inserting and updating records.
    - It utilizes additional settings from the tdfs4ds module for configuring the feature store time and display logs.
    - This function assumes that the necessary database tables and schema are correctly set up and accessible.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    #feature_catalog = tdml.DataFrame(tdml.in_schema(tdfs4ds.SCHEMA, tdfs4ds.FEATURE_CATALOG_NAME))

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_statement2 = validtime_statement
        validtime_start = 'CAST(CURRENT_TIME AS TIMESTAMP(0) WITH TIME ZONE)'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"
        validtime_statement2 = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"
        validtime_start = f"CAST('{tdfs4ds.FEATURE_STORE_TIME}' AS TIMESTAMP(0) WITH TIME ZONE)"

    if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
        end_period_ = '9999-01-01 00:00:00'
    else:
        end_period_ = tdfs4ds.END_PERIOD

    if tdfs4ds.DEBUG_MODE:
        print('tdfs4ds.FEATURE_STORE_TIME :' , tdfs4ds.FEATURE_STORE_TIME)


    if tdfs4ds.DEBUG_MODE:
        print('entity_id :' , entity_id)

    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()
    ENTITY_ID = ','.join([k for k in sorted_entity_id])

    count_features = pd.DataFrame(tdml.execute_sql(f"""
    SEL FEATURE_ID, count(*) as NB_ROWS FROM
    {_get_database_username()}.
    {volatile_table_name}
    GROUP BY 1
    """).fetchall(), columns = ['FEATURE_ID','NB_ROWS'])

    if tdfs4ds.DEBUG_MODE:
        print('count_features :' , count_features)
        print('features_infos :', features_infos)


    features_infos = features_infos.set_index('FEATURE_ID').join(count_features.set_index('FEATURE_ID'))
    features_infos = features_infos.reset_index()

    if tdfs4ds.DEBUG_MODE:
        print('features_infos :' , features_infos)
    # Group the target tables by feature table and feature database and count the number of occurrences
    target_tables = features_infos[['FEATURE_TABLE', 'FEATURE_DATABASE', 'NB_ROWS']].groupby(
        ['FEATURE_TABLE', 'FEATURE_DATABASE']).sum().reset_index()

    if tdfs4ds.DEBUG_MODE:
        print('target_tables :' , target_tables)
    if tdfs4ds.DISPLAY_LOGS:
        display_table(target_tables[['FEATURE_DATABASE', 'FEATURE_TABLE', 'NB_ROWS']])



    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()




    ENTITY_ID_ON = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k in sorted_entity_id])

    ENTITY_ID_SELECT = ', \n'.join(['NEW_FEATURES.' + k for k in sorted_entity_id])
    # Iterate over target tables and perform update and insert operations


    query_collect_stats, query_collect_stats_extension = generate_collect_stats(sorted_entity_id,primary_index=primary_index, partitioning=partitioning)

    for i, row in target_tables.iterrows():
        if tdfs4ds.DEBUG_MODE:
            print('row.iloc[1] :', row.iloc[1])
            print('row.iloc[0] :', row.iloc[0])
            print('features_infos.FEATURE_TABLE : ', features_infos.FEATURE_TABLE)
            print('features_infos.FEATURE_DATABASE : ',
            features_infos.FEATURE_DATABASE)
        features_infos_ = features_infos[(features_infos.FEATURE_TABLE == row.iloc[0]) & (features_infos.FEATURE_DATABASE == row.iloc[1])]
        feature_id_list = ','.join([str(x) for x in list(set(features_infos_.FEATURE_ID.values))])
        feature_version_list = ','.join(["'"+x+"'" for x in list(set(features_infos_.FEATURE_VERSION.values))])
        if tdfs4ds.FEATURE_STORE_TIME == None:
            query_merge = f"""
            {validtime_statement}
            MERGE INTO  {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
            
            USING (SEL * FROM {_get_database_username()}.{volatile_table_name} WHERE FEATURE_ID IN ({feature_id_list}) ) NEW_FEATURES
            ON {ENTITY_ID_ON} 
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            AND NEW_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND EXISTING_FEATURES.FEATURE_VERSION IN ({feature_version_list})
            WHEN MATCHED THEN
                UPDATE
                SET
                FEATURE_VALUE = NEW_FEATURES.FEATURE_VALUE
            WHEN NOT MATCHED THEN
                INSERT
                ({ENTITY_ID_SELECT},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION)
                --,
                --{validtime_start},
                --'{end_period_}')
            """
        else:
            query_merge = f"""
            {validtime_statement}
            MERGE INTO  {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
            USING (SEL * FROM {_get_database_username()}.{volatile_table_name} WHERE FEATURE_ID IN ({feature_id_list}) ) NEW_FEATURES
            ON {ENTITY_ID_ON} 
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION      
            AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})  
            AND NEW_FEATURES.FEATURE_ID IN ({feature_id_list})  
            AND EXISTING_FEATURES.FEATURE_VERSION IN ({feature_version_list})
            WHEN MATCHED THEN
                UPDATE
                SET
                FEATURE_VALUE = NEW_FEATURES.FEATURE_VALUE
            WHEN NOT MATCHED THEN
                INSERT
                ({ENTITY_ID_SELECT},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION,
                {validtime_start},
                '{end_period_}')
            """

        entity_id_str = ', \n'.join([k for k in sorted_entity_id])
        if tdfs4ds.DEBUG_MODE: print(
            f'merge feature values of new {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdfs4ds.DEBUG_MODE:
            print(query_merge)

        try:
            execute_query(query_merge)
        except Exception as e:
            print(str(e))
            raise

        if query_collect_stats_extension is not None:
            execute_query(query_collect_stats_extension + f' ON {row.iloc[1]}.{row.iloc[0]}')


    return
def store_feature(entity_id, volatile_table_name, entity_null_substitute = {},primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Conditionally stores prepared feature data in specific feature tables within a Teradata database. This function decides
    whether to perform updates and inserts on the feature tables based on a global configuration.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments for further customization and configurations.

    Returns:
    None: This function does not return any value but performs database operations based on the specified condition.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    # Record the start time
    start_time = time.time()

    if tdfs4ds.STORE_FEATURE == 'UPDATE_INSERT':
        _store_feature_update_insert(entity_id, volatile_table_name, entity_null_substitute=entity_null_substitute,primary_index=primary_index,
            partitioning=partitioning, features_infos=features_infos, **kwargs)
    elif tdfs4ds.STORE_FEATURE == 'MERGE':
        _store_feature_merge(entity_id, volatile_table_name, entity_null_substitute=entity_null_substitute,primary_index=primary_index,
            partitioning=partitioning, features_infos=features_infos, **kwargs)
    else:
        # Handle other conditions or operations as required
        pass

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time
    formatted_elapsed_time = seconds_to_dhms(elapsed_time)
    if tdfs4ds.DISPLAY_LOGS:
        print(f'Storage of the prepared features : {formatted_elapsed_time} ({elapsed_time}s)')

def prepare_feature_ingestion_tdstone2(df, entity_id):
    """
    Prepares a DataFrame for feature ingestion into a tdstone2 feature store by transforming the data structure.
    This function unpivots the DataFrame and adds necessary columns for entity IDs, feature names, feature values,
    and a predefined feature version. It creates a volatile table in the database to facilitate this transformation.

    Parameters:
    - df (tdml.DataFrame): The input DataFrame containing the feature data. The DataFrame should be structured
      in a way that is compatible with tdstone2 feature store requirements.
    - entity_id (list/dict/other): A representation of the entity ID. If a dictionary, the keys are used as entity IDs.
                                   If a list or another data type, it is used directly as the entity ID.

    Returns:
    - tdml.DataFrame: A transformed DataFrame suitable for feature store ingestion.
    - str: The name of the volatile table created in the database for storing the transformed data.

    Note:
    - The function requires that the input DataFrame 'df' has a valid table name and is compatible with tdml operations.
    - It automatically handles the creation and management of a volatile table in the database.
    - 'ID_PROCESS' is used as the default feature version identifier.
    - The transformed DataFrame includes columns for each entity ID, 'FEATURE_NAME', 'FEATURE_VALUE', and 'FEATURE_VERSION'.

    Example Usage:
    >>> input_df = tdml.DataFrame(...)
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> transformed_df, table_name = prepare_feature_ingestion_tdstone2(input_df, entity_id_dict)
    """

    # Ensure the internal table name of the DataFrame is set, necessary for further processing.
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Combine entity ID columns with feature name and value columns to form the output column list.
    output_columns = ', \n'.join(list_entity_id + ['FEATURE_NAME', 'FEATURE_VALUE'])
    primary_index = ','.join(list_entity_id)

    # Define a query segment to assign feature versions.
    version_query = "ID_PROCESS AS FEATURE_VERSION"

    # Create a volatile table name based on the original table's name, ensuring it is unique.
    if tdfs4ds.USE_VOLATILE_TABLE:
        volatile_table_name = df._table_name.split('.')[1].replace('"', '')
        volatile_table_name = f'temp_{volatile_table_name}'
        volatile_verb = 'VOLATILE'
        volatile_expression = 'ON COMMIT PRESERVE ROWS'
    else:
        volatile_table_name = df._table_name.split('.')[1].replace('"', '')
        volatile_table_name = f'"{tdfs4ds.SCHEMA}"."temp_{volatile_table_name}"'
        volatile_verb = ''
        volatile_expression = ''

    # Construct the SQL query to create the volatile table with the transformed data.
    query = f"""
    CREATE {volatile_verb} TABLE {volatile_table_name} AS
    (
    SELECT 
    {output_columns},
    {version_query}
    FROM {df._table_name}
    ) WITH DATA
    PRIMARY INDEX ({primary_index})
    {volatile_expression}
    """
    # Execute the SQL query to create the volatile table.
    try:
        tdml.execute_sql(query)
    except Exception as e:
        if tdfs4ds.DISPLAY_LOGS:
            print(str(e).split('\n')[0])
        tdml.execute_sql(f'DELETE {volatile_table_name}')

    # Optionally print the query if the display flag is set.
    if tdml.display.print_sqlmr_query:
        print(query)

    # Return the DataFrame representation of the volatile table and its name.
    if tdfs4ds.USE_VOLATILE_TABLE:
        return tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name)), volatile_table_name
    else:
        return tdml.DataFrame(volatile_table_name), volatile_table_name


