from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, when, explode, split, to_date


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    table_id = 'kaggle-ml-ds-survey.kaggle_ml_ds_survey_dataset.kaggle_survey_results'
    table_id_pl = 'kaggle-ml-ds-survey.kaggle_ml_ds_survey_dataset.kaggle_survey_pl'
    table_id_cp = 'kaggle-ml-ds-survey.kaggle_ml_ds_survey_dataset.kaggle_survey_cp'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    df = df.withColumn("Survey_Year", to_date(lit(col("Survey_Year")), "yyyy"))
    df_pl = df.select("Survey_Year", "Country", explode(split("Programming_Language", ",")).alias("programming_language"))
    df_cp = df.select("Survey_Year", "Country", explode(split("Cloud_Platform", ",")).alias("Cloud_Platform"))

    pandas_df = df.toPandas()
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        pandas_df,
        table_id,
        if_exists='replace',  # Specify resolution policy if table name already exists
    )
    #spark = SparkSession.builder.getOrCreate()
    #pd.DataFrame.iteritems = pd.DataFrame.items
    #df_spark = spark.createDataFrame(df)
    #df_pl = df.select("Survey_Year", "Country", explode(split("Programming_Language", ",")).alias("programming_language"))
    #df_pl = df.explode('Programming_Language')[['Survey_Year', 'Country', 'Programming_Language']]
    
    df_pl = df_pl.toPandas()
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df_pl,
        table_id_pl,
        if_exists='replace',  # Specify resolution policy if table name already exists
    )

    df_cp = df_cp.toPandas()
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df_cp,
        table_id_cp,
        if_exists='replace',  # Specify resolution policy if table name already exists
    )