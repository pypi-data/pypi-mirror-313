import teradataml as tdml
import datetime

import tdfs4ds
import numpy as np

def get_hidden_table_name(table_name):
    return table_name + '_HIDDEN'
class TimeManager:
    """
    A class to manage time-related operations in a database table.

    Attributes:
        schema_name (str): Name of the schema in the database.
        table_name (str): Name of the table in the schema.
        data_type (str): Type of the date/time data, defaults to 'DATE'.
    """

    def __init__(self, table_name, schema_name):
        """
        Initializes the TimeManager with a table name, schema name, and optionally a data type.

        If the table doesn't exist, it creates one with a BUSINESS_DATE column of the specified data type.

        Args:
            table_name (str): Name of the table.
            schema_name (str): Name of the schema.
            data_type (str, optional): Type of the date/time data. Defaults to 'DATE'.
        """
        self.schema_name   = schema_name
        self.table_name    = get_hidden_table_name(table_name)
        self.view_name     = table_name
        self.time_id       = 'time_id'
        self.nb_time_steps = None
        self.data_type     = None

        if self._exists():
            df = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
            d_ = {x[0]: x[1] for x in df._td_column_names_and_types}
            self.data_type = d_['BUSINESS_DATE']
            self.nb_time_steps  = tdml.execute_sql(
                f"SEL MAX(TIME_ID) AS nb_time_steps FROM {self.schema_name}.{self.table_name}").fetchall()[
                0][0]

    def load_time_steps(self, df, time_column):
        """
        Loads a new filter into the table and updates the view to reflect this filter.

        This method takes a DataFrame as input, assigns filter IDs to each row, and updates or replaces the table and view to reflect the new filter configuration.

        Args:
            df (DataFrame): The data containing the new filter configuration.
        """

        df_            = df.assign(**{
            'time_id': tdml.sqlalchemy.literal_column(
            f"ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY {time_column})", tdml.BIGINT()),
            'BUSINESS_DATE' : df[time_column]
        })[['time_id','BUSINESS_DATE']]

        d_ = {x[0]: x[1] for x in df_._td_column_names_and_types}
        self.data_type = d_['BUSINESS_DATE']

        df_.to_sql(
            table_name    = self.table_name,
            schema_name   = self.schema_name,
            if_exists     = 'replace',
            primary_index = ['time_id']
        )

        query = f"""
         REPLACE VIEW {self.schema_name}.{self.view_name} AS
         SEL BUSINESS_DATE
         FROM {self.schema_name}.{self.table_name}
         WHERE time_id = 1
         """

        tdml.execute_sql(query)

        self.nb_time_steps = tdml.execute_sql(
            f"SEL MAX(time_id) AS nb_filters FROM {self.schema_name}.{self.table_name}").fetchall()[0][0]


    def _exists(self):
        """
        Checks if the table exists in the database.

        Returns:
            bool: True if the table exists, False otherwise.
        """

        return len([x for x in tdml.db_list_tables(schema_name=self.schema_name).TableName.values if
                    x.lower().replace('"', '') == self.table_name.lower()]) > 0

    def _drop(self):
        """
        Drops the table if it exists.
        """
        # Drop the table if it exists
        if self._exists():
            tdml.db_drop_table(schema_name=self.schema_name, table_name=self.table_name)


    def update(self, time_id):
        """
        Updates the view to apply a new filter based on the provided filter ID.

        Args:
            filter_id (int): The ID of the filter to apply. The view will be updated to only show data that matches this filter ID.
        """
        if self._exists():
            query = f"""
            REPLACE VIEW {self.schema_name}.{self.view_name} AS
            SEL BUSINESS_DATE
            FROM {self.schema_name}.{self.table_name}
            WHERE TIME_ID = {time_id}
            """

            if tdfs4ds.DEBUG_MODE:
                print(query)
            tdml.execute_sql(query)

    def display(self):
        """
        Displays the table.

        Returns:
            DataFrame: The table data as a DataFrame.
        """
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.view_name))

    def get_date_in_the_past(self):
        """
        Retrieves the earliest date and time value from the table.

        Returns:
            str: The earliest date and time value as a formatted string ('YYYY-MM-DD HH:MM:SS').
        """
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

    def get_list_date(self):
        """
        Retrieve a list of dates from the specified table.

        This function returns a DataFrame containing the dates from the table specified by the schema_name and table_name attributes of the class.

        Returns:
        DataFrame: A Teradata DataFrame containing the dates from the specified table.
        """
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))

    def generate_timeline(self, schema_name, view_name, current_included=True):
        """
        Generate a timeline view based on business dates from a hidden source view.

        This function creates a new SQL view that includes business dates from a hidden source view.
        The timeline view can either include or exclude the current business date based on the `current_included` flag.

        Parameters:
        schema_name (str): The name of the schema where the new view will be created.
        view_name (str): The name of the new view to be created.
        current_included (bool, optional): If True, includes the current business date in the timeline.
                                           If False, excludes the current business date. Defaults to True.

        Returns:
        DataFrame: A Teradata DataFrame representing the created timeline view, containing the selected business dates.
        """
        # Construct the base query to replace the view with the timeline data
        query = f"""
        REPLACE VIEW {schema_name}.{view_name} AS
        SEL BUSINESS_DATE
        FROM {self.schema_name}.{self.view_name + '_HIDDEN'} A
        """
        # Modify the query based on whether the current business date should be included
        if current_included:
            query += f"WHERE BUSINESS_DATE <= (SELECT BUSINESS_DATE FROM {self.schema_name}.{self.view_name})"
        else:
            query += f"WHERE BUSINESS_DATE < (SELECT BUSINESS_DATE FROM {self.schema_name}.{self.view_name})"

        # Execute the query to create the view
        tdml.execute_sql(query)
        # Return the DataFrame of the created view
        return tdml.DataFrame(tdml.in_schema(schema_name, view_name))

    def get_current_step(self):

        res = tdml.execute_sql(f"SELECT TIME_ID FROM {self.table_name} WHERE BUSINESS_DATE = (SELECT BUSINESS_DATE FROM {self.view_name})").fetchall()

        if len(res)==1:
            return res[0][0]

        return
