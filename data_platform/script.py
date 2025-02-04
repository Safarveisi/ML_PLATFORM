from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("MLPlatform").getOrCreate()

# Processing raw Iris data
df = spark.read.csv(
    "s3a://${S3_BUCKET}/ml_platform/etl/raw/iris.data",
    inferSchema=True,
    header=False,
    sep=","
    ) \
    .toDF("sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)", "target")

df1 = df.withColumn("target", when(col("target") == "Iris-setosa", 0)
                             .when(col("target") == "Iris-versicolor", 1)
                             .when(col("target") == "Iris-virginica", 2))

# Write the preprocessed spark df into S3 as a single csv file (${S3_BUCKET} will be filled via envsubst later - see Taskfile.yml)
df1.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save("s3a://${S3_BUCKET}/ml_platform/etl/preprocessed")
