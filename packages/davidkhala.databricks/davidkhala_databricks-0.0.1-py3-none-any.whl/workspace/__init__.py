import pathlib

from databricks.sdk import WorkspaceClient
from databricks.sdk.config import Config

from common import CONFIG_PATH


class Workspace:

    def __init__(self, client: WorkspaceClient = None):
        if not pathlib.Path(CONFIG_PATH).exists():
            raise FileNotFoundError(CONFIG_PATH + " does not exist")
        if client is None:
            client = WorkspaceClient()
        self.client = client

    def clusters(self):
        return list(self.client.clusters.list())

    @property
    def config(self) -> Config:
        """
        It returns raw token content. TAKE CARE for secret leakage.
        :return: {'host':'https://adb-662901427557763.3.azuredatabricks.net', 'token':'', 'auth_type':'pat'}
        """
        return self.client.config

    @property
    def config_token(self):
        return self.config.as_dict().get('token')

    @property
    def catalog(self) -> str:
        """
        :return: default catalog name
        """
        return self.client.settings.default_namespace.get().namespace.value

    @property
    def cloud(self):
        token: str = self.config.token
        if token is not None:

            if token.startswith('https://adb-') and token.endswith('.azuredatabricks.net'):
                # adb-662901427557763.3.azuredatabricks.net
                return 'azure'
            elif token.startswith('https://dbc-') and token.endswith('.cloud.databricks.com'):
                # dbc-8df7b30e-676a.cloud.databricks.com
                return "aws"
            elif token.endswith('.gcp.databricks.com'):
                # 1105010096141051.1.gcp.databricks.com
                return "gcp"

    @property
    def metastore(self):
        """
        :return: current metastore
        """
        return self.client.metastores.current()

    @property
    def dbutils(self):
        return self.client.dbutils

    @property
    def api_client(self):
        return APIClient(self.client)


class APIClient:
    api_version = '/api/2.0'

    def __init__(self, client: WorkspaceClient):
        self.client = client.api_client

    def get(self, route, data=None):
        return self.client.do(method='GET', path=self.api_version + route, body=data)
