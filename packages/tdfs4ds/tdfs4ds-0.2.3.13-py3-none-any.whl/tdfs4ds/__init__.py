__version__ = '0.2.3.13'
import logging
# Setup the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format to include timestamp
    datefmt='%Y-%m-%d %H:%M:%S'  # Set the date/time format
)

logger = logging.getLogger(__name__)

from tdfs4ds.feature_store.feature_query_retrieval import get_available_entity_id_records, write_where_clause_filter
from tdfs4ds.process_store.process_followup import follow_up_report

DATA_DOMAIN             = None
SCHEMA                  = None
FEATURE_CATALOG_NAME         = 'FS_FEATURE_CATALOG'
FEATURE_CATALOG_NAME_VIEW    = 'FS_V_FEATURE_CATALOG'
PROCESS_CATALOG_NAME         = 'FS_PROCESS_CATALOG'
PROCESS_CATALOG_NAME_VIEW    = 'FS_V_PROCESS_CATALOG'
PROCESS_CATALOG_NAME_VIEW_FEATURE_SPLIT    = 'FS_V_PROCESS_CATALOG_FEATURE_SPLIT'

DATA_DISTRIBUTION_NAME  = 'FS_DATA_DISTRIBUTION'
FOLLOW_UP_NAME          = 'FS_FOLLOW_UP'
DATA_DISTRIBUTION_TEMPORAL = False
FILTER_MANAGER_NAME     = 'FS_FILTER_MANAGER'

END_PERIOD              = 'UNTIL_CHANGED' #'9999-01-01 00:00:00'
FEATURE_STORE_TIME      = None #'9999-01-01 00:00:00'
FEATURE_VERSION_DEFAULT = 'dev.0.0'
DISPLAY_LOGS            = True
DEBUG_MODE              = False

USE_VOLATILE_TABLE      = True
STORE_FEATURE           = 'MERGE' #'UPDATE_INSERT'
REGISTER_FEATURE        = 'MERGE' #'UPDATE_INSERT'
REGISTER_PROCESS        = 'MERGE' #'UPDATE_INSERT'
BUILD_DATASET_AT_UPLOAD = False

FEATURE_PARTITION_N     = 20000
FEATURE_PARTITION_EACH  = 1

VARCHAR_SIZE            = 1024

import warnings
warnings.filterwarnings('ignore')

import teradataml as tdml
from tdfs4ds.utils.lineage import crystallize_view
from tdfs4ds.utils.filter_management import FilterManager
from tdfs4ds.utils.info import seconds_to_dhms
import tdfs4ds.feature_store
import tdfs4ds.process_store
import tdfs4ds.datasets
import time

import inspect
import tqdm

from tdfs4ds.feature_store.feature_data_processing import generate_on_clause

import uuid

# Generate a UUID
RUN_ID       = str(uuid.uuid4())
PROCESS_TYPE = 'RUN PROCESS'

try:
    SCHEMA = tdml.context.context._get_current_databasename()
    if SCHEMA is None:
        print('Please specify the database which is hosting the feature store.')
        print('tdfs4ds.feature_store.schema = "<feature store database>"')
    else:
        print('The default database is used for the feature store.')
        print(f"tdfs4ds.feature_store.schema = '{SCHEMA}'")
        if DATA_DOMAIN is None:
            DATA_DOMAIN = SCHEMA
            print(f"the data domain for the current work is :{DATA_DOMAIN}")
            print("Please update it as you wish with tdfs4ds.DATA_DOMAIN=<your data domain>")

except Exception as e:
    print('Please specify the database which is hosting the feature store.')
    print('tdfs4ds.feature_store.schema = "<feature store database>"')


def setup(database, if_exists='fail'):
    """
    Set up the database environment by configuring schema names and optionally dropping existing tables.

    This function sets the database schema for feature and process catalogs. If specified, it also handles
    the replacement of existing catalog tables. It reports the status of these operations, including any
    encountered exceptions.

    Parameters:
    database (str): The name of the database schema to be used.
    if_exists (str, optional): Determines the behavior if catalog tables already exist in the database.
                               'fail' (default) - Do nothing if the tables exist.
                               'replace' - Drop the tables if they exist before creating new ones.

    Steps performed:
    1. Sets the schema to the provided database name.
    2. If 'if_exists' is 'replace', attempts to drop 'FS_FEATURE_CATALOG' and 'FS_PROCESS_CATALOG' tables.
    3. Creates new feature and process catalog tables and sets their names in the tdfs4ds module.
    4. Prints the names of the newly created tables along with the database name.
    5. Captures and prints the first line of any exceptions that occur during these operations.

    Returns:
    None
    """

    from tdfs4ds.feature_store.feature_store_management import feature_store_catalog_creation
    from tdfs4ds.process_store.process_store_catalog_management import process_store_catalog_creation

    tdfs4ds.SCHEMA = database
    if if_exists == 'replace':
        try:
            tdml.db_drop_table(table_name = tdfs4ds.FEATURE_CATALOG_NAME, schema_name=database)
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(table_name = tdfs4ds.PROCESS_CATALOG_NAME, schema_name=database)
        except Exception as e:
            print(str(e).split('\n')[0])
        try:
            tdml.db_drop_table(table_name = tdfs4ds.DATA_DISTRIBUTION_NAME, schema_name=database)
        except Exception as e:
            print(str(e).split('\n')[0])
    try:
        tdfs4ds.FEATURE_CATALOG_NAME = feature_store_catalog_creation()
        print('feature catalog table: ', tdfs4ds.FEATURE_CATALOG_NAME, ' in database ', database)
    except Exception as e:
        print(str(e).split('\n')[0])

    try:
        tdfs4ds.PROCESS_CATALOG_NAME, tdfs4ds.DATA_DISTRIBUTION_NAME, tdfs4ds.FILTER_MANAGER_NAME = process_store_catalog_creation()
        print('process catalog table: ', tdfs4ds.PROCESS_CATALOG_NAME, ' in database ', database)
        print('data distribution table: ', tdfs4ds.DATA_DISTRIBUTION_NAME, ' in database ', database)
        print('filter manager table: ', tdfs4ds.FILTER_MANAGER_NAME, ' in database ', database)
    except Exception as e:
        print(str(e).split('\n')[0])

    try:
        tdfs4ds.process_store.process_followup.follow_up_table_creation()
    except Exception as e:
        print(str(e).split('\n')[0])

    tdfs4ds.feature_store.feature_store_management.feature_store_catalog_view_creation()
    tdfs4ds.process_store.process_store_catalog_management.process_store_catalog_view_creation()

    return

def connect(
    database               = tdfs4ds.SCHEMA,
    feature_catalog_name   = tdfs4ds.FEATURE_CATALOG_NAME,
    process_catalog_name   = tdfs4ds.PROCESS_CATALOG_NAME,
    data_distribution_name = tdfs4ds.DATA_DISTRIBUTION_NAME,
    filter_manager_name    = tdfs4ds.FILTER_MANAGER_NAME,
    followup_name          = tdfs4ds.FOLLOW_UP_NAME,
    feature_catalog_name_view = tdfs4ds.FEATURE_CATALOG_NAME_VIEW,
    process_catalog_name_view = tdfs4ds.PROCESS_CATALOG_NAME_VIEW
):
    """
    Configures the database environment by setting schema names and checking the existence of specified catalog tables.

    This function initializes the database schema and verifies the presence of the feature catalog, process catalog,
    data distribution tables, and the filter manager. It updates the module-level configuration for these names if they exist.
    If any of the specified tables or manager do not exist, it raises an assertion error.

    Parameters:
    - database (str): The name of the database schema to use. Defaults to tdfs4ds.SCHEMA.
    - feature_catalog_name (str, optional): The name of the feature catalog table. Defaults to tdfs4ds.FEATURE_CATALOG_NAME.
    - process_catalog_name (str, optional): The name of the process catalog table. Defaults to tdfs4ds.PROCESS_CATALOG_NAME.
    - data_distribution_name (str, optional): The name of the data distribution table. Defaults to tdfs4ds.DATA_DISTRIBUTION_NAME.
    - filter_manager_name (str, optional): The name of the filter manager. Defaults to tdfs4ds.FILTER_MANAGER_NAME.

    Steps Performed:
    1. Set the database schema to the provided 'database' name.
    2. Retrieve the list of tables in the specified schema and check for the existence of the feature catalog, process catalog,
       data distribution tables, and filter manager.
    3. Update the module-level names for these tables and manager if they exist.
    4. Raise an assertion error if any of the specified tables or manager do not exist, specifying which are missing.

    Returns:
    None

    Raises:
    AssertionError: An error indicating which of the feature catalog, process catalog, data distribution table, or filter manager do not exist.
    """
    if database is not None:
        tdfs4ds.SCHEMA = database
    else:
        assert False, "database parameter is None."

    tables = [x.lower() for x in list(tdml.db_list_tables(schema_name=tdfs4ds.SCHEMA, object_type='table').TableName.values)]
    feature_exists = feature_catalog_name.lower() in tables
    process_exists = process_catalog_name.lower() in tables
    distrib_exists = data_distribution_name.lower() in tables
    filter_manager_exists = filter_manager_name.lower() in tables
    followup_name_exists = followup_name.lower() in tables

    if followup_name_exists:
        tdfs4ds.FOLLOW_UP_NAME = followup_name
    else:
        tdfs4ds.process_store.process_followup.follow_up_table_creation()
        tdfs4ds.FOLLOW_UP_NAME = followup_name

    if feature_exists and process_exists and distrib_exists and filter_manager_exists:
        tdfs4ds.FEATURE_CATALOG_NAME = feature_catalog_name
        tdfs4ds.PROCESS_CATALOG_NAME = process_catalog_name
        tdfs4ds.DATA_DISTRIBUTION_NAME = data_distribution_name
        tdfs4ds.FILTER_MANAGER_NAME = filter_manager_name
        tdfs4ds.PROCESS_CATALOG_NAME_VIEW = process_catalog_name_view
        tdfs4ds.FEATURE_CATALOG_NAME_VIEW = feature_catalog_name_view

        process_list = tdml.DataFrame(tdml.in_schema(database, process_catalog_name))
        if 'ENTITY_NULL_SUBSTITUTE' not in process_list.columns:
            print('ENTITY_NULL_SUBSTITUTE column does not exist in the existing process catalog')
            print('upgrade to the latest DDL')
            tdfs4ds.process_store.process_store_catalog_management.upgrade_process_catalog()

        tdfs4ds.feature_store.feature_store_management.feature_store_catalog_view_creation()
        tdfs4ds.process_store.process_store_catalog_management.process_store_catalog_view_creation()
    else:
        missing = []
        if not feature_exists:
            missing.append("feature catalog")
        if not process_exists:
            missing.append("process catalog")
        if not distrib_exists:
            missing.append("data distribution table")
        if not filter_manager_exists:
            missing.append("filter manager")
        assert False, f"""{', '.join(missing)} {'do' if len(missing) > 1 else 'does'} not exist.
        Please run setup to create the missing table ou speficy the correct name in the arguments.
        type help(tdfs4ds.connect) for more information."""

    def is_data_distribution_temporal():
        return 'PERIOD' in tdfs4ds.utils.lineage.get_ddl(view_name=tdfs4ds.DATA_DISTRIBUTION_NAME,
                                                         schema_name=tdfs4ds.SCHEMA, object_type='table')

    if is_data_distribution_temporal():
        tdfs4ds.DATA_DISTRIBUTION_TEMPORAL = True
    else:
        tdfs4ds.DATA_DISTRIBUTION_TEMPORAL = False
    return


def feature_catalog():
    """
    Retrieve a list of all features available in the feature store.

    This function queries the feature store to obtain a comprehensive list of features
    that have been defined and stored. It leverages the feature store's query retrieval
    functionality to compile and return this list. This can be useful for understanding
    what features are available for analysis, machine learning models, or other purposes
    within the data ecosystem.

    Returns:
    - list: A list of features available in the feature store as a teradata dataframe at
            the tdfs4ds.FEATURE_STORE_TIME valid time.
    """
    return tdfs4ds.feature_store.feature_query_retrieval.list_features()


def process_catalog():
    """
    Retrieve a list of all processes registered in the process store.

    This function performs a query against the process store to gather a list of all
    processes that have been registered and are administrable. It utilizes the process
    store's process query administration capabilities to fetch and return this list.
    This is useful for users looking to get an overview of the data processing workflows,
    transformations, and other processes that have been established within the data
    infrastructure.

    Returns:
    - list: A list of processes registered in the process store as a teradata dataframe at
            the tdfs4ds.FEATURE_STORE_TIME valid time.
    """
    return tdfs4ds.process_store.process_query_administration.list_processes()



def run(process_id, return_dataset = False):
    """
    Executes a specific process from the feature store identified by the process ID.
    The function handles different process types and performs appropriate actions.

    Args:
    process_id (str): The unique identifier of the process to run.
    as_date_of (str, optional): Date parameter for the process execution. Defaults to None.

    Returns:
    None: The function returns None, but performs operations based on process type.
    """

    if tdfs4ds.PROCESS_TYPE is None:
        PROCESS_TYPE_ = 'RUN PROCESS'
        tdfs4ds.RUN_ID       = str(uuid.uuid4())
    else:
        PROCESS_TYPE_ = tdfs4ds.PROCESS_TYPE

    if tdfs4ds.DEBUG_MODE:
        print('def run','tdfs4ds.FEATURE_STORE_TIME', tdfs4ds.FEATURE_STORE_TIME)

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    # Construct SQL query to retrieve process details by process ID
    query = f"""
    SELECT *
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} A
    WHERE A.PROCESS_ID = '{process_id}'
    """

    # Executing the query and converting the result to Pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Check if exactly one record is returned, else print an error
    if df.shape[0] != 1:
        print('error - there is ', df.shape[0], f' records. Check table {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW}')
        print('check ou this query:')
        print(query)
        return


    # Fetching the filter manager
    filter_schema_name = df['FILTER_DATABASE_NAME'].values[0]
    if filter_schema_name is None:
        filtermanager = None
    else:
        filter_view_name = df['FILTER_VIEW_NAME'].values[0]
        filter_table_name = df['FILTER_TABLE_NAME'].values[0]
        filtermanager = FilterManager(table_name=filter_view_name, schema_name=filter_schema_name)

    # Fetching the process type from the query result
    process_type = df['PROCESS_TYPE'].values[0]

    # Fetching the primary index from the query result
    primary_index = df['FOR_PRIMARY_INDEX'].values[0]
    if primary_index is not None:
        primary_index = primary_index.split(',')

    # Fetching the primary index from the query result
    partitioning = df['FOR_DATA_PARTITIONING'].values[0]

    # Fetching the data domain from the query result
    DATA_DOMAIN = df['DATA_DOMAIN'].values[0]

    # Handling 'denormalized view' process type
    if process_type == 'denormalized view':
        # Extracting necessary details for this process type
        view_name = df['VIEW_NAME'].values[0]
        entity_id = df['ENTITY_ID'].values[0].split(',')
        entity_null_substitute = eval(df['ENTITY_NULL_SUBSTITUTE'].values[0])
        feature_names = df['FEATURE_NAMES'].values[0].split(',')

        # Fetching data and uploading features to the feature store
        df_data = tdml.DataFrame(tdml.in_schema(view_name.split('.')[0], view_name.split('.')[1]))

        if tdfs4ds.DEBUG_MODE:
            print('run','entity_id',entity_id)
            print('run', 'entity_null_substitute', entity_null_substitute)
            print('run','feature_names',feature_names)
            print('run','process_id',process_id)
            print('run','primary_index',primary_index)
            print('run','partitioning',partitioning)
        dataset = _upload_features(
            df_data,
            entity_id,
            feature_names,
            feature_versions = process_id,
            primary_index = primary_index,
            partitioning = partitioning,
            filtermanager = filtermanager,
            entity_null_substitute = entity_null_substitute,
            process_id = process_id
        )

    # Handling 'tdstone2 view' process type
    elif process_type == 'tdstone2 view':
        print('not implemented yet')



    if return_dataset:
        return dataset
    else:
        return

def upload_features(df, entity_id, feature_names, metadata={}, primary_index = None, partitioning = '', filtermanager = None, entity_null_substitute = {}):
    """
    Uploads feature data from a DataFrame to the feature store for a specified entity. This involves registering the
    process in the feature store, executing the necessary SQL to insert the data, and returning the resulting dataset
    for further use or inspection.

    The function supports dynamic entity ID interpretation and flexible feature name handling, ensuring compatibility
    with various data schemas. It automatically registers the data upload process and applies additional metadata,
    if provided.

    Parameters:
    - df (DataFrame): The DataFrame containing the feature data to be uploaded.
    - entity_id (dict, list, or str): The identifier of the entity to which the features belong. This can be:
        - a dictionary mapping column names to their data types,
        - a list of column names, which will be automatically converted to a dictionary with types inferred from `df`,
        - a string representing a single column name, which will be converted into a list and then to a dictionary as above.
    - feature_names (list or str): The names of the features to be uploaded. If a string is provided, it will be
      split into a list based on commas or treated as a single feature name.
    - metadata (dict, optional): Additional metadata to associate with the upload process. Defaults to an empty dictionary.
    - primary_index (list, optional): Specifies the primary index columns for optimizing data storage and retrieval.
    - partitioning (str, optional): Defines how the data should be partitioned in the store for performance optimization.

    Returns:
    DataFrame: A DataFrame representing the dataset resulting from the upload process, typically used for validation
               or further processing.

    The process involves several steps, including entity ID type conversion if necessary, feature name normalization,
    process registration in the feature store, and the execution of SQL queries to insert the data. The function concludes
    by returning a dataset derived from the uploaded data, offering immediate access to the newly stored information.

    Example:
    >>> df = tdml.DataFrame(...)
    >>> entity_id = ['customer_id']
    >>> feature_names = ['age', 'income']
    >>> dataset = upload_features(df, entity_id, feature_names)
    >>> # Another example with list-based entity_id, custom primary_index, and partitioning
    >>> tddf = tdml.DataFrame(...)  # Assuming tddf is predefined with appropriate columns
    >>> entity_id = ['tx_type', 'txn_id']
    >>> primary_index = ['txn_id']
    >>> partitioning = '''
    ... PARTITION BY CASE_N (
    ...     tx_type LIKE 'DEBIT',
    ...     tx_type LIKE 'PAYMENT',
    ...     tx_type LIKE 'CASH_OUT',
    ...     tx_type LIKE 'CASH_IN',
    ...     tx_type LIKE 'TRANSFER',
    ...     NO CASE,
    ...     UNKNOWN)'''
    >>> features = [x for x in tddf.columns if x not in entity_id]
    >>> dataset = upload_features(
    ...     df = tddf,
    ...     entity_id = entity_id,
    ...     feature_names = features,
    ...     metadata = {'project': 'test'},
    ...     primary_index = primary_index,
    ...     partitioning = partitioning
    ... )
    """

    from tdfs4ds.utils.info import get_column_types
    from tdfs4ds.utils.query_management import execute_query
    from tdfs4ds.process_store.process_registration_management import register_process_view

    # Convert entity_id to a dictionary if it's not already one
    if type(entity_id) == list:
        entity_id.sort()
        entity_id = get_column_types(df, entity_id)
        if tdfs4ds.DISPLAY_LOGS:
            print('entity_id has been converted to a proper dictionary : ', entity_id)
    elif type(entity_id) == str:
        entity_id = [entity_id]
        entity_id = get_column_types(df, entity_id)
        if tdfs4ds.DISPLAY_LOGS:
            print('entity_id has been converted to a proper dictionary : ', entity_id)

    if type(feature_names) != list:
        if tdfs4ds.DISPLAY_LOGS:
            print('feature_names is not a list:', feature_names)
        if ',' in feature_names:
            feature_names = feature_names.split(',')
        else:
            feature_names = [feature_names]
        if tdfs4ds.DISPLAY_LOGS:
            print('it has been converted to : ', feature_names)
            print('check it is a expected.')

    if primary_index is not None and type(primary_index) != list:
        if tdfs4ds.DISPLAY_LOGS:
            print('primary_index is not a list:', primary_index)
        if ',' in primary_index:
            primary_index = primary_index.split(',')
        else:
            primary_index = [primary_index]
        if tdfs4ds.DISPLAY_LOGS:
            print('it has been converted to : ', feature_names)
            print('check it is a expected.')

    partitioning = tdfs4ds.utils.info.generate_partitioning_clause(partitioning=partitioning)

    if tdfs4ds.DISPLAY_LOGS:
        print("filtermanager", filtermanager)

    # Register the process and retrieve the SQL query to insert the features, and the process ID
    query_insert, process_id, query_insert_dist, query_insert_filtermanager = register_process_view.__wrapped__(
        view_name       = df,
        entity_id       = entity_id,
        feature_names   = feature_names,
        metadata        = metadata,
        with_process_id = True,
        primary_index   = primary_index,
        partitioning    = partitioning,
        filtermanager   = filtermanager,
        entity_null_substitute = entity_null_substitute
    )

    # Execute the SQL query to insert the features into the database
    execute_query(query_insert)
    execute_query(query_insert_dist)
    if tdfs4ds.DEBUG_MODE:
        print("query_insert_filtermanager",query_insert_filtermanager)
    if query_insert_filtermanager is not None:
        execute_query(query_insert_filtermanager)

    # Run the registered process and return the resulting dataset
    PROCESS_TYPE = tdfs4ds.PROCESS_TYPE
    tdfs4ds.PROCESS_TYPE = 'UPLOAD_FEATURES'
    if tdfs4ds.BUILD_DATASET_AT_UPLOAD: tdfs4ds.PROCESS_TYPE = 'UPLOAD_FEATURES WITH DATASET VALIDATION'
    tdfs4ds.RUN_ID = str(uuid.uuid4())

    if tdfs4ds.BUILD_DATASET_AT_UPLOAD:

        try:

            dataset = run(process_id=process_id, return_dataset=True)

        except Exception as e:
            tdfs4ds.process_store.process_followup.followup_close(
                run_id       = tdfs4ds.RUN_ID,
                process_type = tdfs4ds.PROCESS_TYPE,
                process_id   = process_id,
                status       = 'FAILED,' + str(e).split('\n')[0]
            )
            raise


        return dataset
    else:

        try:
            run(process_id=process_id, return_dataset=False)
        except Exception as e:
            tdfs4ds.process_store.process_followup.followup_close(
                run_id       = tdfs4ds.RUN_ID,
                process_type = tdfs4ds.PROCESS_TYPE,
                process_id   = process_id,
                status       = 'FAILED,' + str(e).split('\n')[0]
            )
            raise
        return

    tdfs4ds.PROCESS_TYPE = PROCESS_TYPE

def _upload_features(df, entity_id, feature_names,
                   feature_versions=FEATURE_VERSION_DEFAULT, primary_index = None, partitioning = '', filtermanager=None, entity_null_substitute={}, process_id = None):
    """
    Uploads features from a DataFrame to the feature store, handling entity registration, feature type determination,
    feature registration, preparation for ingestion, and storage in the designated feature tables.

    Parameters:
    - df (DataFrame): The input DataFrame containing the feature data.
    - entity_id (str or dict): The identifier for the entity to which these features belong. This can be a single ID
                               (str) or a dictionary of attribute names and values uniquely identifying the entity.
    - feature_names (list): A list of strings specifying the names of the features to be uploaded.
    - feature_versions (str or list, optional): Specifies the versions of the features to be uploaded. Can be a single
                                                string applied to all features or a list of strings specifying the version
                                                for each feature respectively. Default is 'dev.0.0'.
    - primary_index (list, optional): Specifies the columns to be used as the primary index in the feature store tables.
                                      This can significantly impact the performance of data retrieval operations.
    - partitioning (str, optional): A string indicating the partitioning strategy for the feature store tables, which can
                                    enhance query performance based on the access patterns.

    Returns:
    DataFrame: A DataFrame representing the dataset view created in the feature store, detailing the features and their
               metadata, including versions and storage locations.

    This function orchestrates several steps involved in feature storage:
    1. Registers the entity in the feature store if not already present.
    2. Determines the data types of the features based on the input DataFrame.
    3. Registers the features, including their names, types, and versions, in the feature catalog.
    4. Prepares the feature data for ingestion, including any necessary transformations.
    5. Stores the prepared feature data in the feature store.
    6. Optionally, cleans up temporary resources used during the process.
    7. Builds and returns a view of the dataset representing the uploaded features for easy access.

    Note:
    - The function relies on various sub-modules within the `tdfs4ds` library for different steps of the process, from
      entity and feature registration to data preparation and storage.
    - It is intended to be used internally within a system that manages a Teradata feature store, assuming access to
      a Teradata database and the appropriate schema for feature storage.
    - The function assumes that the feature_versions, if provided as a list, matches the length of feature_names.
    """
    from tdfs4ds.feature_store.entity_management        import register_entity
    from tdfs4ds.feature_store.feature_store_management import Gettdtypes
    from tdfs4ds.feature_store.feature_store_management import register_features
    from tdfs4ds.feature_store.feature_data_processing  import prepare_feature_ingestion
    from tdfs4ds.feature_store.feature_data_processing  import store_feature
    from tdfs4ds.utils.info import get_column_types

    # Convert entity_id to a dictionary if it's not already one
    if type(entity_id) == list:
        entity_id.sort()
        entity_id = get_column_types(df, entity_id)
        if tdfs4ds.DISPLAY_LOGS:
            print('entity_id has been converted to a proper dictionary : ', entity_id)
    elif type(entity_id) == str:
        entity_id = [entity_id]
        entity_id = get_column_types(df, entity_id)
        if tdfs4ds.DISPLAY_LOGS:
            print('entity_id has been converted to a proper dictionary : ', entity_id)

    register_entity(entity_id, primary_index=primary_index, partitioning=partitioning)

    # If feature_versions is a list, create a dictionary mapping each feature name to its corresponding version.
    # If feature_versions is a string, create a dictionary mapping each feature name to this string.
    if type(feature_versions) == list:
        selected_features = {k: v for k, v in zip(feature_names, feature_versions)}
    else:
        selected_features = {k: feature_versions for k in feature_names}

    # Get the Teradata types of the features in df.
    feature_names_types = Gettdtypes(
        df,
        features_columns=feature_names,
        entity_id=entity_id
    )

    if tdfs4ds.DEBUG_MODE:
        print('_upload_features', 'entity_id',     entity_id)
        print('_upload_features', 'entity_null_substitute', entity_null_substitute)
        print('_upload_features', 'feature_names', feature_names)
        print('_upload_features', 'primary_index', primary_index)
        print('_upload_features', 'partitioning',  partitioning)
        print('_upload_features', 'selected_features', selected_features)
        print('_upload_features', 'df.columns', df.columns)

    # Register the features in the feature catalog.
    register_features(
        entity_id,
        feature_names_types,
        primary_index,
        partitioning
    )
    if tdfs4ds.DEBUG_MODE:
        print("---------_upload_features")
        print("filtermanager     : ", filtermanager)
        print("feature names     : ", feature_names)
        print("selected features : ", selected_features)

    if process_id is not None and tdfs4ds.FEATURE_STORE_TIME is not None:
        follow_up = tdfs4ds.process_store.process_followup.follow_up_report()
        follow_up = follow_up[(follow_up.STATUS == 'COMPLETED') & (follow_up.VALIDTIME_DATE.isna() == False) & (
                    follow_up.VALIDTIME_DATE == tdfs4ds.FEATURE_STORE_TIME) & (follow_up.PROCESS_ID == process_id)]
    if filtermanager is None:
        do_compute = True
        if process_id is not None and tdfs4ds.FEATURE_STORE_TIME is not None:
            if follow_up.shape[0] > 0:
                do_compute = False
        # Prepare the features for ingestion.
        if do_compute:

            tdfs4ds.process_store.process_followup.followup_open(
                run_id       = tdfs4ds.RUN_ID,
                process_type = tdfs4ds.PROCESS_TYPE,
                process_id   = process_id
            )

            try:
                prepared_features, volatile_table_name, features_infos = prepare_feature_ingestion(
                    df,
                    entity_id,
                    feature_names,
                    feature_versions=selected_features,
                    primary_index=primary_index,
                    entity_null_substitute=entity_null_substitute
                )
                # Store the prepared features in the feature store.
                store_feature(
                    entity_id,
                    volatile_table_name,
                    entity_null_substitute=entity_null_substitute,
                    primary_index=primary_index,
                    partitioning=partitioning,
                    features_infos = features_infos
                )

                tdfs4ds.process_store.process_followup.followup_close(
                    run_id        = tdfs4ds.RUN_ID,
                    process_type  = tdfs4ds.PROCESS_TYPE,
                    process_id    = process_id
                )

            except Exception as e:
                tdfs4ds.process_store.process_followup.followup_close(
                    run_id        = tdfs4ds.RUN_ID,
                    process_type  = tdfs4ds.PROCESS_TYPE,
                    process_id    = process_id,
                    status        = 'FAILED,' + str(e).split('\n')[0]
                )
                raise
    else:
        nb_filters = filtermanager.nb_filters
        for i in range(nb_filters):
            filtermanager.update(i+1)
            if filtermanager.time_filtering:
                tdfs4ds.FEATURE_STORE_TIME = filtermanager.get_date_in_the_past()
                follow_up = tdfs4ds.process_store.process_followup.follow_up_report()
                follow_up = follow_up[(follow_up.STATUS == 'COMPLETED') & (follow_up.VALIDTIME_DATE.isna() == False) & (
                        follow_up.VALIDTIME_DATE == tdfs4ds.FEATURE_STORE_TIME) & (follow_up.PROCESS_ID == process_id)]

            do_compute = True
            if process_id is not None and tdfs4ds.FEATURE_STORE_TIME is not None:
                follow_up_ = follow_up.assign(APPLIED_FILTER=follow_up.APPLIED_FILTER.cast(tdml.VARCHAR(20000))).join(
                    tdml.DataFrame.from_query(
                        f"""
                        SELECT
                        CAST(JSON_AGG({','.join(filtermanager.col_names)}) AS VARCHAR(20000)) AS APPLIED_FILTER
                        FROM {filtermanager.schema_name}.{filtermanager.view_name}
                        """
                    ),
                    on      = 'APPLIED_FILTER',
                    how     = 'inner',
                    lprefix = 'l',
                    rprefix = 'r'
                )
                if follow_up_.shape[0] > 0:
                    do_compute = False

            if tdfs4ds.DISPLAY_LOGS:
                print(filtermanager.display())
            if do_compute:
                tdfs4ds.process_store.process_followup.followup_open(
                    run_id        = tdfs4ds.RUN_ID,
                    process_type  = tdfs4ds.PROCESS_TYPE,
                    process_id    = process_id,
                    filtermanager = filtermanager
                )
                try:
                    # Prepare the features for ingestion.
                    prepared_features, volatile_table_name, features_infos = prepare_feature_ingestion(
                        df,
                        entity_id,
                        feature_names,
                        feature_versions       = selected_features,
                        primary_index          = primary_index,
                        entity_null_substitute = entity_null_substitute
                    )

                    # Store the prepared features in the feature store.
                    store_feature(
                        entity_id,
                        volatile_table_name,
                        entity_null_substitute=entity_null_substitute,
                        primary_index = primary_index,
                        partitioning = partitioning,
                        features_infos=features_infos

                    )
                    tdfs4ds.process_store.process_followup.followup_close(
                        run_id=tdfs4ds.RUN_ID,
                        process_type=tdfs4ds.PROCESS_TYPE,
                        process_id=process_id,
                        filtermanager = filtermanager
                    )

                except Exception as e:
                    tdfs4ds.process_store.process_followup.followup_close(
                        run_id=tdfs4ds.RUN_ID,
                        process_type=tdfs4ds.PROCESS_TYPE,
                        process_id=process_id,
                        status='FAILED,' + str(e).split('\n')[0],
                        filtermanager=filtermanager
                    )
                    raise
                # Clean up by dropping the temporary volatile table.
                tdml.execute_sql(f'DROP TABLE {volatile_table_name}')

    # Build a dataset view in the feature store.
    if tdfs4ds.BUILD_DATASET_AT_UPLOAD:
        if tdfs4ds.DISPLAY_LOGS: print('build dataset for validation')
        try:
            dataset = build_dataset(
                entity_id,
                selected_features,
                view_name=None,
                entity_null_substitute = entity_null_substitute
            )
        except Exception as e:
            print('ERROR at build_dataset in _upload_features:')
            print(str(e).split('\n')[0])
            print('entity :', entity_id)
            print('selected features :', selected_features)

        # Return the dataset view.
        return dataset
    else:
        if tdfs4ds.DISPLAY_LOGS: print('no dataset built for validation. Set tdfs4ds.BUILD_DATASET_AT_UPLOAD to True if you want it')
        return


def build_dataset(entity_id, selected_features, view_name, schema_name=None, comment=None, return_query=False,
                  feature_store_time=False, join_type='INNER'):
    """
    Generate a SQL query and create a Teradata view to retrieve records for the specified entity IDs based on selected features.

    Parameters:
    ----------
    entity_id : list, dict, or str
        The entity IDs for which records are needed. Can be a list, dictionary, or string.
        - If list: contains multiple entity IDs.
        - If dict: keys are the entity IDs.
        - If str: a single entity ID.

    selected_features : dict
        A dictionary where the keys are feature table names, and the values are lists of tuples
        (feature_id, feature_version, feature_name) specifying the features to retrieve.

    view_name : str
        The name of the view to be created in the database.

    schema_name : str, optional
        The name of the database schema where the view will be created.
        Defaults to the global `tdfs4ds.SCHEMA` if not provided.

    comment : str, optional
        A comment to attach to the created view for documentation purposes. Defaults to None.

    return_query : bool, optional
        If True, the function will return the SQL query string instead of executing it. Defaults to False.

    feature_store_time : bool, optional
        If True, the query will use a specific `VALIDTIME` based on `tdfs4ds.FEATURE_STORE_TIME`.
        If False, the query will use `CURRENT VALIDTIME`. Defaults to False.

    join_type : str, optional
        Specifies the type of join to use between features: 'INNER' (default) or 'FULL OUTER'.

    Returns:
    -------
    str or tdml.DataFrame
        - If `return_query` is True, returns the generated SQL query as a string.
        - Otherwise, returns a Teradata DataFrame containing the results.

    Raises:
    ------
    ValueError
        If an invalid `join_type` is provided.
    """

    # Validate the join type
    if join_type not in ['INNER', 'FULL OUTER']:
        tdfs4ds.logger.error(f"{join_type} is not valid. Only 'INNER' and 'FULL OUTER' are authorized.")
        raise ValueError("Invalid join type. Use 'INNER' or 'FULL OUTER'.")

    # Default schema fallback if not provided
    if schema_name is None:
        schema_name = tdfs4ds.SCHEMA

    from tdfs4ds.feature_store.feature_query_retrieval import get_feature_location

    # Define the VALIDTIME clause based on feature store time
    if feature_store_time:
        if tdfs4ds.FEATURE_STORE_TIME is None:
            validtime_statement = 'CURRENT VALIDTIME'
        else:
            validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"
    else:
        validtime_statement = 'CURRENT VALIDTIME'
    tdfs4ds.logger.info(f"VALIDTIME for the query: {validtime_statement}")

    # Retrieve the locations of features from the feature store
    tdfs4ds.logger.info("Retrieving the tables where the features are located.")
    list_features = get_feature_location(entity_id, selected_features)

    # Normalize entity_id into a list format for consistent processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Sort the entity ID list for consistent query generation
    list_entity_id.sort()

    # Initialize sub-query construction
    tdfs4ds.logger.info("Generating the sub-queries for feature retrieval.")
    sub_queries = []

    # Format entity ID columns for SQL query
    txt_entity = '\n ,'.join(['B1.' + e for e in list_entity_id])

    # Construct sub-queries for each feature
    for k, v in list_features.items():
        for feature_id, feature_version, feature_name in v:
            txt_where = f"(FEATURE_ID = {feature_id} AND FEATURE_VERSION='{feature_version}')"
            feature_str = ',B1.FEATURE_VALUE AS ' + feature_name
            sub_queries.append(
                {
                    'feature_name': feature_name,
                    'query': f"""
                    SEQUENCED VALIDTIME
                    SELECT 
                       {txt_entity}
                      {feature_str}
                    FROM {k} B1
                    WHERE {txt_where}
                    """
                }
            )

    # Handle case where no features are available
    if len(sub_queries) == 0:
        tdfs4ds.logger.warning("No features available for the specified entity IDs.")
        return

    # Generate SELECT clause for the final query
    if join_type == 'INNER':
        txt_entity = '\n ,'.join(['A1.' + e for e in list_entity_id])
    elif join_type == 'FULL OUTER':
        txt_entity = '\n ,'.join(
            [f"COALESCE({','.join(['A' + str(i) + '.' + e for i, _ in enumerate(sub_queries, 1)])}) AS {e}" for e in
             list_entity_id])

    select_query = f"""
          {txt_entity}
        , A1.{sub_queries[0]['feature_name']}
    """

    # Generate FROM and JOIN clauses for the final query
    from_query = f"""
    FROM ({sub_queries[0]['query']}) A1
    """

    for i, query_ in enumerate(sub_queries[1:], 2):
        # Add the feature to the SELECT clause
        select_query += f"\t, A{i}.{query_['feature_name']}\n"

        # Create the ON clause for joining on entity IDs
        on_clause = ' AND '.join(['A1.' + c + '= A' + str(i) + '.' + c for c in list_entity_id])

        # Add the join clause to the FROM section
        from_query += f"""
        {join_type} JOIN ({query_['query']}) A{i}
        ON {on_clause}
        """

    # Combine the clauses into the final query
    query = f"""
    {validtime_statement}
    SELECT {select_query}
    {from_query}
    """

    # Wrap the query as a view creation statement
    query = f"""
    REPLACE VIEW {schema_name}.{view_name} AS
    LOCK ROW FOR ACCESS
    {query}
    """
    tdfs4ds.logger.info(f"Creating the view {view_name} in the {schema_name} database.")
    tdml.execute_sql(query)

    # Add a comment to the created view, if provided
    if comment:
        tdfs4ds.logger.info(f"Adding a comment to the view {view_name} in the {schema_name} database.")
        tdml.execute_sql(f"COMMENT ON VIEW {schema_name}.{view_name} IS '{comment}'")

    # Return the query or the DataFrame based on the `return_query` flag
    if return_query:
        tdfs4ds.logger.info("Returning the generated dataset query.")
        return query
    else:
        tdfs4ds.logger.info("Returning the dataset as a Teradata DataFrame.")
        return tdml.DataFrame.from_table(tdml.in_schema(schema_name, view_name))


def build_dataset_opt(entity_id, selected_features, view_name = None, schema_name=tdfs4ds.SCHEMA,
                  comment='dataset', no_temporal=False, time_manager=None, query_only=False, entity_null_substitute={},
                  other=None, time_column=None, filtermanager = None, filter_conditions = None
                  ):
    dataset = augment_source_with_features(
        source_schema       = None,
        source_name         = None,
        entity_id           = entity_id,
        feature_selection   = selected_features,
        output_view_name    = view_name,
        output_view_schema  = schema_name
    )

    return dataset

def augment_source_with_features(source_schema, source_name, entity_id, feature_selection, output_view_schema,
                                 output_view_name, join_type='LEFT JOIN'):
    """
    Augment a source table with selected features by creating a view that joins the source data
    with feature tables based on specified entity identifiers and feature selections. The join
    type can be specified as either 'LEFT JOIN' or 'INNER JOIN':

    - 'LEFT JOIN': Retains all rows from the source table, with missing values for unmatched features.
    - 'INNER JOIN': Returns only rows where all specified features have matching, non-missing values.

    Parameters:
    source_schema (str): The schema of the source table to augment.
    source_name (str): The name of the source table to augment.
    entity_id (str or list of str): The entity ID(s) for joining the source data with feature tables.
                                    Can be a single string or a list of strings.
    feature_selection (list): A list of features to select and join with the source data. Each feature
                              is represented as a tuple with (feature_id, feature_version).
    output_view_schema (str): The schema in which to create the output view.
    output_view_name (str): The name of the output view to create with augmented features.
    join_type (str, optional): The type of SQL join to use, either 'LEFT JOIN' for a full dataset
                               with possible missing values or 'INNER JOIN' for a dataset with
                               only complete feature matches. Defaults to 'LEFT JOIN'.

    Returns:
    tdml.DataFrame: A DataFrame object that references the newly created view with augmented features.
    """

    from tdfs4ds.feature_store.feature_query_retrieval import get_feature_location

    # Convert entity_id to a list if provided as a single string for consistency in handling
    if isinstance(entity_id, str):
        entity_id = [entity_id]

    # Retrieve feature locations (tables) for the selected features based on entity_id
    locations = get_feature_location(entity_id=entity_id, selected_features=feature_selection)

    # Initialize the SELECT part of the query with all columns from the source table
    query_select = f"""
    REPLACE VIEW {output_view_schema}.{output_view_name}
    AS LOCK ROW FOR ACCESS
    SELECT
        SOURCE.*
    """
    query_join = []  # To store the JOIN clauses for each feature
    counter = 1  # Counter for aliasing tables in joins

    # Loop through each feature table and the associated list of features
    for feature_store_view, list_features in locations.items():
        # Add each feature as a separate column selection with appropriate table alias
        for feature in list_features:
            table_name = 'A' + str(counter)  # Alias for the feature table in JOIN
            # Append the feature column to the SELECT clause with alias
            query_select += '\n, ' + table_name + '.' + feature[2]

            # Create the ON clause for joining on entity IDs between source and feature tables
            on_clause = ' AND '.join(['SOURCE.' + c + '=' + table_name + '.' + c for c in entity_id])

            # Construct the JOIN clause based on the specified join_type
            query_join.append(
                f"""
                {join_type} 
                (CURRENT VALIDTIME
                SEL
                    A.*
                  , A.FEATURE_VALUE AS {feature[2]}
                  FROM {feature_store_view} A
                  WHERE FEATURE_ID = {feature[0]} AND FEATURE_VERSION = '{feature[1]}'
                ) {table_name}
                ON {on_clause}
                """
            )
            counter += 1  # Increment the alias counter

    if source_schema is None and source_name is None:
        query_available_features, list_features = get_available_entity_id_records(entity_id, feature_selection)
        # Combine the SELECT and JOIN parts to form the complete SQL query
        query = query_select + '\n' + f'FROM ({query_available_features}) SOURCE \n' + '\n'.join(query_join)
    else:
        # Combine the SELECT and JOIN parts to form the complete SQL query
        query = query_select + '\n' + f'FROM {source_schema}.{source_name} SOURCE \n' + '\n'.join(query_join)

    # Execute the SQL query to create the augmented view
    tdml.execute_sql(query)

    # Return a DataFrame reference to the newly created view for further use
    try:
        return tdml.DataFrame.from_table(tdml.in_schema(output_view_schema, output_view_name))
    except Exception as e:
        print(str(e))
        return None


def upload_tdstone2_scores(model):
    """
    Uploads features from a model's predictions to the Teradata feature store. This function handles the entire
    workflow from extracting feature names and types, registering them in the feature catalog, preparing features for ingestion,
    storing them in the feature store, and finally creating a dataset view in the feature store.

    Parameters:
    - model: The model object whose predictions contain features to be uploaded. This model should have methods
      to extract predictions and feature information.

    Returns:
    - DataFrame: A DataFrame representing the dataset view created in the feature store, which includes
      features from the model's predictions.

    Note:
    - The function assumes that the model provides a method `get_model_predictions` which returns a Teradata DataFrame.
    - Entity ID for the model is extracted and registered in the data domain.
    - The function cleans up by dropping the volatile table created during the process.
    - The feature names and their types are extracted from the model's predictions and are registered in the feature catalog.
    """

    from tdfs4ds.feature_store.entity_management import register_entity
    from tdfs4ds.feature_store.entity_management import tdstone2_entity_id
    from tdfs4ds.feature_store.feature_store_management import tdstone2_Gettdtypes
    from tdfs4ds.feature_store.feature_store_management import register_features
    from tdfs4ds.feature_store.feature_data_processing import prepare_feature_ingestion_tdstone2
    from tdfs4ds.feature_store.feature_data_processing import store_feature

    # Extract the entity ID from the existing model.
    entity_id = tdstone2_entity_id(model)

    # Register the entity ID in the data domain.
    register_entity(entity_id)

    # Get the Teradata types of the features from the model's predictions.
    feature_names_types = tdstone2_Gettdtypes(model,entity_id)

    # Register these features in the feature catalog.
    register_features(entity_id, feature_names_types)

    # Prepare the features for ingestion into the feature store.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_model_predictions(),
            entity_id
        )
    else:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_computed_features(),
            entity_id
        )

    # Store the prepared features in the feature store.
    store_feature(entity_id, prepared_features)

    # Clean up by dropping the temporary volatile table.
    tdml.execute_sql(f'DROP TABLE {volatile_table_name}')

    # Get the list of selected features for building the dataset view.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        selected_features = model.get_model_predictions().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']
    else:
        selected_features = model.get_computed_features().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']

    # Build and return the dataset view in the feature store.
    dataset = build_dataset(entity_id, selected_features, view_name=None)
    return dataset


def roll_out(process_list, time_manager, time_id_start = 1, time_id_end = None):
    """
    Executes a series of processes for each date in a given list, managing the time and logging settings.

    This function iterates over a list of dates, updating a TimeManager object with each date, and then
    executes a list of processes for that date. It also manages the synchronization of time for a feature store
    and disables display logs during its execution.

    Parameters:
    date_list (list): A list of dates for which the processes need to be executed.
    process_list (list): A list of process IDs that need to be executed for each date.
    time_manager (TimeManager object): An object that manages time-related operations, like updating or retrieving time.

    Side Effects:
    - Sets global variables DISPLAY_LOGS and FEATURE_STORE_TIME.
    - Catches and prints exceptions along with the date on which they occurred.
    """

    #global DISPLAY_LOGS
    #global FEATURE_STORE_TIME

    # Disable display logs
    temp_DISPLAY_LOGS = tdfs4ds.DISPLAY_LOGS
    tdfs4ds.DISPLAY_LOGS = False
    PROCESS_TYPE = tdfs4ds.PROCESS_TYPE
    tdfs4ds.PROCESS_TYPE = 'ROLL_OUT'
    tdfs4ds.RUN_ID = str(uuid.uuid4())



    try:
        if time_id_end is None:
            pbar = tqdm.tqdm(range(time_id_start, time_manager.nb_time_steps + 1), desc="Starting")
        else:
            pbar = tqdm.tqdm(range(time_id_start, min([time_manager.nb_time_steps + 1,time_id_end+1]) ), desc="Starting")
        # Iterate over each date in the provided list
        for i in pbar:
            # Update the time manager with the new date
            time_manager.update(time_id = i )
            date_ = str(time_manager.display().to_pandas()['BUSINESS_DATE'].values[0])
            pbar.set_description(f"Processing {date_}")
            # Synchronize the time for the feature store with the current date
            tdfs4ds.FEATURE_STORE_TIME = time_manager.get_date_in_the_past()
            pbar.set_description(f"Processing {tdfs4ds.FEATURE_STORE_TIME}")
            if tdfs4ds.DEBUG_MODE:
                print('def roll_out','date_', date_)
                print('def roll_out','time_manager.get_date_in_the_past()', time_manager.get_date_in_the_past())
                print('def roll_out','tdfs4ds.FEATURE_STORE_TIME', tdfs4ds.FEATURE_STORE_TIME)
            # Execute each process in the process list for the current date
            for proc_id in process_list:
                pbar.set_description(f"Processing {date_} process {proc_id}")
                run(process_id=proc_id)

        tdfs4ds.DISPLAY_LOGS = temp_DISPLAY_LOGS
    except Exception as e:
        tdfs4ds.DISPLAY_LOGS = temp_DISPLAY_LOGS
        # If an exception occurs, print the date and the first line of the exception message
        #print(date_)
        print(str(e).split('\n')[0])
        tdfs4ds.PROCESS_TYPE = PROCESS_TYPE
        raise

    tdfs4ds.PROCESS_TYPE = PROCESS_TYPE


