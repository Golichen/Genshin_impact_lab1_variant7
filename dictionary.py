from typing import Any, List, Optional, Callable, Tuple
import warnings


class Node:
    # Represents a node in the hash table (used for separate chaining)
    def __init__(self, key: Any, value: Any, next_: Optional['Node'] = None):
        self.key = key
        self.value = value
        self.next_ = next_


class Dictionary:
    # A dictionary implemented using hash map with separate chaining
    def __init__(self, capacity: int = 10):
        # Validate that capacity is a positive integer
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.capacity = capacity  # The capacity of the hash table
        self.buckets: List[Optional[Node]] = (
            [None] * self.capacity
        )  # The buckets (each bucket is a linked list)
        self._size = 0  # The number of key-value pairs in the dictionary

    def _hash(self, key: Any) -> int:
        # Compute the hash value of the key and map it to a bucket index
        if key is None:
            raise ValueError("None keys are not allowed in this dictionary.")
        try:
            return hash(key) % self.capacity
        except TypeError as e:
            raise TypeError(f"Unhashable type: {type(key)}") from e

    def add(self, key: Any, value: Any) -> None:
        # Insert or update a key-value pair in the dictionary
        if key is None:
            raise ValueError("None keys are not allowed in this dictionary.")
        if value is None:
            raise ValueError("None values are not allowed in this dictionary.")

        index = self._hash(key)
        if self.buckets[index] is None:
            # If the bucket is empty, insert the node directly
            self.buckets[index] = Node(key, value)
            self._size += 1
        else:
            # check if the key already exists
            cur = self.buckets[index]
            while cur is not None:
                if cur.key == key:
                    # If the key exists, update the value
                    cur.value = value
                    return
                if cur.next_ is None:
                    break
                cur = cur.next_
            # Insert a new node at the end of the linked list
            cur.next_ = Node(key, value)
            self._size += 1

    def get(self, key: Any) -> Optional[Any]:
        # Get the value associated with the key
        if key is None:
            return None

        index = self._hash(key)
        cur = self.buckets[index]
        while cur is not None:
            if cur.key == key:
                return cur.value
            cur = cur.next_
        return None

    def remove(self, key: Any) -> None:
        # Remove the key-value pair associated with the key
        if key is None:
            return

        index = self._hash(key)
        cur = self.buckets[index]
        prev = None
        while cur is not None:
            if cur.key == key:
                if prev is None:
                    # If the node is the first node in the linked list
                    self.buckets[index] = cur.next_
                else:
                    # Remove the node in the middle of the linked list
                    prev.next_ = cur.next_
                self._size -= 1
                return
            prev = cur
            cur = cur.next_

    def size(self) -> int:
        # Return the number of key-value pairs in the dictionary
        return self._size

    def member(self, key: Any) -> bool:
        # Check if the dictionary contains the specified key
        return self.get(key) is not None

    def from_list(self, lst: List[Tuple[Any, Any]]) -> None:
        # Build the dictionary from a built-in list of key-value pairs
        for key, value in lst:
            self.add(key, value)

    def to_list(self) -> List[Tuple[Any, Any]]:
        # Convert the dictionary to a built-in list of key-value pairs
        result = []
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                result.append((cur.key, cur.value))
                cur = cur.next_
        return result

    def filter(self, predicate: Callable[[Any, Any], bool]) -> 'Dictionary':
        # Filter the dictionary by a predicate and return a new dictionary
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            if predicate(key, value):
                new_dict.add(key, value)
        return new_dict

    def map(self, function: Callable[[Any], Any]) -> 'Dictionary':
        # Function for each value in the dictionary and return a new dictionary
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            new_dict.add(key, function(value))
        return new_dict

    def reduce(
        self,
        function: Callable[[Any, Any], Any],
        initial_state: Any
    ) -> Any:
        # Reduce the values in the dictionary and return the final result
        state = initial_state
        for _, value in self.to_list():
            state = function(state, value)
        return state

    def __iter__(self):
        # Return an iterator for the dictionary
        self._iter_index = 0
        self._iter_node = self.buckets[0]
        return self

    def __next__(self) -> Tuple[Any, Any]:
        # Return the next key-value pair in the dictionary
        while self._iter_index < self.capacity:
            if self._iter_node is not None:
                key, value = self._iter_node.key, self._iter_node.value
                self._iter_node = self._iter_node.next_
                return key, value
            else:
                self._iter_index += 1
                if self._iter_index < self.capacity:
                    self._iter_node = self.buckets[self._iter_index]
        raise StopIteration

    @staticmethod
    def empty() -> 'Dictionary':
        # Return an empty dictionary
        return Dictionary()

    def concat(self, other: 'Dictionary') -> 'Dictionary':
        # Concatenate two dictionaries and return a new dictionary
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            new_dict.add(key, value)
        for key, value in other.to_list():
            new_dict.add(key, value)
        return new_dict

    def __str__(self) -> str:
        # Return a string representation of the dictionary
        items = self.to_list()
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
