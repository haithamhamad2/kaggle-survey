from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def download_and_unzip(api_username, api_key, dataset_name, destination_folder):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset_name, path=destination_folder, unzip=True)

    # Get the name of the downloaded zip file
    zip_file = os.path.join(destination_folder, os.listdir(destination_folder)[0])  

    # Return the path to the extracted folder
    
    return zip_file

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    kaggle_api_username = "" # Replace with your Kaggle API username
    kaggle_api_key = ""  # Replace with your Kaggle API key
    dataset_name = "adenrajput/merged-kaggle-survey-data"  # Replace with the Kaggle dataset name
    destination_folder = ""  # Specify the destination folder to download and extract dataset
    extracted_folder = download_and_unzip(kaggle_api_username, kaggle_api_key, dataset_name, destination_folder)
    #print("Extracted folder is ", extracted_folder)
    
    # Define the path to your CSV file
    csv_file = "merged_data.csv"
    csv_path = extracted_folder + "/" + csv_file
    print("full path is ", csv_path)
    
    #Get or create spark session
    spark = SparkSession.builder.getOrCreate()
    
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    df = spark.read \
      .option("header", "true") \
      .option("delimiter", ",") \
      .option("multiline", "true") \
      .csv(csv_path)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
