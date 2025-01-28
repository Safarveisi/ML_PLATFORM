import mlflow
from mlflow.entities import ViewType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("MLPlatform").getOrCreate()
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
df1.show()

mlflow.set_tracking_uri("http://ip:5000")
print(f"The Mlflow tracking uri is: {mlflow.get_tracking_uri()}")