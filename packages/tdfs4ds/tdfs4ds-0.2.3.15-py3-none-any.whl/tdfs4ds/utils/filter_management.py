import teradataml as tdml
import tdfs4ds
import datetime


def get_hidden_table_name(table_name):
    return table_name + '_HIDDEN'


class FilterManager:
    """
    Manages dynamic filtering on a database table by creating and maintaining a view based on specified filter criteria.

    This class enables dynamic filtering of a Teradata database table, providing methods to create, update, and manage
    a view that represents filtered data based on a specific filter ID. It facilitates loading new filters, updating
    existing ones, and managing time-based filtering if applicable.

    Attributes:
        schema_name (str): The schema in the database containing the table and view.
        table_name (str): The underlying table in the schema holding the raw data for filtering.
        view_name (str): The view representing filtered data based on current filter criteria.
        filter_id_name (str): The column identifying different filters. Defaults to 'filter_id'.
        nb_filters (int): The count of filters currently defined in the table, updated with filter changes.
        col_names (list): List of column names in the table excluding the filter ID and time columns.
        time_filtering (bool): Indicates if time-based filtering is enabled based on a 'BUSINESS_DATE' column.
    """

    def __init__(self, table_name, schema_name, filter_id_name='filter_id', time_column = None):
        """
        Initializes the FilterManager for managing filtered views.

        Checks for the existence of the specified table in the schema. If the table exists, the FilterManager
        initializes attributes for the column names, filter count, and time-based filtering. If not, provisions
        for table creation are set up.

        Args:
            table_name (str): Name of the table to manage filters for.
            schema_name (str): Name of the schema where the table is located.
            filter_id_name (str, optional): Column name used to identify filters. Defaults to 'filter_id'.
            time_column (str, optional): Optional time column name for time-based filtering.
        """
        self.schema_name    = schema_name
        self.table_name     = get_hidden_table_name(table_name)
        self.view_name      = table_name
        self.filter_id_name = filter_id_name
        self.nb_filters     = None
        self.col_names      = None
        self.time_filtering = None

        if self._exists():
            if tdfs4ds.DEBUG_MODE:
                print('filter exists: ',[x for x in tdml.db_list_tables(schema_name=self.schema_name).TableName.values if
                    x.lower().replace('"', '') == self.view_name.lower()])
                print('schema_name:', self.schema_name)
                print('table_name:', self.table_name)
            df = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
            self.filter_id_name = df.columns[0]
            self.nb_filters     = tdml.execute_sql(
                f"SEL MAX({self.filter_id_name}) AS nb_filters FROM {self.schema_name}.{self.table_name}").fetchall()[
                0][0]
            self.time_filtering = self._istimefiltering()
            if self.time_filtering:
                self.col_names = df.columns[2::]
            else:
                self.col_names = df.columns[1::]

    def _istimefiltering(self):
        """Check if the table has a 'BUSINESS_DATE' column for time-based filtering."""
        df = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
        return 'BUSINESS_DATE' in df.columns

    def _exists(self):
        """Check if both table and view exist."""
        existing_tables = [x.lower().replace('"', '') for x in
                           tdml.db_list_tables(schema_name=self.schema_name).TableName.values]
        return self.view_name.lower() in existing_tables or self.table_name.lower() in existing_tables
    def load_filter(self, df, primary_index=None, time_column = None):
        """
        Loads a new filter into the table and updates the view to reflect this filter.

        This method takes a DataFrame as input, assigns filter IDs to each row, and updates or replaces the table
        and view to reflect the new filter configuration. If `time_column` is specified and present in `df`,
        it will be used in time-based filtering logic. Raises a ValueError if `time_column` is specified but not found in `df`.

        Args:
            df (DataFrame): DataFrame containing the new filter configuration.
            primary_index (list, optional): List of primary index columns for the table. Defaults to `['filter_id']`.
            time_column (str, optional): Column name used for time-based filtering, if applicable.
        """

        if time_column and time_column not in df.columns:
            raise ValueError(f"Specified time_column '{time_column}' not found in DataFrame columns.")

        if time_column is None:
            self.col_names = df.columns
            all_columns    = ','.join(df.columns)
            collect_stats  = ','.join([f'COLUMN ({c}) \n' for c in df.columns])
        else:
            self.time_filtering = True
            # check if time_colum is part of the column
            self.col_names = [c for c in df.columns if c != time_column]
            all_columns    = ','.join(['BUSINESS_DATE'] + [c for c in df.columns if c != time_column])
            collect_stats  = ','.join([f'COLUMN ({c})' for c in ['BUSINESS_DATE'] + [c for c in df.columns if c != time_column]])




        if time_column is None:
            df_filter = df.assign(**{
                self.filter_id_name: tdml.sqlalchemy.literal_column(
                    f"ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY {all_columns})", tdml.BIGINT())}
                                  )[['filter_id'] + df.columns]

        else:
            df_filter = df.assign(**{
                self.filter_id_name: tdml.sqlalchemy.literal_column(
                    f"ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY {all_columns})", tdml.BIGINT()),
                'BUSINESS_DATE' : df[time_column]
            })[['filter_id'] + ['BUSINESS_DATE'] + [c for c in df.columns if c != time_column]]


        if primary_index is None:
            df_filter.to_sql(
                table_name    = self.table_name,
                schema_name   = self.schema_name,
                if_exists     = 'replace',
                primary_index = ['filter_id'])
        else:
            df_filter.to_sql(table_name=self.table_name, schema_name=self.schema_name, if_exists='replace',
                             primary_index=primary_index)

        query = f"""
        REPLACE VIEW {self.schema_name}.{self.view_name} AS
        SEL {all_columns}
        FROM {self.schema_name}.{self.table_name}
        WHERE {self.filter_id_name} = 1
        """

        # Collect stats

        query_collect_stats = f"""
        COLLECT STATISTICS USING NO SAMPLE AND NO THRESHOLD
               COLUMN (filter_id)
        ,      {collect_stats}
        ON {self.schema_name}.{self.table_name}
        """
        tdml.execute_sql(query_collect_stats)
        tdml.execute_sql(query)

        self.nb_filters = tdml.execute_sql(
            f"SEL MAX({self.filter_id_name}) AS nb_filters FROM {self.schema_name}.{self.table_name}").fetchall()[0][0]

    def _drop(self):
        """
        Drops the view and the table from the database if they exist.

        This method is used to clean up the database by removing the managed view and table. It checks for the existence of the table and view before attempting to drop them.
        """
        # Drop the table if it exists
        if self._exists():
            tdml.db_drop_view(schema_name=self.schema_name, table_name=self.table_view)
            tdml.db_drop_table(schema_name=self.schema_name, table_name=self.table_name)

    def update(self, filter_id):
        """
        Updates the view to apply a new filter based on the provided filter ID.

        Args:
            filter_id (int): The ID of the filter to apply. The view will be updated to only show data that matches this filter ID.
        """
        if not self._exists():
            raise ValueError(f"The filter has not be initialized with load_filter or has been deleted.")

        if self.time_filtering:
            query = f"""
            REPLACE VIEW {self.schema_name}.{self.view_name} AS
            SEL {','.join(['BUSINESS_DATE']+self.col_names)}
            FROM {self.schema_name}.{self.table_name}
            WHERE {self.filter_id_name} = {filter_id}
            """

        else:
            query = f"""
            REPLACE VIEW {self.schema_name}.{self.view_name} AS
            SEL {','.join(self.col_names)}
            FROM {self.schema_name}.{self.table_name}
            WHERE {self.filter_id_name} = {filter_id}
            """

        if tdfs4ds.DEBUG_MODE:
            print(query)
        tdml.execute_sql(query)

    def display(self):
        """
        Retrieves the current data from the view as a DataFrame.

        Returns:
            DataFrame: The current data visible through the view, filtered by the active filter ID.
        """
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.view_name))

    def get_all_filters(self):
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))

    def get_date_in_the_past(self):
        """
        Retrieves the earliest date and time value from the table.

        Returns:
            str: The earliest date and time value as a formatted string ('YYYY-MM-DD HH:MM:SS').
        """

        if self._istimefiltering() == False:
            raise ValueError(f"The filter manager is not filtering on time.")

        # '9999-01-01 00:00:00'
        date_obj = self.display().to_pandas().reset_index().BUSINESS_DATE.values[0]

        if isinstance(date_obj, datetime.datetime):
            # print("temp is a datetime.datetime object")
            datetime_obj = date_obj
        elif isinstance(date_obj, datetime.date):
            # print("temp is a datetime.date object")
            # Convert date object to a datetime object at midnight (00:00:00)
            datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        elif isinstance(date_obj, np.datetime64):
            # Case when the object is a numpy.datetime64, convert it to datetime
            datetime_obj = date_obj.astype('datetime64[ms]').astype(datetime.datetime)
        else:
            print("temp is neither a datetime.date nor a datetime.datetime object")
            print('temp', date_obj)
            print('temp type', type(date_obj))
            return

        # Convert datetime object to string
        output_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        return output_string