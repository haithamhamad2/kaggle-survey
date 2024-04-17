from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, when, explode, split, to_date, expr

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    
    # remove rows with first value Year
    df = data.filter(data["Year"] != "Year")

    # Rename columns
    df = df.withColumnRenamed("Year", "Survey_Year") \
    .withColumnRenamed("Duration (in seconds)","Duration") \
    .withColumnRenamed("Q2", "Age") \
    .withColumnRenamed("Q3", "Gender") \
    .withColumnRenamed("Q4", "Country") \
    .withColumnRenamed("Q11", "Education") \
    .withColumnRenamed("Q29", "Salary")

    # Update Kaggle learn values
    df = df.withColumn("Q6_3", 
                   when(col("Q6_3").isNull(), col("Q6_3")) \
                   .when(col("Q6_3") != lit("Kaggle Learn"), lit("Kaggle Learn")) \
                   .otherwise(col("Q6_3")))    
    # On which platforms have you begun or completed data science courses? 
    q6_columns = [col_name for col_name in df.columns if col_name.startswith("Q6")]
    df = df.withColumn("Course_Platform", F.concat_ws(",", *q6_columns)).drop(*q6_columns)

    #Clean the values of some of the Q31 replies
    # Update Javascript value
    df = df.withColumn("Q12_8", 
                   when(col("Q12_8").isNull(), col("Q12_8")) \
                   .when(col("Q12_8") != lit("Javascript"), lit("Javascript")) \
                   .otherwise(col("Q12_8")))
    #What programming languages do you use on a regular basis?
    q12_columns = [col_name for col_name in df.columns if col_name.startswith("Q12")]
    df = df.withColumn("Programming_Language", F.concat_ws(",", *q12_columns)).drop(*q12_columns)

    #Which of the following integrated development environments (IDE's) do you use on a regular basis?
    q13_columns = [col_name for col_name in df.columns if col_name.startswith("Q13")]
    df = df.withColumn("IDE", F.concat_ws(",", *q13_columns)).drop(*q13_columns)

    #Do you use any of the following hosted notebook products?
    q14_columns = [col_name for col_name in df.columns if col_name.startswith("Q14")]
    df = df.withColumn("Hosted_Notebook", F.concat_ws(",", *q14_columns)).drop(*q14_columns)

    #Clean the values of some of the Q31 replies
    df = df.withColumn("Q31_1", 
                   when(col("Q31_1").isNull(), col("Q31_1")) \
                   .when(col("Q31_1") != lit("Amazon Web Services (AWS)"), lit("Amazon Web Services (AWS)")) \
                   .otherwise(col("Q31_1")))
    df = df.withColumn("Q31_2", 
                   when(col("Q31_2").isNull(), col("Q31_2")) \
                   .when(col("Q31_2") != lit("Microsoft Azure"), lit("Microsoft Azure")) \
                   .otherwise(col("Q31_2")))
    df = df.withColumn("Q31_3", 
                   when(col("Q31_3").isNull(), col("Q31_3")) \
                   .when(col("Q31_3") != lit("Google Cloud Platform (GCP)"), lit("Google Cloud Platform (GCP)")) \
                   .otherwise(col("Q31_3")))
    df = df.withColumn("Q31_4", 
                   when(col("Q31_4").isNull(), col("Q31_4")) \
                   .when(col("Q31_4") != lit("IBM Cloud/Red Hat"), lit("IBM Cloud/Red Hat")) \
                   .otherwise(col("Q31_4")))
    df = df.withColumn("Q31_8", 
                   when(col("Q31_8").isNull(), col("Q31_8")) \
                   .when(col("Q31_8") != lit("Alibaba Cloud"), lit("Alibaba Cloud")) \
                   .otherwise(col("Q31_8")))
    df = df.withColumn("Q31_11", 
                   when(col("Q31_11").isNull(), col("Q31_11")) \
                   .when(col("Q31_11") != lit("None"), lit("None")) \
                   .otherwise(col("Q31_11")))

    #Which of the following cloud computing platforms do you use?
    q31_columns = [col_name for col_name in df.columns if col_name.startswith("Q31")]
    df = df.withColumn("Cloud_Platform", F.concat_ws(",", *q31_columns)).drop(*q31_columns)

    # Update PostgreSQL value
    df = df.withColumn("Q35_2", 
                   when(col("Q35_2").isNull(), col("Q35_2")) \
                   .when(col("Q35_2") != lit("PostgreSQL"), lit("PostgreSQL")) \
                   .otherwise(col("Q35_2")))
    # Update IBM Db2 value
    df = df.withColumn("Q35_7", 
                   when(col("Q35_7").isNull(), col("Q35_7")) \
                   .when(col("Q35_7") != lit("IBM Db2"), lit("IBM Db2")) \
                   .otherwise(col("Q35_7")))
    # Update Amazon DynamoDB
    df = df.withColumn("Q35_12", 
                   when(col("Q35_12").isNull(), col("Q35_12")) \
                   .when(col("Q35_12") != lit("Amazon DynamoDB"), lit("Amazon DynamoDB")) \
                   .otherwise(col("Q35_12")))
    #Do you use any of the following data products (relational databases, data warehouses, data lakes, or similar)?
    q35_columns = [col_name for col_name in df.columns if col_name.startswith("Q35")]
    df = df.withColumn("Data_Product", F.concat_ws(",", *q35_columns)).drop(*q35_columns)
    
    #select the columns needed
    df = df.select("Survey_Year","Duration","Age","Gender","Country","Education","Salary","Course_Platform","Programming_Language","IDE","Hosted_Notebook","Cloud_Platform","Data_Product")
    
    # Drop rows with null values only in specific columns
    #df_filtered = df.dropna(subset=["Age", "Gender", "Country", "Education"])

    country_mapping = {
    "United States of America": "United States",
    "Viet Nam": "Vietnam",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Republic of China": "China",
    "People 's Republic of China": "China",
    "Iran, Islamic Republic of...": "Iran"
    }   
    # Convert the keys of the country_mapping to a list
    # Create a SQL expression for the mapping
    mapping_expr = "CASE "
    for original_name, new_name in country_mapping.items():
        # Escape single quotes by doubling them
        original_name = original_name.replace("'", "''")
        mapping_expr += f"WHEN Country = '{original_name}' THEN '{new_name}' "
    mapping_expr += "ELSE Country END"

    df_cleaned = df.withColumn("Country", expr(mapping_expr)).dropna(subset=["Age", "Gender", "Country", "Education"])

    df_cleaned.filter(df_cleaned["Country"].like("%China%")).select("Country").distinct().show()
    return df_cleaned


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
