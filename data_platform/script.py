from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("MLPlatform").getOrCreate()

# Example of an ETL job (can be anything)
df = spark.createDataFrame(
    [
        ("sue", 32),
        ("li", 3),
        ("bob", 75),
        ("heo", 13),
    ],
    ["first_name", "age"],
)

df1 = df.withColumn(
    "life_stage",
    when(col("age") < 13, "child")
    .when(col("age").between(13, 19), "teenager")
    .otherwise("adult"),
)

df2 = df1.where(col("life_stage").isin(["teenager", "adult"]))

# Write the preprocessed spark df into S3 (${S3_BUCKET} will be filled via envsubst later - see Taskfile.yml)
df2.write.parquet("s3a://${S3_BUCKET}/ml_platform/etl", mode="overwrite")
