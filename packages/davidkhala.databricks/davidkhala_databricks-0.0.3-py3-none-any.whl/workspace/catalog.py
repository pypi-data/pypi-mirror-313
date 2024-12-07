from databricks.sdk.errors import platform

from workspace import Workspace


class Catalog:
    def __init__(self, w: Workspace):
        self.w: Workspace = w

    @property
    def catalogs(self):
        return self.w.client.catalogs

    def create(self, name, *, withMetastoreLevelStorage=False, storage_root=None, if_not_exists=True):

        if if_not_exists and self.get(name) is not None:
            return

        if withMetastoreLevelStorage:
            return self.catalogs.create(name)
        else:
            if storage_root is None:
                storage_root = self.get().storage_root
            return self.catalogs.create(name, storage_root=storage_root)

    def get(self, name=None):
        if name is None:
            name = self.w.catalog
        try:
            return self.catalogs.get(name)
        except platform.NotFound as e:
            if str(e) == f"Catalog '{name}' does not exist.":
                return None
            else:
                raise e

    def delete(self, name):
        return self.catalogs.delete(name, force=True)


class Schema:
    def __init__(self, w: Workspace, catalog: str = None):
        self.w: Workspace = w
        if not catalog:
            catalog = self.w.catalog
        self.catalog = catalog

    @property
    def schemas(self):
        return self.w.client.schemas

    def get(self, name='default'):
        return self.schemas.get(f"{self.catalog}.{name}")

    def create(self, name, if_not_exists=True):
        if if_not_exists and self.get(name) is not None:
            return
        return self.schemas.create(name, self.catalog)

    def delete(self, name):
        return self.schemas.delete(f"{self.catalog}.{name}", force=True)
