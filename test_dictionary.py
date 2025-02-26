from typing import Any
from dictionary import Dictionary
import warnings


def test_add():
    """测试插入键值对功能"""
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.get("name") == "Alice"
    dictionary.add("age", 25)
    assert dictionary.get("age") == 25


def test_get():
    """测试获取值功能"""
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("nonexistent") is None


def test_remove():
    """测试删除键值对功能"""
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)
    dictionary.remove("name")
    assert dictionary.get("name") is None
    assert dictionary.get("age") == 25


def test_size():
    """测试字典大小功能"""
    dictionary = Dictionary()
    assert dictionary.size() == 0
    dictionary.add("name", "Alice")
    assert dictionary.size() == 1
    dictionary.add("age", 25)
    assert dictionary.size() == 2
    dictionary.remove("name")
    assert dictionary.size() == 1


def test_member():
    """测试检查键是否存在功能"""
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.member("name") is True
    assert dictionary.member("nonexistent") is False


def test_from_list():
    """测试从列表构建字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("age") == 25


def test_to_list():
    """测试将字典转换为列表功能"""
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)

    # 获取排序后的键值对列表
    result = sorted(dictionary.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    # 断言结果与预期一致
    assert result == expected


def test_filter():
    """测试过滤字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25), ("height", 170)])
    filtered_dict = dictionary.filter(
        lambda k,
        v: isinstance(v, int)
    )  # 过滤值为整数的键值对

    result = sorted(filtered_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("height", 170)]

    assert result == expected


def test_map():
    """测试映射字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])

    # 定义映射函数
    def map_function(value: Any) -> Any:
        return value.upper() if isinstance(value, str) else value

    # 对字典中的每个值应用映射函数
    mapped_dict = dictionary.map(map_function)

    result = sorted(mapped_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "ALICE")]

    assert result == expected


def test_reduce():
    """测试归约字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("a", 1), ("b", 2), ("c", 3)])
    result = dictionary.reduce(lambda acc, v: acc + v, 0)  # 求和
    assert result == 6


def test_iter():
    """测试字典的迭代功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])
    items = list(iter(dictionary))

    result = sorted(items, key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    assert result == expected


def test_empty():
    """测试空字典功能"""
    dictionary = Dictionary.empty()
    assert dictionary.size() == 0
    assert dictionary.to_list() == []


def test_concat():
    """测试连接两个字典功能"""
    dictionary1 = Dictionary()
    dictionary1.from_list([("name", "Alice")])
    dictionary2 = Dictionary()
    dictionary2.from_list([("age", 25)])
    combined_dict = dictionary1.concat(dictionary2)

    result = sorted(combined_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    assert result == expected


def test_monoid_properties():
    # 单位元测试
    empty_dict = Dictionary.empty()
    dict1 = Dictionary()
    dict1.add("a", 1)
    dict1.add("b", 2)

    # 单位元性质
    assert dict1.concat(empty_dict).to_list() == dict1.to_list()
    assert empty_dict.concat(dict1).to_list() == dict1.to_list()

    # 结合律测试
    dict2 = Dictionary()
    dict2.add("c", 3)
    dict3 = Dictionary()
    dict3.add("d", 4)

    # 结合律性质
    left = dict1.concat(dict2).concat(dict3)
    right = dict1.concat(dict2.concat(dict3))
    assert left.to_list() == right.to_list()


def test_none_values():
    dictionary = Dictionary()

    # 测试 None 键
    try:
        dictionary.add(None, "value")
    except ValueError as e:
        assert str(e) == "None keys are not allowed in this dictionary."

    # 测试 None 值
    try:
        dictionary.add("key", None)
    except ValueError as e:
        assert str(e) == "None values are not allowed in this dictionary."


def test_mixed_types():
    dictionary = Dictionary()

    # 插入不同类型的键值对
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)
    dictionary.add(42, "answer")

    # 检查值
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("age") == 25
    assert dictionary.get(42) == "answer"

    # 转换为列表并排序
    result = dictionary.to_list()
    expected = [("name", "Alice"), ("age", 25), (42, "answer")]

    sorted_result = sorted(result, key=lambda x: str(x[0]))
    sorted_expected = sorted(expected, key=lambda x: str(x[0]))

    assert sorted_result == sorted_expected
