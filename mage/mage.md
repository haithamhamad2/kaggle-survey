<!-- omit in toc -->
# Mage AI Installation and project configuration

- [Mage AI Installation](#mage-ai-installation)
- [Mage AI Project configuration](#mage-ai-project-configuration)
- [Mage kaggle\_survey project pipelines](#mage-kaggle_survey-project-pipelines)

## Mage AI Installation
```pip3 install mage-ai```

## Mage AI Project configuration
All the mage project configuration and pipleline files are under [kaggle_survey](kaggle_survey) folder  
Copy the kaggle_survey folder to your VM.

Edit the configuration file [io_config.yaml](kaggle_survey/io_config.yaml) and set the variable
**GOOGLE_SERVICE_ACC_KEY_FILEPATH** to point to your VM json file

Edit the configuration file [metadata.yaml](kaggle_survey/metadata.yaml) and set the spark variable to the spark GCS and BigQuery connectors downloaded earlier
spark_jars: ['/home/Haitham.hamad/spark/spark-3.3-bigquery-0.37.0.jar,/home/Haitham.hamad/spark/gcs-connector-hadoop3-2.2.21.jar']

Edit the data loader file, [load_spark_csv.py](kaggle_survey/data_loaders/load_spark_csv.py) and change the variables
kaggle_api_username=
kaggle_api_key=
dataset_name="adenrajput/merged-kaggle-survey-data"
destination_folder=

Edit the [kaggle.json](../kaggle/kaggle.md) file downloaded from the Kaggle website and fill the Kaggle_api_username and kaggle_api_key values


You can then start mage by running
```mage start kaggle_survey```

Open Mage project from  
http://VM static IP:6789

## Mage kaggle_survey project pipelines
The two pipelines created for this project are:  
  1. kaggle_survey_csv_to_gcs  
  2. kaggle_survey_csv_to_bigquery
  
The two pipelines are linked together. The data exporter block of the first pipeline, kaggle_survey_csv_to_gcs, calls the trigger function below that runs the second pipleline, kaggle_survery_csv_to_bigquery
```
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
```


**kaggle_survey_csv_to_gcs pipleline can be run or scheduled and it will run both pipelines**
