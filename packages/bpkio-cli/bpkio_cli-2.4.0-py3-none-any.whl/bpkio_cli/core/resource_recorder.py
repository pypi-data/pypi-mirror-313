import os
import pickle
import re
from typing import List

from bpkio_cli.core.exceptions import BroadpeakIoCliError, UsageError
from bpkio_cli.core.logging import logger
from pydantic import BaseModel


class ResourceRecorder:
    def __init__(self, fqdn: str, tenant: str | int):
        # temp_dir = tempfile.gettempdir()
        cache_dir = os.path.join(
            os.path.expanduser("~/.bpkio"), "cache", fqdn, str(tenant)
        )

        logger.debug("Cache folder: " + cache_dir)

        self._resources_file = os.path.join(cache_dir, "resources.pkl")
        self._lists_file = os.path.join(cache_dir, "lists.pkl")
        self._metadata_file = os.path.join(cache_dir, "metadata.pkl")

        self._cache_singles: MoveToFrontList = self._read_file_or_new(
            self._resources_file, MoveToFrontList(100)
        )
        self._cache_lists: dict = self._read_file_or_new(self._lists_file, dict())
        self._cache_metadata: dict = self._read_file_or_new(self._metadata_file, dict())

    def _read_file_or_new(self, file_path: str, default):
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                try:
                    content = pickle.load(file)
                    if isinstance(content, default.__class__):
                        return content
                except Exception:
                    logger.warning(
                        "Issue encountered with loading the cache. No cache will be used"
                    )
                    pass

        return default

    def clear(self):
        """Reset the cache"""
        self._cache_singles = MoveToFrontList(maxlen=100)
        self._cache_lists = dict()
        self._cache_metadata = dict()
        self.save()

    def save(self):
        """Save the cache to disk.

        This will overwrite any existing cache.
        """
        try:
            os.makedirs(os.path.dirname(self._resources_file), exist_ok=True)
            with open(
                self._resources_file,
                "wb",
            ) as file:
                pickle.dump(self._cache_singles, file)
        except IOError as e:
            logger.warn("Unable to write Resources file to cache")

        try:
            with open(self._lists_file, "wb") as file:
                pickle.dump(self._cache_lists, file)
        except IOError:
            logger.warn("Unable to write Lists file to cache")

        try:
            with open(self._metadata_file, "wb") as file:
                pickle.dump(self._cache_metadata, file)
        except IOError:
            logger.warn("Unable to write Metadata file to cache")

    def record(self, item):
        """Add something to the cache.

        The correct cache is chosen based on the type of the value to store"""
        if isinstance(item, List) and len(item) > 0:
            self._cache_lists[item[0].__class__.__name__] = item
        else:
            self._cache_singles.add(item)

    def remove(self, item):
        """Remove a value from the cache"""
        self._cache_singles.remove(item)

        # remove it from all lists too
        for list in self._cache_lists.values():
            if item in list:
                list.remove(item)

        # And from metadata
        for k, v in self._cache_metadata.items():
            if v == item:
                del self._cache_metadata[k]

    def remove_by_id(self, id):
        """Remove a value from the cache by its id"""
        item = next(
            (
                v
                for v in self._cache_singles.values()
                if hasattr(v, "id") and v.id == id
            ),
            None,
        )
        if item:
            self.remove(item)

        # and from metadata
        # TODO - fix this - string keys?  ambiguous IDs...
        keys_to_remove = []
        for k, v in self._cache_metadata.items():
            if f".{id})" in k:
                keys_to_remove.append(k)

        for k in keys_to_remove:
            del self._cache_metadata[k]

    def resolve(self, token, target_type):
        """Resolve non-integer references from data in the cache"""
        if token == "$":
            last_id = self.last_id_by_type(target_type)
            if last_id:
                return str(last_id)
            else:
                raise UsageError(
                    "There is no resource in memory that can be found to "
                    "replace '$' for this context. Use an explicit ID"
                )

        if token.startswith("@"):
            match = re.search(r"(-?\d+)", token)
            if match:
                pos = int(match.group(1))
                id = self.id_by_position_in_last_list_by_type(target_type, pos)
                if id:
                    return str(id)
                else:
                    raise UsageError(
                        f"There is no resource in position {pos} "
                        f"in the last list of {target_type.__name__}"
                    )

        return token

    def last_id(self):
        return getattr(self._cache_singles[0], "id", self._cache_singles[0])

    def last_id_by_type(self, type: type):
        candidates = [v for v in self._cache_singles.values() if isinstance(v, type)]
        if len(candidates):
            return getattr(candidates[0], "id", candidates[0])

    def last_by_type(self, type_: type):
        candidates = [v for v in self._cache_singles.values() if isinstance(v, type_)]
        if len(candidates):
            return candidates[0]

    def exists_by_id(self, type_: type, id: int):
        return any(isinstance(v, type_) and v.id == id for v in self._cache_singles)

    def get_by_type_and_id(self, type_: type, id: int):
        return next(
            (v for v in self._cache_singles if isinstance(v, type_) and v.id == id),
            None,
        )

    def id_by_position_in_last_list_by_type(self, type_: type, position: int):
        """Find the id of a resource in a list of resources of a specific type.

        The list of resources is found by looking at the cache, and the position
        is found by looking at the last list of resources of that type.

        If the list is empty, or the position is out of bounds, None is returned.
        """
        if type_.__name__ in self._cache_lists:
            # Try strict type first:
            list = self._cache_lists[type_.__name__]
        else:
            try:
                # Otherwise, find first list that contains super-types
                list = next(
                    l for l in self._cache_lists.values() if isinstance(l[0], type_)
                )
            except StopIteration:
                raise RecorderCacheError(
                    f"There is no list of resources of type {type_.__name__} in cache."
                )

        try:
            return list[position].id
        except IndexError:
            raise RecorderCacheError(
                f"The list of resources of type {type_.__name__} currently "
                f"in cache only contains {len(list)} resources"
            )

    def list_resources(self, models_only=False):
        """Return a list of all resources in the cache"""
        resources = self._cache_singles.values()
        if models_only:
            resources = [r for r in resources if isinstance(r, BaseModel)]
        return resources

    def list_resources_by_type(self, type):
        """Return a list of all resources of a specific type in the cache"""
        return [r for r in self._cache_singles.values() if isinstance(r, type)]

    def list_lists(self):
        """Return a list of all lists in the cache"""
        return self._cache_lists

    def _make_key(self, item):
        if hasattr(item, "summary"):
            return item.summary
        else:
            return str(item)

    def record_metadata(self, item, key, value):
        """Records metadata against an item"""
        item_key = self._make_key(item)
        if item_key not in self._cache_metadata:
            self._cache_metadata[item_key] = dict()

        if key not in self._cache_metadata[item_key]:
            self._cache_metadata[item_key][key] = MoveToFrontList(maxlen=50)

        self._cache_metadata[item_key][key].add(value)

    def get_metadata(self, item, key):
        """Returns the metadata for an item"""
        item_key = self._make_key(item)
        if item_key in self._cache_metadata:
            lst: MoveToFrontList = self._cache_metadata[item_key].get(key)
            if lst:
                return lst.values()
        return None

    def remove_metadata(self, item, key, value):
        """Removes metadata for an item"""
        item_key = self._make_key(item)
        if item_key in self._cache_metadata:
            lst: MoveToFrontList = self._cache_metadata[item_key].get(key)
            if lst:
                lst.remove(value)
                self._cache_metadata[item_key][key] = lst
                return lst
        return None

    def list_metadata(self):
        """Return a list of all metadata in the cache"""
        return self._cache_metadata

    def sort_resources_by_most_recently_accessed(self, original_list):
        """Sort a list of resources by placing the most recently accessed first,
        as recorded in the cache"""

        accessed_resources = self.list_resources()
        order_dict = {
            getattr(item, "summary", str(item)): i
            for i, item in enumerate(accessed_resources)
        }

        # Create a key function for the sorted() function
        # If the object is in access_order, its sort key is its position,
        # otherwise it's the length of access_order (which puts it at the end)
        key_func = lambda obj: order_dict.get(obj.summary, len(accessed_resources))

        # Sort the list
        sorted_main_list = sorted(original_list, key=key_func)

        return sorted_main_list


class MoveToFrontList:
    def __init__(self, maxlen: int = None):
        self._list = []
        self._maxlen = maxlen

    def add(self, item, id_field="id"):
        if item in self._list:
            self._list.remove(item)
        # next try and find it by type and id
        for i, v in enumerate(self._list):
            if (
                isinstance(v, type(item))
                and hasattr(v, id_field)
                and getattr(v, id_field) == getattr(item, id_field)
            ):
                self._list.pop(i)

        self._list.insert(0, item)

        if self._maxlen is not None and len(self._list) > self._maxlen:
            self._list.pop()

    def remove(self, item):
        if item in self._list:
            self._list.remove(item)

    # def search(self, item):
    #     if item in self._list:
    #         self._list.remove(item)
    #         self._list.insert(0, item)
    #         return True
    #     return False

    def values(self):
        return self._list

    def __str__(self):
        return str(self._list)

    def __getitem__(self, key):
        return self._list[key]

    def __setitem__(self, key, value):
        self._list[key] = value

    def __delitem__(self, key):
        del self._list[key]

    def __repr__(self) -> str:
        return str(self._list)


class RecorderCacheError(BroadpeakIoCliError):
    def __init__(self, message):
        super().__init__(message)
