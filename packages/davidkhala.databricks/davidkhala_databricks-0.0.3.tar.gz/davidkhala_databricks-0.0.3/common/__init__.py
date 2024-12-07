from pyspark.sql import SparkSession


class SparkDecorator:
    spark: SparkSession

    def __init__(self, spark):
        self.spark: SparkSession = spark

    def disconnect(self):
        self.spark.stop()

    @property
    def schema(self) -> str:
        """
        :return: current schema full name
        """
        return self.spark.catalog.currentCatalog() + '.' + self.spark.catalog.currentDatabase()

    @property
    def serverless(self) -> bool:
        return self.conf.get("spark.databricks.clusterUsageTags.clusterId") is None

    @property
    def conf(self) -> dict:
        return self.spark.conf.getAll
