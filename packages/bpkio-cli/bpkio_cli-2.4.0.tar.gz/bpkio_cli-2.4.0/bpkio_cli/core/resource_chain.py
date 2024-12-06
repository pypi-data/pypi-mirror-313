from typing import List, Tuple


class ResourceChain:
    """Implements a sort of breadcrumbs storage, for multi-level resources"""

    def __init__(self) -> None:
        self._chain: List[str | int, object] = []

    # TODO - this needs to be moved to a separate object,
    # directly linked to the ResourceGroup
    def add_resource(self, key, resource=None):
        """Records a resource, against a key (usually the identifier of the resource)"""
        self._chain.append((key, resource))

    def extract_resource(self, *, pos: int = -1) -> Tuple:
        try:
            return self._chain[pos]
        except IndexError:
            return (None, None)

    def last(self) -> int | None:
        return self.extract_resource(pos=-1)

    def last_key(self) -> str | None:
        return self.last()[0]

    def parent(self) -> int | None:
        return self.extract_resource(pos=-2)

    def overwrite_last(self, key, resource):
        self._chain[-1] = (key, resource)


class UnknownResourceError(ValueError):
    def __init__(self, message):
        super().__init__(message)
