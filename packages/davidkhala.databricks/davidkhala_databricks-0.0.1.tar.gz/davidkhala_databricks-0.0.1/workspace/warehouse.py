from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState, StatementResponse


class Warehouse:
    def __init__(self, client: WorkspaceClient, http_path: str):
        """
        :param client:
        :param http_path: e.g. '/sql/1.0/warehouses/7969d92540da7f02'
        """
        self.client = client
        self.warehouse_id = http_path.split('/')[-1]

    def run_async(self, query: str):
        return self.client.statement_execution.execute_statement(query, self.warehouse_id)

    def run(self, query: str):
        r = self.run_async(query)
        return Warehouse.pretty(self.wait_until_statement_success(r))

    def wait_until_statement_success(self, r: StatementResponse):
        if r.status.state == StatementState.PENDING:
            next_response = self.client.statement_execution.get_statement(r.statement_id)
            return self.wait_until_statement_success(next_response)
        assert r.status.state == StatementState.SUCCEEDED
        return r

    def activate(self):
        return self.client.warehouses.start_and_wait(self.warehouse_id)

    def stop(self):
        return self.client.warehouses.stop_and_wait(self.warehouse_id)

    @staticmethod
    def pretty(r: StatementResponse):
        return {
            'schema': r.manifest.schema.as_dict().get('columns'),
            'data': r.result.as_dict().get('data_array'),
        }
