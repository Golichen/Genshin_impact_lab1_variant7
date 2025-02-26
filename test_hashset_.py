import hypothesis.strategies as st
import pytest
from hypothesis import given
from hashset import HashSet
import warnings


def test_add():
    # 测试添加元素功能
    hash_set = HashSet()
    hash_set.add(1)
    assert hash_set.member(1) is True
    hash_set.add(2)
    assert hash_set.member(2) is True


def test_remove():
    # 测试移除元素功能
    hash_set = HashSet()
    hash_set.add(1)
    hash_set.add(2)
    hash_set.remove(1)
    assert hash_set.member(1) is False
    assert hash_set.member(2) is True


def test_member():
    # 测试检查元素是否存在功能
    hash_set = HashSet()
    hash_set.add(1)
    assert hash_set.member(1) is True
    assert hash_set.member(2) is False


def test_size():
    # 测试集合大小功能
    hash_set = HashSet()
    assert hash_set.size() == 0
    hash_set.add(1)
    assert hash_set.size() == 1
    hash_set.add(2)
    assert hash_set.size() == 2
    hash_set.remove(1)
    assert hash_set.size() == 1


def test_from_list():
    # 测试从列表构建集合功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3])
    assert hash_set.member(1) is True
    assert hash_set.member(2) is True
    assert hash_set.member(3) is True
    assert hash_set.member(4) is False


def test_to_list():
    # 测试集合转换为列表功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3])
    assert sorted(hash_set.to_list()) == [1, 2, 3]


def test_filter():
    # 测试过滤功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3, 4, 5])
    filtered_set = hash_set.filter(lambda x: x % 2 == 0)
    assert sorted(filtered_set.to_list()) == [2, 4]


def test_map():
    # 测试映射功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3])
    mapped_set = hash_set.map(lambda x: x * 2)
    assert sorted(mapped_set.to_list()) == [2, 4, 6]


def test_reduce():
    # 测试归约功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3])
    result = hash_set.reduce(lambda acc, x: acc + x, 0)
    assert result == 6


def test_iter():
    # 测试迭代功能
    hash_set = HashSet()
    hash_set.from_list([1, 2, 3])
    elements = []
    for value in hash_set:
        elements.append(value)
    assert sorted(elements) == [1, 2, 3]

    # 测试空集合的迭代
    empty_set = HashSet()
    i = iter(empty_set)
    with pytest.raises(StopIteration):
        next(i)


def test_empty():
    # 测试空集合功能
    hash_set = HashSet.empty()
    assert hash_set.size() == 0
    assert hash_set.to_list() == []


def test_concat():
    # 测试连接两个集合功能
    hash_set1 = HashSet()
    hash_set1.from_list([1, 2, 3])
    hash_set2 = HashSet()
    hash_set2.from_list([3, 4, 5])
    concatenated_set = hash_set1.concat(hash_set2)
    assert sorted(concatenated_set.to_list()) == [1, 2, 3, 4, 5]


@given(st.lists(st.integers()))
# Generate lists of random integers
def test_from_list_to_list_equality(lst):
    # 测试 from_list 和 to_list 的等价性。
    hash_set = HashSet()
    hash_set.from_list(lst)
    # 集合会去重，因此与 set(lst) 的结果一致
    assert sorted(hash_set.to_list()) == sorted(set(lst))


@given(st.lists(st.integers()))
def test_python_set_and_hashset_equality(lst):
    # 测试 HashSet 和 Python 内置集合的行为一致性
    hash_set = HashSet()
    hash_set.from_list(lst)
    python_set = set(lst)
    assert sorted(hash_set.to_list()) == sorted(python_set)


@given(st.lists(st.integers()))
def test_size_after_operations(lst):
    # 测试在添加和移除操作后集合的大小是否正确
    hash_set = HashSet()
    for value in lst:
        hash_set.add(value)
    assert hash_set.size() == len(set(lst))
    for value in lst:
        hash_set.remove(value)
    assert hash_set.size() == 0


def test_monoid():
    # test for Monoid law
    hash_set1 = HashSet()
    hash_set1.from_list([1,2,3])

    hash_set2 = HashSet()
    hash_set2.from_list([3,4,5])

    hash_set3 = HashSet()
    hash_set3.from_list([5,6,7])

    # 验证结合律
    left = (hash_set1.concat(hash_set2)).concat(hash_set3)
    right = hash_set1.concat(hash_set2.concat(hash_set3))
    assert left.to_list() == right.to_list()

    # 验证单位元
    empty_set = HashSet.empty()
    assert hash_set1.concat(empty_set).to_list() == hash_set1.to_list()
    assert empty_set.concat(hash_set1).to_list() == hash_set1.to_list()


def test_none_value():
    try:
        hash_set = HashSet(None)
    except ValueError as e:
        assert str(e) == "Capacity must be a positive integer."


def test_different_types():
    hash_set = HashSet()
    hash_set.add(42)  # 添加整数

    # 添加不同类型的元素（字符串），发出警告
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # 捕获所有警告
        hash_set.add("hello")
        assert len(w) == 1  # 确保捕获到一个警告
        assert issubclass(w[-1].category, UserWarning)
        assert "Mixed types" in str(w[-1].message)

    # 检查元素是否存在
    assert hash_set.member("hello") is True
