from collections import defaultdict


class NestedMap(defaultdict):
    def __init__(self):
        super().__init__(lambda: NestedMap())

    def set_value(self, keys: list[str], value):
        """
        Sets the value for the nested keys provided.
        keys: list[str] of keys representing the path to the target.
        value: The value to set at the target.
        """
        target = self
        for key in keys[:-1]:  # Traverse to the second last key
            target = target[key]
        if keys[-1] in target and not isinstance(target[keys[-1]], defaultdict):
            raise ValueError(f"Duplicate found: {keys[-1]}")
        target[keys[-1]] = value  # Set the value for the last key. it cannot be *

    def get_values(self, keys: list[str]):
        """
        Retrieves values matching the exact keys or wildcards stored in the data.
        keys: list[str] representing the path for lookup.
        """
        results = []
        self._retrieve_values(self, keys, 0, results)

        return results

    def _retrieve_values(self, current, keys: list[str], index: int, results: list):
        """
        Helper method to recursively retrieve values, considering wildcards in data.
        current: The current level in the nested dictionary.
        keys: A list of keys representing the path for lookup.
        index: The current index in the list of keys.
        results: The list of values that match the path (intentionally mutable).
        """
        if index == len(keys):  # Base case: all keys have been processed
            if not isinstance(current, defaultdict):  # If current is a value, not a dict
                results.append(current)  # results is mutated
            else:  # Collect values from all sub-trees
                for key in current:
                    self._retrieve_values(current[key], keys, index, results)
            return

        key = keys[index]
        # Check for exact match or wildcard in current level
        if key in current:
            self._retrieve_values(current[key], keys, index + 1, results)
        if "*" in current:  # Check if there's a wildcard path
            self._retrieve_values(current["*"], keys, index + 1, results)
