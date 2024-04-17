from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from mage_ai.orchestration.triggers.api import trigger_pipeline
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'kaggle_ml_ds_survey_bucket'
    object_key = 'kaggle_survey_transformed.csv'
 
    #convert dataframe to Pandas to run with code below
    pandas_df = df.toPandas()

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        pandas_df,
        bucket_name,
        object_key,
    )

    trigger_pipeline(
    'kaggle_survey_gcs_to_bigquery',
    variables={},
    check_status=False,
    error_on_failure=False,
    poll_interval=60,
    poll_timeout=None,
    schedule_name=None,  # Enter a unique name to create a new trigger each time
    verbose=True,
)
