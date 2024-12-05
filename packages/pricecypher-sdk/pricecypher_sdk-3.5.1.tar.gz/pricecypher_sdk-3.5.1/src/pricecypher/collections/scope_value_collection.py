from pricecypher.models import ScopeValue
from .base_collection import Collection


class ScopeValueCollection(Collection[ScopeValue]):
    def where_in(self, values):
        """
        Filter collection on the given values.

        :param list or float or str values: Value or values to filter the collection on.
        :return: Collection of filtered scope values.
        :rtype: ScopeValueCollection
        """
        # Turn values into a list if it is not a list already.
        if type(values) is not list:
            values = [values]

        # Make sure all values are strings.
        values = list(map(str, values))
        # Filter and create new collection
        scope_values = [sv for sv in self._list if sv.value in values]
        return ScopeValueCollection(scope_values)
