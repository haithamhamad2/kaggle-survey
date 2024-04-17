
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
import os
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    gcs_csv_path = "gs://kaggle_ml_ds_survey_bucket/kaggle_survey_transformed.csv"
    
    #Start spark session
    spark = SparkSession.builder.config('spark.jars', '/home/Haitham.hamad/spark/spark-3.3-bigquery-0.37.0.jar,/home/Haitham.hamad/spark/gcs-connector-hadoop3-2.2.21.jar').getOrCreate()
    # Set Hadoop configuration for GCS
    spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
    spark._jsc.hadoopConfiguration().set('fs.AbstractFileSystem.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS')

      
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    df = spark.read \
      .option("header", "true") \
      .option("delimiter", ",") \
      .option("multiline", "true") \
      .csv(gcs_csv_path)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
