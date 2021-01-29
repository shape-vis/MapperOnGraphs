from typing import Iterable


class DisjointSet:
    """class that holds a disjoint set"""

    def __init__(self, items = [], key=(lambda x: x)):
        self._data = dict()
        self._key_func = key
        for item in items:
            self._data[self._key_func(item)] = item
        self._num_sets = len(self._data)

    def contains(self, item) -> bool:
        return self._key_func(item) in self._data

    def put(self, item):
        self._data[self._key_func(item)] = item
        self._num_sets = self._num_sets+1

    def find(self, item):
        key = self._key_func(item)
        if key not in self._data:
            self._data[key] = item
        elif item != self._data[key]:
            self._data[key] = self.find(self._data[key])
        return self._data[key]

    def findKey(self, key):
        if key not in self._data:
            print("ERROR")
            return
        return self.find(self._data[key])


    def union(self, old_parent, new_parent) -> None:
        parent0, parent1 = self.find(old_parent), self.find(new_parent)
        if not parent0 == parent1:
            self._data[self._key_func(parent0)] = parent1
            self._num_sets = self._num_sets-1
        return parent1


    def unionKey(self, old_parent_key, new_parent_key) -> None:
        parent0, parent1 = self.findKey(old_parent_key), self.findKey(new_parent_key)
        if not parent0 == parent1:
            self._data[self._key_func(parent0)] = parent1
            self._num_sets = self._num_sets-1
        return parent1

    def set_count(self):
        return self._num_sets
