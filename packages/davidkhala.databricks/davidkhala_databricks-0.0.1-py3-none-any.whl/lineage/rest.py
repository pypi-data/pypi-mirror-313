from workspace import APIClient


class API:
    def __init__(self, client: APIClient):
        self.client = client

    def get_table(self, table_name):
        """
        function to get lineage of unity catalog tables
        :param table_name:
        :return:
        """
        return self.client.get('/lineage-tracking/table-lineage', {
            "table_name": table_name, "include_entity_lineage": True
        })

    def get_column(self, table_name, column_name):
        return self.client.get('/lineage-tracking/column-lineage', {
            'table_name': table_name, "column_name": column_name
        })
