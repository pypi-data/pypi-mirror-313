import json

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import TableInfo
from syntax.js import Array


class Table:
    """
    NOTE: table create is not supported by SDK. Use dataframe instead.
    """
    def __init__(self, client: WorkspaceClient):
        self.client = client

    def get(self, full_name: str):
        return Table.pretty(self._get(full_name))

    def columns(self, full_name: str):
        return Array(self._get(full_name).columns).map(lambda column: column.name)

    def _get(self, full_name: str) -> TableInfo:
        return self.client.tables.get(full_name)

    def list(self, catalog_name: str, schema_name: str):
        return self.client.tables.list(catalog_name, schema_name)

    @staticmethod
    def columns_of(table: TableInfo):
        return Array(table.columns).map(lambda column: {
            'name': column.name,
            'nullable': column.nullable,
            'type': json.loads(column.type_json)['type']
        })

    @staticmethod
    def pretty(table: TableInfo):
        d = table.as_dict()
        return {
            'catalog_name': d['catalog_name'],
            'columns': Table.columns_of(table),
            'comment': d['comment'],
            "data_source_format": d['data_source_format'],
            'name': d['name'],
            'schema_name': d['schema_name'],
            'id': d['table_id'],
        }
