from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col


class Table:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def join_notebook_dimension(self, notebook_dimension_table: str):
        spark = self.spark
        # Load the DataFrames (replace with actual data loading methods)
        table_lineage_df = spark.table("system.access.table_lineage")#.where(col('entity_type')=='NOTEBOOK')

        notebooks_dimension_df = spark.table(notebook_dimension_table)

        # Perform the join
        joined_df = table_lineage_df.join(
            notebooks_dimension_df,
            (table_lineage_df.entity_id == notebooks_dimension_df.object_id) &
            (table_lineage_df.entity_type == 'NOTEBOOK'),
            how='left'
        )

        # Apply the CASE logic and select the required columns
        result_df = joined_df.select(
            when(col("entity_type") == 'NOTEBOOK', col("nd.path"))
            .otherwise(None).alias("notebook_path"),
            col("entity_id"),
            col("source_type"),
            col("source_table_full_name"),
            col("target_type"),
            col("target_table_full_name")
        ).filter(
            col("source_table_full_name").isNotNull() &
            col("target_table_full_name").isNotNull()
        )
        result_df.show()
        return result_df
