variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my_cred.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "kaggle-ml-ds-survey"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "us-west4"
}

variable "zone" {
  description = "Zone"
  #Update the below to your desired zone
  default     = "us-west4-b"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "bq_dataset_name" {
  description = "Kaggle Survey BigQuery Dataset"
  #Update the below to what you want your dataset to be called
  default     = "kaggle_ml_ds_survey_dataset"
}

variable "gcs_bucket_name" {
  description = "Kaggle Survey Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "kaggle_ml_ds_survey_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}