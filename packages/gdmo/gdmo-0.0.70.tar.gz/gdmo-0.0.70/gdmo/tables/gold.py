import re
import pandas as pd
import time
from datetime import date, timedelta
from pyspark.sql.functions import lit, col, row_number
import pyspark.sql.functions as F
from IPython.display import display

from concurrent.futures import ThreadPoolExecutor, wait
from pyspark.sql import Window

from delta.tables import *



class Gold_Consolidation:
    """
        Class to consolidate datasets into gold layer. Can be used to join data from multiple datasets into a single stage table when all sources are expected to produce the same columns.

        Attributes:
        - _dbutils (object): Databricks utilities object for file operations.
        - _spark (object): SparkSession object to be used for processing.
        - _catalog (str): Catalog used in Delta Lake (default is 'prd').
        - _database (str): Name of the database where the data should be landed.
        - _gold_table (str): Name of the gold table where the data should be landed.
        - _gold_table_path (str): Complete path of the gold table.
        - _stage_table_name (str): Name of the staging table.
        - _stage_table_path (str): Path of the staging table.
        - _distinct (bool): Flag to indicate if input data is made distinct.
        - _joincolumns (list): Columns to merge on when load type is set to merge.
        - _static_cols (list): List of columns (dictionaries) with fixed values not in the source data.
        - _loadtype (str): Type of data loading (append, merge, overwrite).
        - _parallel (bool): Flag for parallel processing.
        - _InlineVar (object): Inline variables for source code.
        - _refresh (str): Flag for complete table refresh.
        - _verbose (bool): Flag for verbose logging.
        - _control_table_name (str): Table containing source codes when used.

        Methods:
        - set_catalog(self, catalog): Sets the catalog.
        - set_refresh(self, refresh): Sets a complete table refresh.
        - set_config(self, config): Sets the configuration.
        - set_not_parallel(self): Sets processing to be non-parallel.
        - set_verbose(self): Sets verbose mode for logging.
        - set_sourcecodes(self, sourcecodes): Captures a dictionary of sources.
        - set_stage(self): Runs the SQL codes through to stage.
        - get_latest_data(self): Retrieves the latest data based on the timeseries filter.
        - set_stage_key(self, keytable, keycolumn): Sets the primary key numeric key.
        - get_sourcecodes(self, specificsource=''): Retrieves the source codes for the specified source.
        - get_stage_status(self): Gets the status of the stage table.
        - set_inlinevar(self, InlineVar): Sets the inline variables for source codes.
        - set_final(self, reloaded=0): Sets the final data based on the configuration.
        - set_source(self, SourceName, SourceCode, InlineVar, SortOrder=0): Sets the source data with the provided parameters.
        - clean_stage(self): Cleans up the stage table.
    """
    
    def __init__(self, spark, dbutils, database, gold_table, triggerFullRefresh = 'N', controltable = 'admin.bronze__gold_consolidation_sources'):
        """
            Initializes a Landing object with the specified parameters.

            Parameters:
            - spark:                            SparkSession object to be used for processing.
            - dbutils:                          Databricks utilities object for file operations.
            - database:                         Name of the database where the data should be landed.
            - gold_table:                       Name of the gold table where the data should be landed.
            - catalog (str, optional):          Catalog used in Delta Lake (default is 'default').

            Raises:
            - Exception: If the specified location cannot be created.

            Notes:
            - The folder path is created if it does not exist.
        """

        self._dbutils           = dbutils                           # Required. Passes the dbutils function to be used down the line
        self._spark             = spark                             # Required. Passes a sparksession to be used down the line

        #gold vars
        self._catalog           = 'prd'                             # Optional. the catalog used in delta lake. Defaults to prd
        self._database          = database                          # Required. the gold database  that the data should be landed in
        self._gold_table        = gold_table                        # Required. the gold tablename that the data should be landed in
        self._gold_table_path   = f'{self._database}.{self._gold_table}' # Complete path of the gold table.
        self._stage_table_name  = self._gold_table + '_stage'
        self._stage_table_path  = f'{self._database}.{self._stage_table_name}'

        #Load Mechanism
        self._distinct          = False                             # By default the input data is not made distinct
        self._joincolumns       = None                              # When load type is set to merge, this will contain the columns to merge on
        self._static_cols       = []                                # List of columns (dictionaries) that should be added with their fixed value, not in the source data. 
        self._loadtype          = 'append'                          # By default we merge data in on a unique key in the joincolumns var. Other options are append and overwrite. Append has an optional command "drop" that deletes from the gold table after a specific condition and then does a simple insert. 

        self._parallel          = True
        self._InlineVar         = None
        self._refresh           = 'N'

        self._verbose           = False

        self._control_table_name = controltable                     # Table containing the sourcecodes when used

        # Check if the database exists
        databases = [db.name for db in spark.catalog.listDatabases()]
        if database not in databases:
            raise ValueError(f"Database {database} not found in the SparkSession.")

        # Check if the table name is valid
        if not re.match(r'^[a-zA-Z0-9_]+$', self._gold_table):
            raise ValueError(f"Invalid table name: {self._gold_table}. Table names can only contain alphanumeric characters and underscores.")

        """
        Example config element:
        {
            'partitioncolumns': ['UsageDate'],
            
            'loadType': 'append',           
            'loadmechanism': 'timeseries',                  #[Options: timeseries | uniquevalues]
            
            #append timeseries specific config
            'timeseriesFilterColumn': 'UsageDate',          #[Optional, required when loadmechanism = timeseries]
            'timeseriesFilterValue': '36',                  #[Optional, required when loadmechanism = timeseries]

            #append uniquevalues specific config      
            'deduplication': 'sourceRank',                  #[Optional, required when loadmechanism = uniquevalues. Options: sourceRank, distinct, False]
            'sourceRank': {1: 'SourceName', 2: '...'},      #[Optional, required when loadmechanism = uniquevalues & deduplication = sourceRank. Should contain a dict with ordering using the source names]
            
            #Merge specific config
            'joincolumns' = []                              #[Optional, required when loadmechanism = merge. Should contain a list of unique columns that make up the unique record]

            #Other
            'staticcolumns': [{'SourceName': 'SourceName'}] #[Optional]
        }
        """

    def set_catalog(self, catalog):
        """
        Function to set the catalog.

        Parameters:
        - catalog (str): The catalog to be set.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with the catalog set.

        Notes:
        - This function sets the catalog attribute of the Gold_Consolidation object to the provided catalog value.
        """
        self._catalog = catalog
        return self
      
    def set_refresh(self, refresh):
        """
        Function to set a complete table refresh.

        Parameters:
        - refresh (str): Flag indicating the type of table refresh ('Y' for full refresh, 'N' for no refresh).

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with the refresh set.

        Notes:
        - This function sets the refresh attribute of the Gold_Consolidation object to the provided refresh value.
        - If refresh is 'Y', it drops the current table content from the gold table path.
        - If refresh is not 'N' and has a length of 10, it performs a delete operation based on the timeseries filter column.
        - Raises an exception if there is an error during the table refresh process.
        """

        self._refresh = refresh
        try:
            if self._refresh == 'Y':
                print(f'Dropping current table content from {self._gold_table_path}')
                self._spark.sql(f'TRUNCATE TABLE {self._gold_table_path}')
            elif self._refresh != 'N' and len(str(self._refresh)) == 10:
                if 'timeseriesFilterColumn' not in self._config:
                    raise Exception(f"Error refreshing table {self._gold_table_path}. Timeseries filter column is required when refreshing using a specific date as filter.")
                self._spark.sql(f"DELETE FROM {self._gold_table_path} WHERE {self._config['timeseriesFilterColumn']} >= '{self._refresh}'")
        except Exception as e:
            raise Exception(f"Error refreshing table {self._gold_table_path}. {e}")

        return self

    def set_config(self, config):
        """
        Function to set the config.

        Parameters:
        - config (dict): Configuration dictionary containing settings for data loading.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with the config set.

        Notes:
        - This function sets the config attribute of the Gold_Consolidation object to the provided config dictionary.
        - If 'joincolumns' is present in the config, it sets the joincolumns attribute accordingly.
        """
        self._config = config

        if 'joincolumns' in config:
            self._joincolumns = config['joincolumns']

        return self

    def set_not_parallel(self):
        """
        Function to set the processing to be non-parallel.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with parallel processing set to False.
        """
        self._parallel = False
        return self

    def set_verbose(self):
        """
        Function to set the verbose mode for logging.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with verbose mode set to True.
        """
        self._verbose = True
        return self

    def set_sourcecodes(self, sourcecodes):
        """
            Function to capture a dictionary of sources. Basically these are all select statements to preset the data to be loaded. 
        """
        self._sourcecodes = sourcecodes
        return self
    
    def _build_stagetable(self):
        """
        Function to build the staging table.

        Returns:
        - bool: True if the staging table creation is successful.

        Notes:
        - This function retrieves the schema from the gold table path and creates a new staging table based on that schema.
        - If the staging table already exists, it is dropped before creating a new one.
        - The function uses the partition columns from the config if available to partition the staging table.
        - Verbose logging is printed if set_verbose() is called.
        """
        try:
            stage_schema = self._spark.table(self._gold_table_path).schema
            self._stage_schema = stage_schema
        except Exception as e:
            raise Exception(f"Error retrieving schema from {self._gold_table_path}: {e}")
        
        try:
            self._spark.sql(f'DROP TABLE IF EXISTS {self._stage_table_path}')
        except Exception as e:
            raise Exception(f"Error dropping existing stage table {self._stage_table_path}: {e}")

        try:
            # Create a new delta table using the schema stored in stage_schema
            writer = self._spark.createDataFrame([], stage_schema).write.format("delta").mode("overwrite")
            
            if self._config.get('partitioncolumns'):
                writer = writer.partitionBy(self._config['partitioncolumns'])
            
            writer.saveAsTable(self._stage_table_path)
        except Exception as e:
            raise Exception(f"Error creating new stage table {self._stage_table_path}: {e}")
        
        if self._verbose:
            print(f'Created a new table {self._stage_table_path} to use for loading the data.')
            display(self._spark.createDataFrame([], stage_schema))
        
        return True

    def set_stage(self):
        """
        Run the SQL codes through to stage.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object after running the SQL codes to stage.

        Raises:
        - ValueError: If the gold table is not found in the database.
        - Exception: If no sourcecodes have been set.

        Notes:
        - This function checks if the gold table exists in the database and raises an error if not found.
        - If sourcecodes are not set, an exception is raised.
        - If the stage table does not exist, it calls _build_stagetable() to create the staging table.
        - The function processes the sourcecodes either in parallel or sequentially based on the parallel flag.
        - The function prints the number of records in the stage table after processing.
        """
        
        # Check if the table exists
        #tables = [table.name for table in self._spark.catalog.listTables(self._database) if table.provider == 'delta']
        #if self._gold_table not in tables:
        #    raise ValueError(f"Table {self._gold_table} not found in the database {self._database}.")

        if self._sourcecodes is None:
            raise Exception("No sourcecodes have been set. Please use set_sourcecodes() to set the sourcecodes.")

        # Check if stage table exists. if not, call self._build_stagetable()
        if not self._spark.catalog.tableExists(self._stage_table_path):
            self._build_stagetable()

        if self._parallel:
            if self._verbose:
                print('Running all inserts in parallel')
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self._process_source, source) for source in self._sourcecodes]
                wait(futures)  # Wait for all tasks to complete

        else:
            for source in self._sourcecodes:
                self._process_source(source)

        stagerecords = self._spark.table(self._stage_table_path).count()
        print(f'finished running all data into stage. Stage contains {stagerecords} records now')
        
        return self
    
    def get_latest_data(self):
        """
        Retrieves the latest data based on the timeseries filter.

        Returns:
        - str: The formatted latest refresh date in 'YYYY-MM-DD' format.

        Notes:
        - This function calculates the latest refresh date based on the timeseries filter value and column.
        - If the last refresh date is not found, it reloads data based on the default or specified timeseries filter value.
        - Verbose logging is provided for the reloading process.
        """
        last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
        LastMonth = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
        
        if self._config['timeseriesFilterValue'] is None:
            self._config['timeseriesFilterValue'] = 60
        
        n = int(self._config['timeseriesFilterValue'])  # Default reload is 5 years of data.
        
        try:
            LastRefreshDate = self._spark.sql(f"SELECT CAST(MAX({self._config['timeseriesFilterColumn']}) as Date) LastRefreshDate FROM {self._gold_table_path}").collect()[0]["LastRefreshDate"]
            
            if not LastRefreshDate:
                # Reload trailing 5 years of data if it has been truncated.
                LastRefreshDate = (LastMonth - pd.DateOffset(months=n)).date()
                if self._verbose:
                    print(f"Final table was empty, so we will reload {n} months of data starting from {LastRefreshDate}.")
            else:
                LastRefreshDate = (LastRefreshDate - pd.DateOffset(months=n)).replace(day=1).date()
                if self._verbose:
                    print(f"The final table was reloaded last on {LastRefreshDate + pd.DateOffset(months=n)}, so we are reloading the {n} months prior to that. Reload of data starts at {LastRefreshDate}.")
        except Exception as e:
            LastRefreshDate = (LastMonth - pd.DateOffset(months=n)).replace(day=1).date()
            if self._verbose:
                print(f"Final table was empty, so we will reload {n} months of data starting from {LastRefreshDate}.")
        
        return LastRefreshDate.strftime('%Y-%m-%d')

    def _process_source(self, source_dict):
        """
        Processes the source data based on the provided dictionary.

        Parameters:
        - source_dict (dict): Dictionary containing source details like SourceName, SourceCode, and InlineVar.

        Raises:
        - Exception: If the InlineVar is not a list or not set when required.
        - Exception: If there is an error running the sourcecode after retries.

        Notes:
        - This function processes the source data by replacing inline variables and executing the SQL code.
        - It handles retries in case of errors and provides verbose logging for successful insertions.
        """
        SourceName = source_dict['SourceName']
        SourceCode = source_dict['SourceCode']
        SourceVars = source_dict['InlineVar']

        if SourceVars is not None: # The SQL code contains vars we need to replace
            SourceVars = eval(SourceVars) # Change the stringified list to an actual list
            if not isinstance(SourceVars, list):
                raise Exception(f"InlineVar is not a list. the control table entry is faulty. Please fix at the control table level.")

            if self._inlinevar is not None: #if the source code contains inline Vars and they are also set, we need to replace the values in the sourcecode with the values in the self.inlinevar for the corresponding key.

                for key in self._inlinevar:
                    val = str(self._inlinevar[key])
                    SourceCode = SourceCode.replace(key, val)
            else:
                raise Exception(f"InlineVar is not set. Please use set_inlinevar() to set the inlinevar. This source requires {str(SourceVars)}")

        sql = self._set_source_sql(SourceCode)
        if self._verbose:
            print(sql)
        retries = 0
        while retries < 1:
            try:
                df = self._spark.sql(sql)
                num_affected_rows = df.select("num_affected_rows").first()[0]
                if self._verbose:
                    print(f'Successfully inserted {num_affected_rows} records into the stage table for {SourceName}.')
                break
            except Exception as e:
                retries += 1
                if retries >= 1:
                    raise Exception(f"Error running sourcecode {SourceName} ({sql}) after 10 retries. Error: {e}")
                time.sleep(10)

    def _set_source_sql(self, sourcecode):
        """
        Sets the SQL code for the source.

        Parameters:
        - sourcecode (str): The SQL code for the source.

        Returns:
        - str: The formatted SQL code for inserting into the stage table.

        Raises:
        - Exception: If there is an error setting the sourcecode.

        Notes:
        - This function processes the sourcecode to insert data into the stage table based on the SQL code provided.
        """
        try:
            if sourcecode.strip().upper().startswith("WITH "):
                open_brackets = 0
                cte_end = 0
                for i, char in enumerate(sourcecode):
                    if char == '(':
                        open_brackets += 1
                    elif char == ')':
                        open_brackets -= 1
                    if open_brackets == 0 and sourcecode[i:i+6].upper() == "SELECT":
                        cte_end = i
                        break
                sql = f"{sourcecode[:cte_end]} INSERT INTO {self._stage_table_path} {sourcecode[cte_end:]}"
            else:
                sql = f"INSERT INTO {self._stage_table_path} {sourcecode}"
            return sql
        except Exception as e:
            raise Exception(f"Error setting sourcecode {sourcecode}. Error {e}")
    
    def set_stage_key(self, keytable, keycolumn, keyname):
        """
        Sets the primary key numeric key.

        Parameters:
        - keytable (str): The key table to be used.
        - keycolumn (str): The key column for the merge operation.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object after setting the primary key numeric key.

        Raises:
        - Exception: If there is an error setting the PK Numeric Key.

        Notes:
        - This function merges the keytable with the stage table based on the key column to update the TenantKey.
        """
        keydf = self._spark.table(keytable)

        keyname = 'f.'+keyname

        joinstring = f'f.{keycolumn} = s.ObjectStringID'
        try:
            final = DeltaTable.forName(self._spark, self._stage_table_path)

            merge_builder = final.alias('f') \
                                .merge(keydf.alias('s'), joinstring) \
                                .whenMatchedUpdate(set={keyname: 's.ObjectNumericID'}) \
                                .execute()
            if self._verbose:
                print(f'Updated the {keycolumn} key in the stage table')

            return self
        except Exception as e:
            raise Exception(f"Error setting the PK Numeric Key. Error {e}")

    def get_sourcecodes(self, specificsource = ''):
        """
        Retrieves the source codes for the specified source.

        Parameters:
        - specificsource (str): Specific source name to filter the sourcecodes.

        Returns:
        - Gold_Consolidation: The updated Gold_Consolidation object with the retrieved sourcecodes.

        Raises:
        - ValueError: If no active sourcecodes are found for the gold table in the control table.

        Notes:
        - This function fetches the sourcecodes based on the gold table name and optional specific source.
        - It sets the sourcecodes attribute and displays them if verbose logging is enabled.
        """
        f = ''
        if specificsource != '':
            f = f" AND SourceName = '{specificsource}'"

        codes = self._spark.sql(f"""
                    SELECT SourceName, SourceCode, CAST(COALESCE(InlineVar, '[]') as string) InlineVar, CAST(COALESCE(SortOrder, 0) as INT) SortOrder
                    FROM {self._control_table_name}
                    WHERE TableName = '{self._gold_table}' {f} AND IsDeleted = 0
                """)
        
        result = [source.asDict() for source in codes.collect()]
        
        if not result:
            raise ValueError(f"No active sourcecodes found for {self._gold_table} in {self._control_table_name}.")
        
        self._sourcecodes = result
        if self._verbose:
            display(self._sourcecodes)
        return self

    def get_stage_status(self):
        """
        Gets the status of the stage table.

        Returns:
        - int or bool: The count of records in the stage table if it exists, False otherwise.

        Notes:
        - This function checks if the stage table exists and returns the count of records if found.
        """
        if self._spark.catalog.tableExists(self._stage_table_path):
            count = self._spark.table(self._stage_table_path).count()
            return count
        else:
            return False

    def set_inlinevar(self, InlineVar):
        """
        Sets the inline variables for source codes.

        Parameters:
        - InlineVar (dict): Dictionary with key/value pairs for each inline variable.

        Raises:
        - Exception: If InlineVar is not a dictionary.

        Notes:
        - This function sets the inline variables to be replaced in the sourcecodes.
        """
        if not isinstance(InlineVar, dict):
            raise Exception("InlineVar must be a dict with key/value pairs for each of the inline variables that need to be replaced in the sourcecodes.")
        self._inlinevar = InlineVar
    
    def set_final(self, reloaded = 0):
        """
        Sets the final data based on the configuration.

        Parameters:
        - reloaded (int): Number of retries for merging the data.

        Raises:
        - Exception: If no records are found in the stage table or there is an error during the merge process.

        Notes:
        - This function merges the stage data into the final gold table based on the loadType configuration.
        - It handles append, merge, and overwrite operations with optional dropNotMatchedBySource flag.
        - Retries the merge process if unsuccessful and provides verbose logging for successful merges.
        """

        if 'dropNotMatchedBySource' not in self._config:
            self._config['dropNotMatchedBySource'] = False

        if self._spark.sql(f"SELECT COUNT(*) recs FROM {self._stage_table_path}").collect()[0]['recs'] == 0:
            print(f"No records found in the stage table for {self._stage_table_path}. Not merging anything into final. Please check your configuration.")
            return True
            
        if self._config['loadType'] == 'append':
            try:
                df = self._spark.sql(f'''
                                     INSERT INTO {self._gold_table_path}
                                     SELECT * FROM {self._stage_table_path}
                                     ''')
            except Exception as e:
                raise Exception(f"Error running append statement with error {e}")

        elif self._config['loadType'] == 'merge':
            if 'joincolumns' not in self._config:
                raise Exception("joincolumns must be set for merge load type")

            try:

                stage = self._spark.table(self._stage_table_path)

                if self._config['loadmechanism'] == "uniquevalues":
                    stage = self._set_unique(stage)


                joinstring = ' AND '.join([f's.{cond} = f.{cond}' for cond in self._config['joincolumns']])

                final = DeltaTable.forName(self._spark, self._gold_table_path)

                # Check if the stage dataframe contains the columns DbxUpdated and IsDeleted
                if 'DbxUpdated' not in stage.columns:
                    stage = stage.withColumn('DbxUpdated', F.current_timestamp())

                if 'IsDeleted' not in stage.columns:
                    stage = stage.withColumn('IsDeleted', F.lit(0))

                merge_builder = final.alias('f') \
                                     .merge(stage.alias('s'), joinstring) \
                                     .whenMatchedUpdateAll() \
                                     .whenNotMatchedInsertAll()

                if self._config['dropNotMatchedBySource']:
                    merge_builder = merge_builder.whenNotMatchedBySourceUpdate(set={"IsDeleted": lit(1)})

                merge_builder.execute()
                
                print(f'Merge successful for {self._stage_table_path}. Rows merged: {stage.count()}.')
                #display(stage)
                
            except Exception as e:
                try:
                    if reloaded < 1:
                        #Retry it twice with a pause.
                        time.sleep(10)
                        print(f'Merge attempt failed for {self._stage_table_path}: {e}')
                        self.set_final(reloaded + 1)
                    else:
                        print(f'Second merge attempt failed for {self._stage_table_path}: {e}')
                except Exception as e:
                    print(f'merge attempt failed for {self._stage_table_path}: {e}')

        elif self._config['loadType'] == 'overwrite':
            try:
                stage = self._spark.sql(f'SELECT * FROM {self._stage_table_path}')
                stage.write.format("delta").mode("overwrite").saveAsTable(self._gold_table_path)
            except Exception as e:
                raise Exception(f"Error running overwrite statement with error {e}")
        
    def _set_unique(self, stage):
        """
        Sets unique values for the stage table.

        Parameters:
        - stage (DataFrame): The stage DataFrame to deduplicate.

        Returns:
        - DataFrame: The deduplicated DataFrame based on the sort order.

        Raises:
        - Exception: If there is an error setting unique values for the stage table.

        Notes:
        - This function deduplicates the stage table by selecting the highest sort-ordered source per TenantID.
        """
        try:
            #We need to deduplicate the stage table now by selecting only the higher sortordered source. 
            sorter = f"SELECT SortOrder, SourceName FROM {self._control_table_name} WHERE TableName = '{self._gold_table}'"
            print(f'Getting sorting order via query {sorter}')
            sortorders = self._spark.sql(sorter)
            if sortorders.count() == 0:
                raise Exception(f"No sortorders found for {self._gold_table}")
            stage = stage.join(sortorders, stage.DataSource == sortorders.SourceName, 'left')
            print(f'Stage DF count was  {stage.count()}')

            # Assuming self._joincolumns is a list of values
            try:
                partition_columns = [col(value) for value in self._config['joincolumns']]
                # Define a Window specification partitioned by TenantID and ordered by SortOrder
                windowSpec = Window.partitionBy(*partition_columns).orderBy(stage["SortOrder"].desc())
            except Exception as e:
                raise Exception(f"Error building the partition columns for the window for {self._stage_table_path}: {e}")
            # Add a row number column based on the Window specification
            stage = stage.withColumn("row_number", row_number().over(windowSpec))

            # Select only the rows where row_number is 1 (highest sort-ordered source per TenantID)
            deduplicated_stage = stage.filter("row_number = 1").drop("row_number")
            print(f'Deduplicated DF count is  {deduplicated_stage.count()}')

            # Return the deduplicated DataFrame
            return deduplicated_stage
        except Exception as e:
            raise Exception(f"Error setting unique values for {self._stage_table_path}: {e}")

    def set_source(self, SourceName, SourceCode, InlineVar, SortOrder = 0):
        """
        Sets the source data with the provided parameters.

        Parameters:
        - SourceName (str): Name of the data source.
        - SourceCode (str): SQL code for the data source.
        - InlineVar (str): Inline variables for the source code.
        - SortOrder (int): Sort order for the source.

        Raises:
        - ValueError: If SortOrder is not an integer or if any parameter is blank.

        Notes:
        - This function sets the source data by merging it with the control table based on the TableName and SourceName.
        """
        variables = {
            "SourceName": SourceName,
            "SourceCode": SourceCode,
            "InlineVar": InlineVar,
            "SortOrder": SortOrder
        }
        for var_name, var_value in variables.items():
            if var_name == "SortOrder":
                if not isinstance(var_value, int):
                    raise ValueError(f"{var_name} must be an integer")
            elif not var_value:
                raise ValueError(f"{var_name} is blank")

        try:
            SourceCode = SourceCode.replace("'", "\\'").replace("\n", " ")
            InlineVar  = InlineVar.replace("'", "\\'").replace("\n", " ")

            # Use parameterized query to avoid SQL injection
            sql = """
                    SELECT now() AS DbxCreated, now() AS DbxUpdated, 0 AS IsDeleted, '{TableName}' AS TableName, '{SourceName}' AS SourceName, '{SourceCode}' AS SourceCode, '{InlineVar}' AS InlineVar, {SortOrder} as SortOrder
                    """.format(TableName=self._gold_table, SourceName=SourceName, SourceCode=SourceCode, InlineVar=InlineVar, SortOrder=SortOrder)

            stage = self._spark.sql(sql)
            if self._verbose:
                print(f'Stage code: {sql}')
                display(stage)

            final = DeltaTable.forName(self._spark, self._control_table_name)
            try:
                final.alias('f') \
                    .merge(stage.alias('s'),'f.TableName = s.TableName and f.SourceName = s.SourceName') \
                    .whenMatchedUpdate(set={'SourceCode': 's.SourceCode', 'InlineVar': 's.InlineVar', 'DbxUpdated': 'now()', 'IsDeleted': 's.IsDeleted', 'SortOrder': 's.SortOrder'}) \
                    .whenNotMatchedInsertAll() \
                    .execute()
                print(f'Merge succesfull')
            except Exception as e:
                print(f'merge failed: {e}')
                self._dbutils.notebook.exit(f'Merge failed due to an exception: {e}')
        except Exception as e:
            print(f"Error occurred: {e}")
            self._dbutils.notebook.exit(f"Error occurred when building a stage DF: {e}")

    def clean_stage(self):
        """
        Cleans up the stage table.

        Notes:
        - This function drops the stage table if it exists.
        """
        try:
            self._spark.sql(f'DROP TABLE IF EXISTS {self._stage_table_path}')
            if self._verbose:
                print(f'Stage table {self._stage_table_name} is dropped.')
        except Exception as e:
            print(f'Error dropping stage table: {e}')
