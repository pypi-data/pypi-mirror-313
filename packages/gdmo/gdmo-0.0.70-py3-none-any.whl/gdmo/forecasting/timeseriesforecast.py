# Standard library imports
from datetime import datetime, timedelta
import warnings
from IPython.display import display


# Third-party library imports
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import logging

#Modeling related imports
import matplotlib.pyplot as plt
from dateutil import relativedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing, Holt
from prophet import Prophet
from scipy.stats import linregress


# PySpark related imports
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from delta.tables import *

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

logger = logging.getLogger('cmdstanpy')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

class TimeSeriesForecast:
    """
        A class for generating forecasts based on time series data with various forecasting methods and configurations. This class is managed by DG-GL-GDMO-DS

        Attributes:
        -----------
        _col_time : str
            The column name representing time in the dataset.
        _col_identifier : str
            The column name representing different categories or series in the dataset.
        _col_value : str
            The column name representing the values to be forecasted.
        _forecast_length : int
            The number of periods to forecast into the future.
        _return_spark : bool
            Indicates whether to return the results as a Spark DataFrame (if applicable).
        _imputation_method : str
            The method used for imputing missing data in the time series.
        _forecast_method : str
            The method used for forecasting; 'auto' selects the best model automatically.
        _naive_delta : float
            The delta value used in naive forecasting models.
        _time_interval : str
            The time interval of the data (e.g., 'MS' for month start).
        _upper_percentile : float
            The upper percentile for prediction intervals.
        _lower_percentile : float
            The lower percentile for prediction intervals.
        _forecast_name : str
            The name of the forecast for identification purposes.
        _track_outcome : bool
            Whether to track the actual outcomes for comparison with the forecast.
        _input_df : pandas.DataFrame or None
            The input DataFrame containing the data to be forecasted.
        _run_concurrent : bool
            Whether to run forecasting processes concurrently for faster execution.
        _last_data_point : pandas.Timestamp
            The last data point in the time series, used to anchor the forecast.

        Methods:
        --------
        set_columns(time, identifier, value):
            Sets the column names for time, identifier, and value in the input dataset.

        set_forecast_length(length):
            Sets the number of periods to forecast into the future.

        set_forecast_method(method):
            Sets the forecasting method to be used.

        set_input(df):
            Sets the input DataFrame containing the data to be forecasted.

        set_imputation_method(method):
            Sets the method for imputing missing data in the time series.

        set_time_interval(interval):
            Sets the time interval of the data.

        set_naive_delta(delta):
            Sets the delta value used in naive forecasting models.

        set_upper_percentile(percentile):
            Sets the upper percentile for prediction intervals.

        set_lower_percentile(percentile):
            Sets the lower percentile for prediction intervals.

        set_track_outcome(track):
            Sets whether to track the actual outcomes for comparison with the forecast.

        set_last_data_point(data_point):
            Sets the last data point in the time series.

        set_run_concurrent(run_concurrent):
            Sets whether to run forecasting processes concurrently.

        build_forecast():
            Builds the forecast based on the current settings and returns the resulting DataFrame.

        inspect_forecast():
            Inspects the forecast dataset and provides an overview of its characteristics.

        get_forecast():
            Returns the forecast dataset as a pandas DataFrame.

        _forecast_auto():
            Automatically selects and runs the best forecasting model.

        _forecast_exponential_smoothing():
            Runs the Exponential Smoothing forecasting model.

        _process_naive(data):
            Processes data using the Naive forecasting model.

        _process_exp_smoothing(data):
            Processes data using the Exponential Smoothing forecasting model.

        _process_prophet(data):
            Processes data using the Prophet forecasting model.

        Model_Naive_forecast(input):
            Forecasts using the Naive model.

        Model_Exponential_smoothing(input):
            Forecasts using the Exponential Smoothing model.

        Model_Prophet(input):
            Forecasts using the Prophet model.

        _chunk_inputs(data):
            Splits the input data into manageable chunks for processing.

        _naive_trendline(data, order=1):
            Calculates a naive trendline based on the input data.

        _fill_time_series_gaps(data):
            Fills any gaps in the time series data.

        _impute(data):
            Imputes missing values in the time series data.

        _data_prep():
            Prepares the data for forecasting by applying necessary preprocessing steps.
    """

    def __init__(self, spark, name):
        self._spark                 = spark
        self._col_time              = 'time'
        self._col_identifier        = 'category'
        self._col_value             = 'value'

        self._forecast_length       = 12
        self._return_spark          = True
        self._imputation_method     = 'linear'
        self._forecast_method       = 'auto'
        self._naive_delta           = 0.01
        self._time_interval         = 'MS'
        self._ES_upper_percentile   = 0.95
        self._ES_lower_percentile   = 0.05
        self._ES_Growth_Cap         = 0.03
        self._forecast_name         = name
        self._track_outcome         = True
        self._input_df              = None
        self._run_concurrent        = True
        self._max_concurrent        = 1250 #Maximum number of series in a chunk to run parallelized
        self._use_growth_cap        = False
        
        self._min_ES                = 6   #The minimum number of datapoints to consider using Exponential Smoothing
        self._min_Prophet           = 24  #The minimum number of datapoints to consider using Prophet

        self._not_usable_series     = 0   #Tracks the inputted series it could not use.

        today = datetime.now()
        self._last_data_point = pd.to_datetime((today - timedelta(days=today.day)).replace(day=1)) #Expect last month as default

        self._start_time            = datetime.now()

    ##########################################################################################################
    # Base Public Functions. These are the functions you can use to change around default configurations     #
    # and also kick of the actual forecast creation. Finally, once made you can both view a sample result    #
    # set, view output dataframe characteristics, and retrieve the reults.                                   #
    ##########################################################################################################
    
    def set_columns(self, time, identifier, value):
        """
        Set the columns to be used for the forecast. Use this function if your input dataframe contains different column names.

        Parameters:
        time (str): The column name for the time series.
        identifier (str): The column name for the identifier.
        value (str): The column name for the value.

        Returns:
        bool: True if the columns are set successfully.
        """
        self._col_time = time
        self._col_identifier = identifier
        self._col_value = value
        return self

    def set_forecast_length(self, length):
        """
        Set the forecast length.

        Parameters:
        length (int): The forecast length to set.

        Returns:
        bool: True if the forecast length is set successfully.
        """
        if length > 0:
            self._forecast_length = length
        else:
            raise ValueError(f'Forecast length {length} is not supported. Please use a positive integer value to represent the number of datapoints to forecast. for monthly datasets this is the number of months, for daily the number of days. Default is 12.')
        return self

    def set_forecast_method(self, method):
        """
        Set the forecast method.
        
        Parameters:
        method (str): The forecast method to set ('auto' or 'exponentialsmoothing').
        
        Returns:
        bool: True if the method is set successfully.
        """
        if method in ['auto', 'exponentialsmoothing']:
            self._forecast_method = method
        else:
            raise ValueError(f'Method {method} is not supported. Please use auto or exponentialsmoothing.')
        return self

    def set_input(self, df):
        """
        Set the input dataframe.

        Parameters:
        df (DataFrame): The input dataframe to set.

        Returns:
        bool: True if the input is set successfully.
        """
        start_time = datetime.now()

        if isinstance(df, pd.DataFrame):
            if df.empty:
                raise ValueError("Input dataframe is empty.")
            
            self._input_df = self._data_prep(df)
        elif hasattr(df, 'toPandas') and callable(getattr(df, 'toPandas')):
            # Check if it's a Spark DataFrame with toPandas method
            pandas_df = df.toPandas()
            
            if pandas_df.empty:
                raise ValueError("Input dataframe converted from Spark DataFrame is empty.")
            
            self._input_df = self._data_prep(pandas_df)
        else:
            raise TypeError("Input dataframe must be a Pandas DataFrame or a Spark DataFrame with toPandas method.")

        print(self._timer('Prepare input Dataframe', start_time))

        #display(self._input_df)

        return self

    def set_imputation_method(self, method):
        """
        Set the imputation method.
        
        Parameters:
        method (str): The imputation method to set ('linear' or 'zero').
        
        Returns:
        bool: True if the method is set successfully.
        """
        if method in ['linear', 'zero']:
            self._imputation_method = method
        else:
            raise ValueError(f'Method {method} is not supported. Please use linear or zero.')
        return self

    def set_time_interval(self, interval):
        """
        Set the time interval.
        
        Parameters:
        interval (str): The time interval to set ('monthly', 'quarterly', or 'yearly').
        
        Returns:
        bool: True if the interval is set successfully.
        """
        if interval in ['daily','monthly']:

            if interval == 'monthly':
                interval = 'MS'
            elif interval == 'daily':
                interval = 'D'

            self._time_interval = interval

            if self._last_data_point == None:
                today = datetime.now()
                if self._time_interval == 'MS':
                    self._last_data_point = pd.to_datetime((today - timedelta(days=today.day)).replace(day=1))
                else:
                    self._last_data_point = pd.to_datetime(today - timedelta(1))

        else:
            raise ValueError(f'Interval {interval} is not supported. Please use monthly, quarterly or yearly.')
        return self

    def set_naive_delta(self, delta):
        """
        Set the naive delta value.
        
        Parameters:
        delta (float): The naive delta value to set (between 0 and 1).
        
        Returns:
        bool: True if the delta value is set successfully.
        """
        if 0 <= delta <= 1:
            self._naive_delta = delta
        else:
            raise ValueError(f'Delta {delta} is not supported. Please use a value between 0 and 1.')
        return self

    def set_ES_upper_percentile(self, percentile):
        """
        Set the upper percentile.

        Parameters:
        percentile (float): The upper percentile value to set (between 0 and 1).

        Returns:
        bool: True if the upper percentile is set successfully.
        """
        if 0 <= percentile <= 1:
            self._ES_upper_percentile = percentile
        else:
            raise ValueError(f'Upper percentile {percentile} is not supported. Please use a value between 0 and 1.')
        return self

    def set_ES_lower_percentile(self, percentile):
        """
        Set the lower percentile.

        Parameters:
        percentile (float): The lower percentile value to set (between 0 and 1).

        Returns:
        bool: True if the lower percentile is set successfully.
        """
        if 0 <= percentile <= 1:
            self._ES_lower_percentile = percentile
        else:
            raise ValueError(f'Lower percentile {percentile} is not supported. Please use a value between 0 and 1.')
        return self

    def set_growth_cap(self, cap):
        if 0 <= cap <= 1:
            self._ES_Growth_Cap = cap
        else:
            raise ValueError(f'A growth cap of {cap} is not supported. Please use a value between 0 and 1.')
        return self
    
    def set_use_cap_growth(self, cap):
        """
        Enable or disable concurrent runs. Default is True. If enabled and auto-select is chosen, then each individual model is run concurrently. If a single model is selected, the inputs are chunked into packages of at least 1000 series. If disabled, the inputs are processed sequentially.
        """
        if isinstance(cap, bool):
            self._use_growth_cap = cap
        else:
            raise ValueError(f'Run concurrent {cap} is not supported. Please use True or False.')
        return self
    
    def set_track_outcome(self, track):
        """
        Enable or disable tracking of results. Default is True.

        Parameters:
        track (bool): True means track the results, false means do not track.

        Returns:
        bool: True if the tracking is set successfully.
        """
        if isinstance(track, bool):
            self._track_outcome = track
        else:
            raise ValueError(f'Track outcome {track} is not supported. Please use True or False.')
        return self
    
    def set_last_data_point(self, data_point):
        """
        Set the last data point value. Typically this is a date value.

        Parameters:
        data_point (str): The last data point to set.

        Returns:
        bool: True if the last data point is set successfully.
        """
        self._last_data_point = pd.to_datetime(data_point)
        return self
    
    def set_run_concurrent(self, run_concurrent):
        """
        Enable or disable concurrent runs. Default is True. If enabled and auto-select is chosen, then each individual model is run concurrently. If a single model is selected, the inputs are chunked into packages of at least 1000 series. If disabled, the inputs are processed sequentially.
        """
        if isinstance(run_concurrent, bool):
            self._run_concurrent = run_concurrent
        else:
            raise ValueError(f'Run concurrent {run_concurrent} is not supported. Please use True or False.')
        return self
    
    def set_modelselection_breakpoints(self, min_ES = 6, min_Prophet = 30):
        """
        Set the model selection breakpoints for automatic model selection. Default is 6 - 36.
        """
        self._min_ES      = min_ES
        self._min_Prophet = min_Prophet

        return self

    def build_forecast(self):
        """
        Get the forecast.

        Returns:
        DataFrame: The forecast dataframe.
        """
        start_time = datetime.now()

        try:
            if self._forecast_method == 'auto':
                self.forecast_df = self._forecast_auto()
            elif self._forecast_method == 'exponentialsmoothing':
                self.forecast_df = self._forecast_exponential_smoothing()
            else:
                raise ValueError(f'Method {self._forecast_method} is not supported. Please use auto or exponentialsmoothing.')
        except Exception as e:
            raise ValueError(f'Error building forecast: {e}')

        print(self._timer('Building forecasts', start_time))

        if self.forecast_df is None:
            raise ValueError('No forecast has been generated.')

        print('Forecast generated succesfully. Run get_forecast([spark | pandas]) to retrieve the results, or run inspect_forecast() to get dataset characteristics.')

        if self._not_usable_series > 0:
            print(f'We had to drop {self._not_usable_series} series because they were not usable. They did not have enough datapoints.')

        return self
        
    def inspect_input(self):
        """
            Inspects the forecast dataset and provides an overview of its characteristics.

            Returns:
            dict: A dictionary containing information about the dataset including the number of records by time column,
                the number of series in the DataFrame, the number of series per forecasting method,
                and unique series where the difference between the first and last value is more than 100%.
        """
        if self.forecast_df is None:
            raise ValueError('No forecast has been generated. Please run build_forecast() first.')
        else:
            try:
                # Number of records by time column
                records_by_time = self._input_df.groupby(self._col_time).size().reset_index(name='number_of_records')
                print("Number of Records by Time Column:")
                print(records_by_time)

                # Number of series in the DataFrame
                num_series = self._input_df[self._col_identifier].nunique()
                print(f"Number of Series in the DataFrame: {num_series}")

                # Unique series where the difference between first and last value is more than 100%
                unique_series = self._input_df.groupby(self._col_identifier).apply(lambda x: (x[self._col_value].iloc[-1] - x[self._col_value].iloc[0]) / x[self._col_value].iloc[0] > 1)
                series_with_100_percent_diff = unique_series[unique_series].reset_index()[self._col_identifier]
                print("Series with >100% Difference:")
                print(series_with_100_percent_diff)

            except Exception as e:
                error_msg = f"Failed to perform inspection: {e}"
                raise Exception(error_msg)

    def inspect_forecast(self):
        """
        Inspects the forecast dataset and provides an overview of its characteristics.
        the forecasted dataset is a Pandas Dataframe with the following columns:
        - self._col_time            Time dimension
        - self._col_identifier      Series dimension
        - self._col_value           Value dimension
        - ForecastMethod            Model of forecasting used
        - UpperInterval             Upper certainty bounds of the forecast
        - LowerInterval             Lower certainty bounds of the forecast

        Returns:
        dict: A dictionary containing information about the dataset including the number of records by time column,
            the number of series in the DataFrame, the number of series per forecasting method,
            and unique series where the difference between the first and last value is more than 100%.
        """
        if self.forecast_df is None:
            raise ValueError('No forecast has been generated. Please run build_forecast() first.')
        else:
            # Number of series per Forecasting Method
            series_per_method = self.forecast_df['ForecastMethod'].value_counts().reset_index()
            series_per_method.columns = ['ForecastMethod', 'count']
            print("\nNumber of Series per Forecasting Method:")
            print(series_per_method)

            # Unique series where the difference between first and last value is more than 100%
            series_diff = self.forecast_df.groupby(self._col_identifier).apply(lambda x: (x[self._col_value].iloc[-1] - x[self._col_value].iloc[0]) / x[self._col_value].iloc[0] > 1)
            series_with_100_percent_diff = series_diff[series_diff].reset_index()[self._col_identifier]

            total_series = self.forecast_df[self._col_identifier].nunique()
            outlier_series = series_diff.any(level=0).sum()
            percentage_outlier_series = (outlier_series / total_series) * 100

            print("\nTotal Series:", total_series)
            print("Outlier Series Count:", outlier_series)
            print("Percentage of Outlier Series:", np.round(percentage_outlier_series, 2))

            # Number of series per Forecasting Method
            series_per_method = self.forecast_df['ForecastMethod'].value_counts().reset_index()
            series_per_method.columns = ['ForecastMethod', 'TotalSeries']

            # Calculate outliers per ForecastMethod
            outlier_series = self.forecast_df.groupby(['ForecastMethod', self._col_identifier]).apply(lambda x: (x[self._col_value].iloc[-1] - x[self._col_value].iloc[0]) / x[self._col_value].iloc[0] > 1)
            outlier_series_count = outlier_series.any(level=[0, 1]).groupby('ForecastMethod').sum()

            # Calculate total series per ForecastMethod
            total_series_per_method = self.forecast_df.groupby('ForecastMethod')[self._col_identifier].nunique()

            # Calculate percentage of outliers per ForecastMethod
            percentage_outliers = (outlier_series_count / total_series_per_method) * 100

            # Create a matrix with Total Series, Outlier Series Count, and Percentage of Outlier Series per ForecastMethod
            outlier_matrix = pd.DataFrame({
                'Total Series': total_series_per_method,
                'Outlier Series Count': outlier_series_count,
                'Percentage of Outlier Series': percentage_outliers
            })

            print("\nOutlier Matrix:")
            print(outlier_matrix)

            # Create a graph showing the relationship between series and percentage increase
            series_percentage_increase = self.forecast_df.groupby(self._col_identifier).apply(lambda x: (x[self._col_value].iloc[-1] - x[self._col_value].iloc[0]) / x[self._col_value].iloc[0] * 100)

            # Define the bins for grouping based on percentage increase
            bins = [-np.inf, 0, 50, 100, 150, np.inf]
            labels = ['0-50%', '50-100%', '100-150%', '150-200%', '200%+']

            # Group the series based on percentage increase bins
            grouped_series = pd.cut(series_percentage_increase, bins=bins, labels=labels)

            # Create a bar graph showing the relationship between series and percentage increase groups
            plt.figure(figsize=(10, 6))
            grouped_series.value_counts().sort_index().plot(kind='barh')
            plt.xlabel('Number of Series')
            plt.ylabel('Percentage Increase Group')
            plt.title('Series Grouped by Percentage Increase')
            plt.tight_layout()
            plt.show()


            historical_sum = pd.concat(self._input_df.values()).groupby(self._col_time)[self._col_value].sum()
            #historical_sum = self._input_df.groupby(  self._col_time)[self._col_value].sum()
            forecasted_sum = self.forecast_df.groupby(self._col_time)[self._col_value].sum()

            plt.figure(figsize=(12, 6))
            historical_sum.plot(kind='bar', color='fuchsia', label='Historical', stacked=True)
            forecasted_sum.plot(kind='bar', color='purple', label='Forecasted', stacked=True)
            plt.xlabel(self._col_time)
            plt.ylabel('Sum of ' + self._col_value)
            plt.title('Sum of ' + self._col_value + ' by ' + self._col_time)
            plt.legend()
            plt.tight_layout()
            plt.show()
   
    def get_forecast(self, type = 'spark'):
        """
        Gets the forecast dataset.
        
        Returns:
        DataFrame: The forecast dataset.
        """
        if self.forecast_df is None:
            raise ValueError('No forecast has been generated. Please run build_forecast() first.')
        else:
            if type == 'spark':
                return self._spark.createDataFrame(self.forecast_df)
            elif type == 'pandas':
                return self.forecast_df
            else:
                raise ValueError(f'Type {type} is not supported. Please use spark or pandas.')

    ##########################################################################################################
    # Forecasting Functions. These are the functions you can use to either have it auto-select models or     #
    # run specific models                                                                                    #
    ##########################################################################################################
    
    def _forecast_auto(self):
        """
        Auto-select the best forecasting model based on the number of datapoints available per individual series.

        Returns:
        DataFrame: The forecast dataframe.
        """
        try:

            forecasts = []
            input_naive_forecasts = []
            input_exp_smoothing_forecasts = []
            input_prophet_forecasts = []

            # Categorize individual series based on the number of datapoints
            try:
                classification_start_time = datetime.now()

                for individual, df in self._input_df.items():
                    count = len(df)  # Get the count of records in the Pandas DataFrame for the individual

                    if count < self._min_ES:
                        input_naive_forecasts.append((individual, df))
                    elif self._min_ES <= count <= self._min_Prophet:
                        input_exp_smoothing_forecasts.append((individual, df))
                    else:
                        input_prophet_forecasts.append((individual, df))

                print(self._timer('Autoforecast: series classification', classification_start_time))
            except Exception as e: 
                print ("Error categorizing data")

            # Display the number of series for each forecasting method
            print(f"Number of series for Naive Forecast: {len(input_naive_forecasts)}")
            print(f"Number of series for Exponential Smoothing: {len(input_exp_smoothing_forecasts)}")
            print(f"Number of series for Prophet Forecast: {len(input_prophet_forecasts)}")
            print(f"Total forecasts to make: {len(input_naive_forecasts) + len(input_exp_smoothing_forecasts) + len(input_prophet_forecasts)}")

            if len(input_naive_forecasts) + len(input_exp_smoothing_forecasts) + len(input_prophet_forecasts) == 0:
                raise ValueError('No series meet the minimum number of data points required for forecasting. No forecast will be generated. Please increase the minimum number of data points required for forecasting.')

            runner_start_time = datetime.now()

            
            all_naive_forecasts   = []
            all_es_forecasts      = []
            all_prophet_forecasts = []

            if self._run_concurrent:
                # Execute forecasting methods concurrently using ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=10) as executor:
                    if len(input_naive_forecasts) > 0:
                        if len(input_naive_forecasts) > self._max_concurrent:
                            
                            chunks = self._chunk_inputs(input_naive_forecasts)
                            print(f'Chunking input into {len(chunks)} chunks for Naive Forecast')
                            i = 1
                            for chunk in chunks:
                                naive_future = executor.submit(self._process_naive, chunk)
                                all_naive_forecasts.append(naive_future.result())
                                print(f'Finished Naive chunk {i} of {len(chunks)}')
                                i += 1
                        else:
                            naive_future = executor.submit(self._process_naive, input_naive_forecasts)
                            all_naive_forecasts.append(naive_future.result())

                    if len(input_exp_smoothing_forecasts) > 0:
                        if len(input_exp_smoothing_forecasts) > self._max_concurrent:
                            chunks = self._chunk_inputs(input_exp_smoothing_forecasts)
                            print(f'Chunking input into {len(chunks)} chunks for Exponential Smoothing Forecast')
                            i = 1
                            for chunk in chunks:
                                exp_smoothing_future = executor.submit(self._process_exp_smoothing, chunk)
                                all_es_forecasts.append(exp_smoothing_future.result())
                                print(f'Finished ES chunk {i} of {len(chunks)}')
                                i += 1
                        else:
                            exp_smoothing_future = executor.submit(self._process_exp_smoothing, input_exp_smoothing_forecasts)
                            all_es_forecasts.append(exp_smoothing_future.result())
                            
                    if len(input_prophet_forecasts) > 0:
                        if len(input_prophet_forecasts) > self._max_concurrent:
                            chunks = self._chunk_inputs(input_prophet_forecasts)
                            print(f'Chunking input into {len(chunks)} chunks for Prophet Forecasts')
                            i = 1
                            for chunk in chunks:
                                prophet_future = executor.submit(self._process_prophet, chunk)
                                all_prophet_forecasts.append(prophet_future.result())
                                print(f'Finished Prophet chunk {i} of {len(chunks)}')
                                i += 1
                        else:
                            prophet_future = executor.submit(self._process_prophet, input_prophet_forecasts)
                            all_prophet_forecasts.append(prophet_future.result())

            else:
                # Execute each model consecutively
                if len(input_naive_forecasts)   > 0:
                    all_naive_forecasts         = [self._Model_Naive_forecast(input_naive_forecasts)]

                if len(input_exp_smoothing_forecasts) > 0:
                    all_es_forecasts            = [self._Model_Exponential_smoothing(input_exp_smoothing_forecasts)]

                if len(input_prophet_forecasts) > 0:
                    all_prophet_forecasts       = [self._Model_Prophet(input_prophet_forecasts)]

            print(self._timer('Autoforecast: All Forecasting models', runner_start_time))

            # Combine the DataFrames from different forecasting methods
            combined_forecasts = pd.DataFrame()  # Initialize an empty DataFrame

            # Check if each forecast DataFrame exists before appending
            if len(input_naive_forecasts) > 0 and all_naive_forecasts is not None:
                print('Naive forecasts found:')
                all_naive_forecasts = pd.concat(all_naive_forecasts, ignore_index=True)
                display(all_naive_forecasts.head())
                combined_forecasts = combined_forecasts.append(all_naive_forecasts, ignore_index=True)

            if len(input_exp_smoothing_forecasts) > 0 and all_es_forecasts is not None:
                print('ES forecasts found:')
                all_es_forecasts = pd.concat(all_es_forecasts, ignore_index=True)
                display(all_es_forecasts.head())
                combined_forecasts = combined_forecasts.append(all_es_forecasts, ignore_index=True)

            if len(input_prophet_forecasts) > 0 and all_prophet_forecasts is not None:
                print('Prophet forecasts found:')
                all_prophet_forecasts = pd.concat(all_prophet_forecasts, ignore_index=True)
                display(all_prophet_forecasts.head())
                combined_forecasts = combined_forecasts.append(all_prophet_forecasts, ignore_index=True)

            # Display the combined DataFrame
            #combined_forecasts.show()

            return combined_forecasts

        except Exception as e:
            # Handle any exceptions that occur during the forecasting process
            print(f"The automatic forecast resulted in an error: {e}")
            
    def _forecast_exponential_smoothing(self):
        """
        Run the exponential smoothing forecasting method. Needs to be written out further still.
        """

        chunks = self._chunk_inputs(self._input_df)
        
        if self._run_concurrent:
            try:
                # Execute forecasting methods concurrently using ThreadPoolExecutor
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(self._process_exp_smoothing, chunk) for chunk in chunks]
                
                # Retrieve the results from the futures
                results = [future.result() for future in futures]
                
                # Combine the results if needed
                result = self._spark.createDataFrame(results[0].schema)
                for res_df in results:
                    result = result.union(res_df)
            except Exception as e:
                # Handle any exceptions that occur during concurrent processing
                raise Exception(f"The exponential smoothing forecast resulted in an error when running multiple chunks: {e}")
        else:
            try:
                # Process the entire DataFrame in a single chunk
                result = self._process_exp_smoothing(self._input_df)
            except Exception as e:
                # Handle any exceptions that occur during concurrent processing
                raise Exception(f"The exponential smoothing forecast resulted in an error: {e}")
        
        return result

    ##########################################################################################################
    # Processor Functions. These are utilized for parallel processing of forecasts to speed it up            #
    ##########################################################################################################
    
    def _process_naive(self, data):
        return self._Model_Naive_forecast(data)
    
    def _process_exp_smoothing(self, data):
        return self._Model_Exponential_smoothing(data)

    def _process_prophet(self, data):
        return self._Model_Prophet(data)

    ##########################################################################################################
    # Forecasting Models available. All models take an input list of tuples (individual, data) as input.     #
    ##########################################################################################################

    def _Model_Naive_forecast(self, input_df):
        start_time = datetime.now()
        try:
            percent_change = float(self._naive_delta)
            slope = 0
            time = self._col_time

            forecasts = pd.DataFrame()
            forecast_start = self._last_data_point + relativedelta.relativedelta(months=1)

            # Generate forecast dates based on the forecast length and time interval
            forecast_dates = pd.date_range(start=forecast_start, periods=self._forecast_length, freq=self._time_interval)
            #print(f'Forecast dates: {forecast_dates}')

            for individual, data in input_df:
                #print(f'Naive forecasting for individual: {individual}')
                #display(data)

                try:
                    values_length = len(data)
                    try:
                        value = data[self._col_value].iloc[-1]
                    except Exception as e:
                        raise Exception(f"Failed to retrieve the last value from the data: {e}. Values length: {values_length}")
                    #print(f'Value length: {values_length}')
                    if values_length <= 6:
                        # If values_length is smaller or equal to 6, generate a flat forecast
                        forecast = [value] * len(forecast_dates)
                        upper_intervals = [value * 1.1] * len(forecast_dates)
                        lower_intervals = [value * 0.75] * len(forecast_dates)
                    else:
                        value, slope = self._naive_trendline(data)
                        percent_change = 1.00 + (slope / 4)

                        forecast = []
                        upper_intervals = []
                        lower_intervals = []

                        for i in range(len(forecast_dates)):
                            try:
                                if i > 12:
                                    target_percent_change = self._ES_Growth_Cap
                                else:
                                    target_percent_change = (self._ES_Growth_Cap / 3) - 0.2 * (i / 6)

                                if percent_change > target_percent_change:
                                    percent_change = target_percent_change
                                elif percent_change < -target_percent_change:
                                    percent_change = -target_percent_change

                                forecast_value = np.round(value * (1 + percent_change), 2)
                                upper_interval = np.round(forecast_value * 1.1, 2)
                                lower_interval = np.round(forecast_value * 0.75, 2)

                                forecast.append(forecast_value)
                                upper_intervals.append(upper_interval)
                                lower_intervals.append(lower_interval)

                                #Show some debug data here. Upper is the percentage change used. 
                                #upper_intervals.append(percent_change)
                                #lower_intervals.append(target_percent_change)

                                value = forecast[-1]
                                #print(f'Next value: {value}. Percentage used to get there: {percent_change}')
                            except Exception as e:
                                raise Exception(f"Failed to generate a forecast value with the percentage change: {e}")


                    # Create a forecast DataFrame for the individual
                    forecast_df = pd.DataFrame({
                        self._col_identifier: individual,
                        self._col_value: forecast,
                        'UpperInterval': upper_intervals,
                        'LowerInterval': lower_intervals,
                        'ForecastMethod': 'naive'
                    }, index=forecast_dates)

                    forecast_df.index.name = time
                    forecast_df.reset_index(inplace=True)

                    forecasts = forecasts.append(forecast_df)

                except Exception as e:
                    raise Exception(f"Error processing individual forecast: {e}")

            print(self._timer('Modelling: Naive forecast', start_time))

            return forecasts

        except Exception as e:
            raise Exception(f"The naive forecast resulted in an error: {e}")

    def _Model_Exponential_smoothing(self, input_df):
        start_time = datetime.now()
        try:
            
            # Create a DataFrame to store forecasting results
            forecasts = pd.DataFrame()

            if self._use_growth_cap:
                print(f'I am going to place a cap on growth for the ES model of {self._ES_Growth_Cap} %')

            for individual, data in input_df:
                months_of_data = len(data)

                if months_of_data == 0:
                    continue

                if months_of_data < self._min_ES:
                    print(f'Flipping ES down to Naive because {individual} has {months_of_data} months of data, which is less than {self._min_ES}')
                    naive_forecast_df = self._Model_Naive_forecast([(individual, data)])
                    forecasts = forecasts.append(naive_forecast_df)
                    continue

                if months_of_data >= 6:
                    num_of_recent_months = -6
                else:
                    num_of_recent_months = -months_of_data

                recent_months = data[self._col_value].values[num_of_recent_months:]

                if np.diff(recent_months).mean() > 0:
                    alpha = 0.5
                    beta = 0.1
                else:
                    alpha = 0.1
                    beta = 0.5

                # Training Model (Holt's Linear Trend Model)
                hltm = Holt(data[self._col_value]).fit(smoothing_level=alpha, smoothing_slope=beta)
                hltm_pred = hltm.forecast(self._forecast_length)

                # Making sure no predictions are negative, if they are set them equal to 0
                hltm_pred[hltm_pred < 0] = 0

                # Cap unnatural growth to at most a predefined % month over month if thats desired
                if self._use_growth_cap:
                    value, slope = self._naive_trendline(data)
                    hltm_pred = self._cap_growth(individual, hltm_pred, slope)
                    hltm_pred = hltm_pred * .9

                # ss: add prediction interval to forecast result
                df_simul = hltm.simulate(nsimulations=self._forecast_length, repetitions=500, random_state=0)
                upper_ci = df_simul.quantile(q=self._ES_upper_percentile, axis='columns')
                lower_ci = df_simul.quantile(q=self._ES_lower_percentile, axis='columns')

                upper_ci[upper_ci<0] = 0
                lower_ci[lower_ci<0] = 0

                # Check if forecasted value is zero and upper bound is higher than 500. if so, add a 1/4 of upper bound to forecast
                if (hltm_pred == 0).any() and (upper_ci > 500).any():
                    hltm_pred[hltm_pred == 0] = 0.25 * upper_ci

                # Storing forecast
                forecast = pd.DataFrame({self._col_identifier: individual,
                                        self._col_value: np.round(hltm_pred,2),
                                        'UpperInterval': np.round(upper_ci,2),
                                        'LowerInterval': np.round(lower_ci,2),
                                        'ForecastMethod': 'exponentialsmoothing'}, index=None)
                
                forecast.index.name = self._col_time
                forecast.reset_index(inplace=True)
                
                # Appending forecast to forecasts DataFrame
                forecasts = forecasts.append(forecast)

            print(self._timer('Modelling: ES forecast', start_time))
            return forecasts

        except Exception as e:
            raise Exception(f"The exponential smoothing forecast resulted in an error: {e}")

    def _Model_Prophet(self, input_df):
        start_time = datetime.now()

        try:
            
            forecasts = pd.DataFrame()
            i = 1
            for individual, data in input_df:

                value, slope = self._naive_trendline(data)

                try:
                    prophet_model = Prophet()

                    prophet_data = data.rename_axis('ds').reset_index().rename(columns={self._col_value: 'y'})
                    
                    prophet_model.fit(prophet_data)
                except Exception as e:
                    error_msg = f"Failed to fit Prophet forecast for individual {individual}: {e}"
                    print(error_msg)
                    display(prophet_data.head())
                    raise Exception(error_msg)

                try:
                    future = prophet_model.make_future_dataframe(periods=self._forecast_length, freq=self._time_interval)
                    forecast = prophet_model.predict(future)
                    #display(forecast)
                except Exception as e:
                    error_msg = f"Failed to make Prophet future forecast for individual {individual}: {e}"
                    print(error_msg)
                    raise Exception(error_msg)

                try:
                    forecast.set_index('ds', inplace=True)
                except Exception as e:
                    error_msg = f"Failed to set the index on the forecast df for {individual}: {e}"
                    print(error_msg)
                    display(forecast.head())
                    raise Exception(error_msg)
                #print(f'Series {individual} head: ')
                #display(forecast.head())
                try:

                    # Generate forecast dates based on the forecast length and time interval
                    forecast_start = self._last_data_point + relativedelta.relativedelta(months=1)
                    forecast_dates = pd.date_range(start=forecast_start, periods=self._forecast_length, freq=self._time_interval)
                    
                    if len(forecast_dates) != len(forecast):
                        forecast = forecast.tail(len(forecast_dates))                        

                    # Prepare the forecast DataFrame
                    forecast_df = forecast.reset_index()[['ds', 'yhat', 'yhat_upper', 'yhat_lower']]

                    forecast_df['yhat'][forecast_df['yhat']<0] = 0 #Disallow negative values
                    forecast_df['yhat'] = forecast_df['yhat'].round(2)
                    forecast_df['yhat_upper'] = forecast_df['yhat_upper'].round(2)
                    forecast_df['yhat_lower'] = forecast_df['yhat_lower'].round(2)
                    #forecast_df[self._col_time] = forecast_dates
                    forecast_df[self._col_identifier] = individual
                    forecast_df = forecast_df.rename(columns={'ds':         self._col_time,
                                                              'yhat':       self._col_value,
                                                              'yhat_upper': 'UpperInterval',
                                                              'yhat_lower': 'LowerInterval'})
                    forecast_df['ForecastMethod'] = 'Prophet'

                    # Reorder columns
                    forecasted_df = forecast_df[[self._col_time, self._col_identifier, self._col_value, 'UpperInterval', 'LowerInterval', 'ForecastMethod']]

                    # add to the overall Pandas DataFrame while setting the time column as the index
                    forecasts = forecasts.append(forecasted_df)
                except Exception as e:
                    error_msg = f"Failed to create Prophet forecast DataFrame for individual {individual}: {e}"
                    display(forecast.head())
                    raise Exception(error_msg)

            print(self._timer('Modelling: Prophet', start_time))
            return forecasts

        except Exception as e:
            raise Exception(f"The Prophet forecast resulted in an error: {e}")

    ####################################
    # Helper functions used internally #
    ####################################

    def _chunk_inputs(self, data):
        """
        Chunk the input data into smaller chunks for processing, especially when running concurrent tasks.

        Parameters:
        data (DataFrame): The input data to be chunked.

        Returns:
        list: A list of DataFrame chunks based on the specified chunk size and run_concurrent flag.
        """
        chunks = []
        try:
            if self._run_concurrent:
                datasize = len(data)
                min_chunk_size = int(self._max_concurrent * 0.6)
                max_chunk_size = self._max_concurrent
                chunk_size = max(min_chunk_size, min(max_chunk_size, datasize // (datasize // min_chunk_size)))

                num_chunks = int(datasize + chunk_size - 1) // chunk_size

                for i in range(num_chunks):
                    start = i * chunk_size
                    end = min((i + 1) * chunk_size, datasize)
                    chunk = data[start:end]  # Chunk the list of DataFrames
                    chunks.append(chunk)

            else:
                # Process the entire DataFrame in a single chunk
                chunks.append(data)
        except Exception as e:
            raise Exception(f"Failed to chunk the input data: {e}")

        return chunks

    def _naive_trendline(self, data):
        '''
        trendline() is a helper function for naive_forecast() to determine if an individual's value is going up or down so that it can produce an appropriate forecast.

        Args:
            data  : DataFrame containing values for the individual.

        Returns:
            slope : Float, the slope of the data if it were to be plotted. Positive slope values indicate an increasing forecast, and negative slope values indicate a decreasing forecast.
        '''
        try:
            if data.empty or len(data) < 2:
                raise ValueError("Insufficient data points for trendline calculation")

            #Extract the values from the DataFrame
            datavalues = data[self._col_value].values
            try:
                first_val = data[self._col_value].iloc[0]
                last_val  = data[self._col_value].iloc[-1]
                second_to_last_val  = data[self._col_value].iloc[-2]
            except Exception as e:
                raise ValueError(f"Error in setting first and last value: {e}")

            slope = 0  # Initialize slope to a default value

            datapoints = len(datavalues)

            #Try Lingress to get a slope
            try:
                slope, intercept, r_value, p_value, std_err = linregress(range(len(datavalues)), datavalues)
                if intercept < 0:
                    intercept = last_val
                #print(f'Slope made via linregres based on {first_val} growing to {last_val}: {slope}. Intercept: {intercept}. Percentage slope: {((slope / intercept) / (len(datavalues) -1)) * 100}%')
                slope = (slope / intercept) / (len(datavalues) -1) #Make it a percentage increase instead of a flat value
            except Exception as e:
                print(f'Slope could not be made using lingress: {e}')

            if slope == 0 or slope == None:
                # Fallback. Calculate the slope based on the first and last values in the data

                # Compute the slope
                x1 = 0
                try:
                    x2 = len(data) - 1
                except Exception as e:
                    raise ValueError("Error in setting x1 and x2: " + str(e))
                y1 = first_val
                y2 = last_val

                try:
                    slope = (y2 - y1) / (x2 - x1)
                except Exception as e:
                    print(f"Error in calculating slope: {e}")

                if slope < 0:
                    #Negative slopes can happen, but should be marked as zero then. This is a bit of a hack, but it works.
                    slope = 0

                intercept = last_val

            if last_val == second_to_last_val:
                slope = 0

            lastmonthslope = (last_val - second_to_last_val) / second_to_last_val

            slope = (slope + lastmonthslope) / 2 #Average the last month slope and the linregress value to put an emphasis on the last month slope
            #print(f'Final slope to use: {slope} with intercept {intercept}')
            return intercept, slope
        except Exception as e:
            print(f"Error in calculating trendline slope: {e}")
            return None

    def _cap_growth(self, individual, hltm_pred, slope):
        capped_pred = hltm_pred.copy()
        
        #Cap is divided in Y1, Y2, and Y3 cap. 
        CapY1 = self._ES_Growth_Cap
        CapY2 = CapY1 * .6667
        CapY3 = CapY2 * .5

        #Monthly growth rate calculation
        discounted_growth_rate = slope / len(hltm_pred)
        try:
            for i in range(1, len(hltm_pred)):
                growth_rate = (hltm_pred[i] - hltm_pred[i-1]) / hltm_pred[i-1]

                if growth_rate > discounted_growth_rate:
                    growth_rate = discounted_growth_rate

                if i <= 12:
                    cap = CapY1
                elif i <= 24:
                    cap = CapY2
                else:
                    cap = CapY3

                if growth_rate > cap:
                    if np.round((growth_rate * pow((1 - growth_rate),2) * pow(1 - cap, i * 3)) * 100, 4) < np.round(cap, 2):
                        rate = np.round((growth_rate * pow((1 - growth_rate),2) * pow(1 - cap, i * 3)) * 100, 4)
                    else:
                        rate = cap

                    #print(f'Capping growth rate for individual {individual} to {np.round(cap, 2) * 100} %as it grew with {np.round(growth_rate * 100, 4)} %. A better fit might be {np.round((growth_rate * pow((1 - growth_rate),2) * pow(1 - cap, i * 3)) * 100, 4)} %. This month value is {np.round(hltm_pred[i], 2)} and the previous month value is {np.round(hltm_pred[i-1], 2)}. Discounted growth rate is {np.round(discounted_growth_rate * 100, 4)} %. Original slope was {np.round(slope * 100, 4)} % against a data length of {len(hltm_pred)}.')

                    rate_used = (1 + rate)
                    #rate_used = np.round((growth_rate * pow((1 - growth_rate),3) * pow(1 - cap, i * 6)) * 100, 4)

                    capped_pred[i] = hltm_pred[i-1] * (rate_used)
        except Exception as e:
            raise Exception(f"Error in capping growth rate for {individual} with slope {slope}: {e}")
        return capped_pred

    def _fill_time_series_gaps(self, individual, data):
        '''
        fill_time_series_gaps() is a helper function for impute(). It creates new rows if there are any dates missing in an individual's time series.

        Args:
            data          : Pandas DataFrame containing the data for the individual.
            individual    : Python string of the individual's identifier.

        Returns:
            data : Pandas DataFrame that is fixed with complete dates.
        '''

        try:      
            data = data.resample(self._time_interval).asfreq().fillna(np.nan)
            data[self._col_identifier] = data[self._col_identifier].fillna(individual)
            return data
        except Exception as e:
            raise Exception(f"Error in filling time series gaps: {e}")

    def _impute(self, individual, data):
        """
        Impute missing values in an individual's dataset for a Spark DataFrame.

        Parameters:
        data (DataFrame): Input Pandas DataFrame of the individual's data.
        imputation_method (str): Method for imputing missing values ('linear' or 'zero').

        Returns:
        DataFrame: Pandas DataFrame that is imputed and clean, without missing values.
        """


        # Fill in time series gaps
        try:
            data = self._fill_time_series_gaps(individual, data)
        except Exception as e:
            raise Exception(f"Error in filling time series gaps: {e}")

        # Check for missing values
        try:
            if data.isnull().values.any():
                # Linear imputation
                if self._imputation_method == 'linear':
                    try:
                        data[self._col_value] = data[self._col_value].interpolate(method='linear')
                    except Exception as e:
                        raise Exception(f"Error in imputing missing values using linear imputation: {e}")
                # Zero imputation
                elif self._imputation_method == 'zero':
                    try:
                        data[self._col_value] = data[self._col_value].fillna(0)
                    except Exception as e:
                        raise Exception(f"Error in imputing missing values using zero imputation: {e}")

                else:
                    raise ValueError(f'Imputation method {self._imputation_method} is not supported. Please use "linear" or "zero".')

        except Exception as e:
            raise Exception(f"Error in checking for missing values: {e}")

        return data
        
    def _data_prep(self, df):
        """
        Prepare the main query's result for forecasting using Spark DataFrames. the input is made of a Pandas DF to make the imputation and filling of time series gaps workable. 

        Returns:
        dict: Python dictionary of identifiers and their respective datasets.
        """
        # Unpack definitions supplied by user
        #time = self._col_time
        #identifier = self._col_identifier
        #value = self._col_value
        try:
            # Convert timestamps to Spark TimestampType
            df[self._col_time]  = pd.to_datetime(df[self._col_time])
            df[self._col_value] = df[self._col_value].astype(float)
            
            # Initialize df_dictionary which will be filled and returned.
            df_dictionary = dict()

            for individual, data in df.groupby(self._col_identifier):

                # If all values are null, continue to next indiviudual, there's no data for a forecast ._.
                if data[self._col_value].isnull().all():
                    #print(f'Category was empty so no forecast: {individual}')
                    self._not_usable_series += 1
                    continue
                
                # Make dates a DateTime type
                data[self._col_time] = pd.to_datetime(data[self._col_time])
                
                # Make sure that individual doesn't have any future data points.
                data = data[data[self._col_time] <= self._last_data_point]
                
                # If individual's most recent month does not equal last_data_point, don't create a forecast for them.

                if data[self._col_time].max() < self._last_data_point:
                    #print(f'Not forecasting {individual}. We forecast only series with last data point of {self._last_data_point}, but this series has the latest data on {data[self._col_time].max()}')
                    self._not_usable_series += 1
                    continue
                

                # Set the index to time for necessary operations
                data.set_index(self._col_time, inplace=True)
                data.sort_index(inplace=True)

                # If there are any negative values, make them null and have it handled by impute() later on.
                if data[self._col_value].lt(0).any():
                    data[self._col_value][data[self._col_value] < 0] = np.nan
                
                
                # Imputing missing data if there is any.
                try:
                    data = self._impute(individual, data)
                except Exception as e:
                    raise Exception(f"Error in imputing data: {e}")
        
                # Adding cleaned individual and its time series to azure dictionary
                serie_df = data.drop(self._col_identifier, axis=1)

                if serie_df is not None:
                    df_dictionary[individual] = serie_df
                else:
                    raise Exception(f"Error in creating a Spark DataFrame for {individual}")
                
            return df_dictionary
    
        except Exception as e:
            raise Exception(f"Error in data preparation: {e}")

    def _timer(self, stepname, start_time):
        delta = datetime.now() - start_time
        sec = delta.total_seconds()
        return f'{stepname} took {round(sec)} seconds'
    
#Room to add in more forecasting classes to tackle things like anomaly detection, financial or demand forecasts, or even classification algorithms. 