import warnings
from typing import Any, List, Optional, Callable, Type


class Node:
    # 表示哈希表中的节点（用于分离链接法）

    def __init__(self, value: Any, next_: Optional['Node'] = None):
        self.value = value
        self.next_ = next_


class HashSet:
    # 基于哈希映射和分离链接法实现的集合。

    def __init__(self, capacity: int = 10):
        # 验证 capacity 是否为整数且大于 0
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.capacity = capacity  # 哈希表的容量
        self.buckets: List[Optional[Node]] = [None] * self.capacity  # 桶（buckets）
        self._size = 0  # number of the elements
        self._element_type: Optional[Type] = None  # 记录第一个元素的类型

    def _hash(self, value: Any) -> int:
        # 计算值的哈希值，并映射到桶的索引
        try:
            return hash(value) % self.capacity
        except TypeError as e:
            raise TypeError(f"Unhashable type: {type(value)}") from e

    def add(self, value: Any) -> None:
        # 向集合中添加一个值
        if value is None:
            raise ValueError("None values are not allowed in this set.")

        # 检查类型一致性
        if self._element_type is None:
            # 如果集合为空，记录第一个元素的类型
            self._element_type = type(value)
        elif not isinstance(value, self._element_type):
            # 如果类型不一致，发出警告
            warnings.warn(
                f"Adding element of type {type(value)} to a HashSet "
                f"containing {self._element_type}. "
                "Mixed types may cause unexpected behavior.",
                UserWarning,
                )

        try:
            index = self._hash(value)  #try to take hash function
        except TypeError as e:
            raise TypeError(f"Cannot add element of type {type(value)}: {e}")
        if self.buckets[index] is None:
            # 如果桶为空，直接插入节点
            self.buckets[index] = Node(value)
            self._size += 1
        else:
            # 否则，遍历链表，检查是否已存在
            cur = self.buckets[index]
            while cur is not None:
                if cur.value == value:
                    return  # 值已存在，无需添加
                if cur.next_ is None:
                    break
                cur = cur.next_
            # 在链表末尾插入新节点
            cur.next_ = Node(value)
            self._size += 1

    def remove(self, value: Any) -> None:
        #从集合中移除一个值
        if value is None:
            return

        index = self._hash(value)
        cur = self.buckets[index]
        prev = None
        while cur is not None:
            if cur.value == value:
                if prev is None:
                    # 如果要移除的是链表的第一个节点
                    self.buckets[index] = cur.next_
                else:
                    # 移除链表中间的节点
                    prev.next_ = cur.next_
                self._size -= 1
                return
            prev = cur
            cur = cur.next_

    def size(self) -> int:
        # 返回集合中元素的数量
        return self._size

    def member(self, value: Any) -> bool:
        # 检查集合中是否包含某个值
        if value is None:
            return False

        index = self._hash(value)
        cur = self.buckets[index]
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next_
        return False

    def from_list(self, lst: List[Any]) -> None:
        # 从内置列表构建集合
        for value in lst:
            self.add(value)

    def to_list(self) -> List[Any]:
        # 将集合转换为内置列表
        result = []
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                result.append(cur.value)
                cur = cur.next_
        return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'HashSet':
        # 过滤集合中的元素，返回满足谓词的新集合
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                if predicate(cur.value):
                    new_set.add(cur.value)
                cur = cur.next_
        return new_set

    def map(self, function: Callable[[Any], Any]) -> 'HashSet':
        # 对集合中的每个元素应用函数，返回新集合
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                new_set.add(function(cur.value))
                cur = cur.next_
        return new_set

    def reduce(self, function: Callable[[Any, Any], Any], initial_state: Any) -> Any:
        # 归约集合中的元素，返回最终结果
        state = initial_state
        for bucket in self.buckets:
            cur = bucket
            while cur is not None:
                state = function(state, cur.value)
                cur = cur.next_
        return state

    def __iter__(self):
        # 返回集合的迭代器
        self._iter_index = 0
        self._iter_node = self.buckets[0]
        return self

    def __next__(self) -> Any:
        # 返回集合的下一个值
        while self._iter_index < self.capacity:
            if self._iter_node is not None:
                value = self._iter_node.value
                self._iter_node = self._iter_node.next_
                return value
            else:
                self._iter_index += 1
                if self._iter_index < self.capacity:
                    self._iter_node = self.buckets[self._iter_index]
        raise StopIteration

    @staticmethod
    def empty() -> 'HashSet':
        # 返回一个空集合
        return HashSet()

    def concat(self, other: 'HashSet') -> 'HashSet':
        # 连接两个集合，返回新集合
        new_set = HashSet(self.capacity)
        for value in self.to_list():
            new_set.add(value)
        for value in other.to_list():
            new_set.add(value)
        return new_set

    def __str__(self) -> str:
        # 返回集合的字符串表示
        return "{" + ", ".join(map(str, self.to_list())) + "}"
