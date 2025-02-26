from typing import Any, List, Optional, Callable, Tuple


class Node:
    """表示哈希表中的节点（用于分离链接法）"""

    def __init__(self, key: Any, value: Any, next_: Optional['Node'] = None):
        self.key = key
        self.value = value
        self.next_ = next_


class Dictionary:
    """基于哈希映射和分离链接法实现的字典"""

    def __init__(self, capacity: int = 10):
        # 验证 capacity 是否为整数且大于 0
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.capacity = capacity  # 哈希表的容量
        self.buckets: List[Optional[Node]] = (
            [None] * self.capacity
        )  # 桶（buckets）
        self._size = 0  # 字典中键值对的数量

    def _hash(self, key: Any) -> int:
        """计算键的哈希值，并映射到桶的索引"""
        if key is None:
            raise ValueError("None keys are not allowed in this dictionary.")
        try:
            return hash(key) % self.capacity
        except TypeError as e:
            raise TypeError(f"Unhashable type: {type(key)}") from e

    def add(self, key: Any, value: Any) -> None:
        """向字典中插入或更新键值对"""
        if key is None:
            raise ValueError("None keys are not allowed in this dictionary.")
        if value is None:
            raise ValueError("None values are not allowed in this dictionary.")

        index = self._hash(key)
        if self.buckets[index] is None:
            # 如果桶为空，直接插入节点
            self.buckets[index] = Node(key, value)
            self._size += 1
        else:
            # 否则，遍历链表，检查是否已存在相同的键
            cur = self.buckets[index]
            while cur is not None:
                if cur.key == key:
                    # 如果键已存在，更新值
                    cur.value = value
                    return
                if cur.next_ is None:
                    cur.next_ = Node(key, value)
                    self._size += 1
                cur = cur.next_


    def get(self, key: Any) -> Optional[Any]:
        """根据键获取值，如果键不存在则返回 None"""
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
        """根据键删除键值对"""
        if key is None:
            return

        index = self._hash(key)
        cur = self.buckets[index]
        prev = None
        while cur is not None:
            if cur.key == key:
                if prev is None:
                    # 如果要删除的是链表的第一个节点
                    self.buckets[index] = cur.next_
                else:
                    # 删除链表中间的节点
                    prev.next_ = cur.next_
                self._size -= 1
                return
            prev = cur
            cur = cur.next_

    def size(self) -> int:
        """返回字典中键值对的数量"""
        return self._size

    def member(self, key: Any) -> bool:
        """检查字典中是否包含指定的键"""
        return self.get(key) is not None

    def from_list(self, lst: List[Tuple[Any, Any]]) -> None:
        """从内置列表构建字典"""
        for key, value in lst:
            self.add(key, value)

    def to_list(self) -> List[Tuple[Any, Any]]:
        """将字典转换为内置列表"""
        result = []
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                result.append((cur.key, cur.value))
                cur = cur.next_
        return result

    def filter(self, predicate: Callable[[Any, Any], bool]) -> 'Dictionary':
        """过滤字典中的键值对，返回满足谓词的新字典"""
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            if predicate(key, value):
                new_dict.add(key, value)
        return new_dict

    def map(self, function: Callable[[Any], Any]) -> 'Dictionary':
        """对字典中的每个值应用函数，返回新字典"""
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            new_dict.add(key, function(value))
        return new_dict

    def reduce(
        self,
        function: Callable[[Any, Any], Any],
        initial_state: Any
    ) -> Any:
        """归约字典中的值，返回最终结果"""
        state = initial_state
        for _, value in self.to_list():
            state = function(state, value)
        return state

    def __iter__(self):
        """返回字典的迭代器"""
        self._iter_index = 0
        self._iter_node = self.buckets[0]
        return self

    def __next__(self) -> Tuple[Any, Any]:
        """返回字典的下一个键值对"""
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
        """返回一个空字典"""
        return Dictionary()

    def concat(self, other: 'Dictionary') -> 'Dictionary':
        """连接两个字典，返回新字典"""
        new_dict = Dictionary(self.capacity)
        for key, value in self.to_list():
            new_dict.add(key, value)
        for key, value in other.to_list():
            new_dict.add(key, value)
        return new_dict

    def __str__(self) -> str:
        """返回字典的字符串表示"""
        items = self.to_list()
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
