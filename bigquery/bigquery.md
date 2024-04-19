# Bigquery Tables

The following three Bigquery tables should be created before running the pipelines:

CREATE OR REPLACE TABLE `kaggle_ml_ds_survey_dataset.kaggle_survey_results` (
  Survey_Year DATE,  
  Duration INT64,   
  Age INT64,         
  Gender STRING,
  Country STRING,
  Education STRING,
  Salary FLOAT64,    
  Course_Platform STRING,
  Programming_Language STRING,
  IDE STRING,
  Hosted_Notebook STRING,
  Cloud_Platform STRING,
  Data_Product STRING
)
PARTITION BY Survey_Year
CLUSTER BY Country
OPTIONS(
description="A table for Kaggle ML & DS survey results"
);

CREATE OR REPLACE TABLE `kaggle_ml_ds_survey_dataset.kaggle_survey_pl` (
  Survey_Year DATE,
  Country STRING,
  Programming_Language STRING
)
PARTITION BY Survey_Year
CLUSTER BY Country
OPTIONS(
description="A table for Kaggle ML & DS survey results"
);

CREATE OR REPLACE TABLE `kaggle_ml_ds_survey_dataset.kaggle_survey_cp` (
  Survey_Year DATE,
  Country STRING,
  Cloud_Platform STRING
)
PARTITION BY Survey_Year
CLUSTER BY Country
OPTIONS(
description="A table for Kaggle ML & DS survey results"
);

For optimized queries, the three tables were partitioned by Survey_Year and clustered by Country