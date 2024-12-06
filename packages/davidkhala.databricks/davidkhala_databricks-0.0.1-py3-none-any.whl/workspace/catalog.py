from workspace import Workspace


class Catalog:
    def __init__(self, w: Workspace):
        self.w: Workspace = w

    @property
    def catalogs(self):
        return self.w.client.catalogs

    def create(self, name, *, withMetastoreLevelStorage=False, storage_root=None):
        if withMetastoreLevelStorage:
            return self.catalogs.create(name)
        else:
            if storage_root is None:
                storage_root = self.get().storage_root
            return self.catalogs.create(name, storage_root=storage_root)

    def get(self, name=None):
        if name is None:
            name = self.w.catalog
        return self.catalogs.get(name)

    def delete(self, name):
        return self.catalogs.delete(name, force=True)
