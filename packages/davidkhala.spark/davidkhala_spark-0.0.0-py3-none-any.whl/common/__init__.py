from pyspark.sql import SparkSession

class Regular:
    """
    Visit https://spark.apache.org/docs/latest/sql-getting-started.html#starting-point-sparksession for creating regular Spark Session
    """

    @staticmethod
    def sparkSession():
        return SparkSession.builder.getOrCreate()


class SessionDecorator:
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
