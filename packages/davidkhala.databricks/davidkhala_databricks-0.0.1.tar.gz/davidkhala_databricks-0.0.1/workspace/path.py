from typing import Iterator

from databricks.sdk import WorkspaceExt
from databricks.sdk.service.workspace import ObjectInfo, ObjectType
from pyspark.sql.connect.session import SparkSession

from common import DatabricksConnect
from workspace import APIClient, Workspace


class API:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def ls(self, path="/"):
        """
        function to retrieve objects within specified path
        :param path:
        :return:
        """
        return self.api_client.get('/workspace/list', {'path': path})

    def scan_notebooks(self, path="/") -> list:
        """
        Get Notebook Paths
        :param path:
        :return:
        """
        result = []
        response = self.ls(path)
        if "objects" in response:
            for object_item in response["objects"]:
                if object_item["object_type"] == "NOTEBOOK":
                    result.append([object_item["object_id"], object_item["path"]])
                elif object_item["object_type"] == "DIRECTORY":
                    result = result + self.scan_notebooks(object_item["path"])
        return result


class SDK:
    def __init__(self, w: WorkspaceExt):
        self.workspace = w

    @staticmethod
    def from_workspace(w: Workspace):
        return SDK(w.client.workspace)

    def ls(self, path="/") -> Iterator[ObjectInfo]:
        return self.workspace.list(path, recursive=True)

    def get_by(self, *, notebook_id: str | int = None, path: str = None) -> str | None:
        for o in self.ls():
            if o.object_type == ObjectType.NOTEBOOK:
                if notebook_id:
                    if o.object_id == int(notebook_id):
                        return o.path
                if path is not None:
                    if path in o.path:
                        return str(o.object_id)


class NotebookIndex:
    notebook_name = "notebooks_dimension"

    def __init__(self, spark: SparkSession):
        self.spark = spark
        _d = DatabricksConnect(spark)
        self.serverless = _d.serverless
        if self.serverless:
            self.schema = _d.schema

    @property
    def notebook_full_name(self):
        """
        full name of notebook dimension GlobalTempView or Table
        :return:
        """

        return f"{self.schema}.{self.notebook_name}" if self.serverless else f"global_temp.{self.notebook_name}"

    def build(self, api: API) -> bool:
        """
        :return: True if found any notebooks, False otherwise
        """
        _notebooks = api.scan_notebooks()
        if len(_notebooks) == 0:
            return False
        notebook_dataframe = self.spark.createDataFrame(_notebooks, ["object_id", "path"])
        if self.serverless:
            notebook_dataframe.writeTo(self.notebook_full_name).createOrReplace()
        else:
            notebook_dataframe.createOrReplaceGlobalTempView(self.notebook_name)
        return True

    def show(self):
        self.spark.sql(f"select * from {self.notebook_full_name}").show()

    def get_by(self, *, notebook_id: str = None, path: str = None):
        if self.spark.catalog.tableExists(self.notebook_full_name):
            if path:
                _any = self.spark.sql(
                    f"select object_id from {self.notebook_full_name} where path LIKE '%{path}%'").first()
                if _any:
                    return _any.object_id
            elif notebook_id:
                _any = self.spark.sql(
                    f"select path from {self.notebook_full_name} where object_id = {notebook_id}").first()
                if _any:
                    return _any.path

            else:
                raise "Either notebook_id or path is required"

        return
