from pricecypher.models import Scope
from .base_collection import Collection


class ScopeCollection(Collection[Scope]):
    def find_by_id(self, scope_id):
        return next((s for s in self._list if s.id == scope_id), None)

    def find_by_repr(self, representation):
        return next((s for s in self._list if s.representation == representation), None)

    def find_by_name_dataset(self, name_dataset):
        return next((s for s in self._list if s.name_dataset == name_dataset), None)

    def where_type(self, typ):
        return self.where('type', typ)

    def where_multiply_by_volume_enabled(self, enabled=True):
        return self.where('multiply_by_volume_enabled', enabled)
