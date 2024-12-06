# gdmo

[![PyPI](https://img.shields.io/pypi/v/gdmo.svg)](https://pypi.org/project/gdmo/)
[![Tests](https://github.com/StephanKuiper-Insight/gdmo/actions/workflows/test.yml/badge.svg)](https://github.com/StephanKuiper-Insight/gdmo/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/StephanKuiper-Insight/gdmo?include_prereleases&label=changelog)](https://github.com/StephanKuiper-Insight/gdmo/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/StephanKuiper-Insight/gdmo/blob/main/LICENSE)


# GDMO native classes for standardized interaction with data objects within Azure Databricks

This custom library allows our engineering team to use standardized packages that strip away a load of administrative and repetitive tasks from their daily object interactions. The current classes supported (V0.1.0) are: 


# Installation

Install this library using `pip`:
```bash
pip install gdmo
```
# Usage

## Forecast - Forecast
Standardized way of forecasting a dataset. Input a dataframe with a Series, a Time, and a Value column, and see the function automatically select the right forecasting model and generate an output. 

Example usage:

```python
from gdmo import TimeSeriesForecast
forecaster = TimeSeriesForecast(spark, 'Invoiced Revenue')\
                    .set_columns('InvoiceDate', 'ProductCategory', 'RevenueUSD')\
                    .set_forecast_length(forecast_length)\
                    .set_last_data_point(lastdatamonth)\
                    .set_input(df)\
                    .set_growth_cap(0.02)\
                    .set_use_cap_growth(True)\
                    .set_modelselection_breakpoints(12, 24)\
                    .set_track_outcome(False)\
                    .build_forecast()

forecaster.inspect_forecast()
```

## API - APIRequest
Class to perform a standard API Request using the request library, which allows a user to just add their endpoint / authentication / method data, and get the data returned without the need of writing error handling or need to understand how to properly build a request. 

Example usage:

```python

request = APIRequest(uri)\
            .set_content_type('application/json') \
            .set_header('bearer xxxxx') \
            .set_method('GET') \
            .set_parameters({"Month": "2024-01-01"})\
            .make_request()

response = request.get_json_response()
display(response)
```

## Tables - Landing
A class for landing API ingests and other data into Azure Data Lake Storage (ADLS). Currently can ingest Sharepoint (excel) data and JSON (API-sourced) data. The class can load data three ways: overwriting data, appending data (with check for existing filenames), or merge data in. When using a merge, the config data needs joincolumns to perform the merge on.

Example usage to ingest files from Sharepoint folder:

```python

environment     = 'xxxxx' #Databricks catalog

Sharepointsite  = 'xxxxx'
UserName        = 'xxxxx'
Password        = 'xxxxx'
Client_ID       = 'xxxxx'
adls_temp       = 'xxxxx'

sharepoint = Landing(spark, dbutils, database="xxx", bronze_table="xxx", catalog=environment, container='xxx')\
                  .set_tmp_file_location(adls_temp)\
                  .set_sharepoint_location(Sharepointsite)\
                  .set_sharepoint_auth(UserName, Password, Client_ID)\
                  .set_auto_archive(False)\
                  .get_all_sharepoint_files()

```

If you need to capture logging on top of these ingests, follow up the code with the get_log() function
```python
try:
  log = sharepoint.get_log()
  # Construct the SQL query to insert logging information into the logtable
  sql_query = f"""
    INSERT INTO {logtable} 
    SELECT now() DbxCreated, '{log['database']}', '{log['bronze_table']}', '{log['catalog']}', '{log['file_path']}', {log['records_influenced']}, '{log['start_time']}', '{log['end_time']}'
    """

  # Execute the SQL query using Spark SQL
  spark.sql(sql_query)
except Exception as e:
  raise e
```


Example usage to ingest JSON content from an API:

```python
#Sample API request using the APIRequest class
uri = 'xxxxx'
request  = APIRequest(uri).make_request()
response = request.get_json_response()

#Initiate the class, tell it where the bronze table is located, load configuration data for that table (required for delta merge), add the JSON to the landing area in ADLS, then put the landed data into a bronze delta table in the databricks catalog. 
landing = Landing(spark, dbutils, database="xxx", bronze_table="xxx", target_folder=location, filename=filename, catalog=environment, container='xxx')\
                .set_bronze(bronze)\                                
                .set_config(config)\
                .put_json_content(response)\
                .put_bronze()

```

## Tables - Delta
Class to enable you to create a delta table on azure databricks. Supports the ability to assign a primary key, foreign key constraints, table properties, partitioning, identity column, and more. 

Example usage to create a delta table with a primary key and a foreign key:

```python
from gdmo import Delta

table = Delta(db_name,table_name, spark, env, container)\
            .set_columns([
                {"name": "DbxCreated",   "data_type": "timestamp",  "comment": "Date when data was last loaded into source tables"},
                {"name": "DbxUpdated",   "data_type": "timestamp",  "comment": "Last modified timestamp"},
                {"name": "IsDeleted",    "data_type": "int",        "comment": "Deleted Flag"},
                {"name": "DataSource",   "data_type": "string",     "comment": "Identifies the source of the record."},
                {"name": "PK_ValueCol1", "data_type": "int",        "comment": "Primary Key column. Numeric value"},
                {"name": "ValueCol2",    "data_type": "string",     "comment": "Value column one"},
                {"name": "FK_ValueCol3", "data_type": "date",       "comment": "Value column two, which is a foreign key"},
              ])\
            .set_comment(table_comment)\
            .set_location(table_location)\
            .set_partitioning('DataSource')\
            .drop_existing()\
            .create_table()\
            .set_primary_key('NCC_PKValueCol1', 'PK_ValueCol1')

foreign_keys = [
    {'name': 'NCC_FKValueCol3', 'columns': 'FK_ValueCol3', 'table': 'schema.othertable'}
]

table.set_foreign_keys(foreign_keys)

```

## Tables - Gold_Consolidation
A class to perform gold layer (see databricks medallion architecture) consolidation of records. This class is usable when you have a gold table that should consist of unique records, or a timeseries dataset, which need to be sourced from multiple sources, each offering roughly the same dataset. Example usage is if you want a single gold customer table, but there are two raw sources of customer data (multiple ERP systems for example), but both offer the same sort of data. 

In order to use this class, one would need a control table to contain all unique (SQL) source codes to retrieve data in a standard format from the silver layer. By default, this class assumes there is a delta table located at "admin.bronze__gold_consolidation_sources". If that is not present, start by creating one like this:
```python
from gdmo import Delta
import os
env = os.environ['Environment']

container = '{enter container name here}'
db_name = 'admin'
table_name = 'bronze__gold_consolidation_sources'

location = os.environ.get("ADLS").format(container=container, path=db_name)
table_location = f'{location}/{table_name.replace("__", "/").lower()}'

table = Delta(db_name,table_name, spark, env, container)\
            .set_columns([
                  {"name": "DbxCreated",      "data_type": "timestamp", "comment": "Creation date in databricks"},
                  {"name": "DbxUpdated",      "data_type": "timestamp", "comment": "Last updated date"},
                  {"name": "IsDeleted",       "data_type": "int",       "comment": "Deletion Flag"},
                  {"name": "TableName",       "data_type": "string",    "comment": "Complete gold table name. IE: sales__invoices"},
                  {"name": "SourceName",      "data_type": "string",    "comment": "silver table name consolidating into the gold layer"},
                  {"name": "SourceCode",      "data_type": "string",    "comment": "sql code required to pull data from silver"},
                  {"name": "InlineVar",       "data_type": "string",    "comment": "optional. the silver sql code can contain a var in the filtering clause when loading for example only partial data for performance. this contains the varname inline in the code as a python list of dicts. , so we can do a text.replace on it. "},
                  {"name": "SortOrder",       "data_type": "int",       "comment": "When consolidation uses unique records this order is used to order the sources by importance. Lower value = higher priority. 1 = highest priority"}
              ])\
            .set_comment('Holds the silver sql codes to retrieve data for gold layer consolidation tables. ')\
            .set_location(table_location)\
            .drop_existing()\
            .create_table()\
            .set_primary_key('TableName, SourceName')
```

When ready, then add sources to this dataset by using the below code. In this example, each sourcecode contains a catalog var inline in the sql, which needs to be replaceable by a python var during runtime (called InlineVar):

```python
from gdmo import Gold_Consolidation

db_name    = 'gold'
table_name = 'tablename'
inlinevar  = '\'[catalog]\']' #stringified python list
SortOrder  = 1 #Numeric value used for deduplication of unique records when asked to

gold = Gold_Consolidation(spark, dbutils, database=db_name,gold_table=table_name)

SourceName =  'SilverDataSourceOne'
SourceCode = f'''
    SELECT  columns
    FROM [catalog].silvertable
    ...This should be your bespoke transformational layer to retrieve the records in the shape you need it in for gold. the column list should be identical to the gold table column list. 
    '''

gold.set_source(SourceName = SourceName, SourceCode = SourceCode, InlineVar = inlinevar, SortOrder=SortOrder)

```

Once sourcecodes are added to the control table, we can use a scheduled notebook (workflow) in databricks to pull data into the gold layer. The basic way of doing this is in below example:

```python
from gdmo import DbxWidget, Gold_Consolidation, DbxClearCachedTables
import os

db_name    = 'gold'
table_name = 'tablename'

final_table = db_name+'.'+table_name
stage_table = final_table+'_stage'

catalog       = DbxWidget(dbutils, 'catalog', defaultValue = os.environ.get('Environment'))
verbose       = DbxWidget(dbutils, 'verbose', defaultValue = 'N')

#Set the metadata ready. these tables might be joined to within the source codes but are added as cached tables here to decrease runtime and increase performance
MetaTables = ['metatable']
DbxClearCachedTables(spark, MetaTables)

meta = spark.sql(f'''CACHE TABLE metadata AS SELECT * from somewheremetadata''')

#Start a gold instance for this table
gold = Gold_Consolidation(spark, dbutils, database=db_name,gold_table=table_name)
gold.set_catalog(catalog)

#Set basic configuration - how is data loaded in this gold table. 
config = {
    'partitioncolumns': ['DataSource'],   #Required when loadtype is merge and the class is running in parallel (which is default)
    'loadType':         'merge',          #[Options: merge | append | overwrite]
    'loadmechanism':    'uniquevalues',   #[Options: timeseries | uniquevalues]
    'joincolumns':      ['PKColOne']      #Required when loadtype is merge
}
gold.set_config(config)

#If you want to see more comments and runtime execution, set verbose to Y
if verbose == 'Y':
  gold.set_verbose()

#Get the sourcecodes from the control table and clear staging if needed
gold.get_sourcecodes()
gold.clean_stage()

#Replace inline vars with the correct value if needed
gold.set_inlinevar({'[catalog]': catalog})

#Run the data into staging
gold.set_stage()

#Merge data into the actual table
gold.set_final()

#Drop the staging table again
gold.clean_stage()

#Clear cached tables
DbxClearCachedTables(spark, MetaTables)

#Provide visual output of the data
if verbose == 'Y':
  df = spark.sql(f'''
                  SELECT DataSource, COUNT(*) Recs
                  FROM {final_table}
                  group by DataSource
                  ''')
  df.display()
```


## Dbx - DbxWidget
A class for generating and reading a databricks notebook widget. The widget supports all four widget types (['text', 'dropdown', 'multiselect', 'combobox']) and allows for different response datatypes to be set ['text', 'int', 'double', 'float','date']

The default databricks method:
```python
dbutils.widgets.dropdown("colour", "Red", "Enter Colour", ["Red", "Blue", "Yellow"])
colour = dbutils.widgets.read("colour")
```

Using this function all the user needs to write is:
```python
colour = DbxWidget(dbutils, "colour", 'dropdown', "Red", choices=["Red", "Blue", "Yellow"])
```

A simple text value parameter:
```python
reloadData = DbxWidget(dbutils, "fullReload", 'N')
```

A simple date value parameter:
```python
reloadData = DbxWidget(dbutils, "startDate", 'N', returntype='date')
```

## Dbx - DbxClearCachedTables
A class to simply input a list of cached table names to, which will then uncache them all. 

```python
MetaTables = ['CachedTableOne','CachedTableTwo','CachedTableThree']

DbxClearCachedTables(spark, MetaTables)

```