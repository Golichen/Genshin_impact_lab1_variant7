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
    assert sorted(dictionary.to_list(), key=lambda x: str(x[0])) == [("age", 25), ("name", "Alice")]


def test_filter():
    """测试过滤字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25), ("height", 170)])
    filtered_dict = dictionary.filter(lambda k, v: isinstance(v, int))  # 过滤值为整数的键值对
    assert sorted(filtered_dict.to_list(), key=lambda x: str(x[0])) == [("age", 25), ("height", 170)]


def test_map():
    """测试映射字典功能"""
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])
    mapped_dict = dictionary.map(lambda v: v.upper() if isinstance(v, str) else v)  # 对字符串值转换为大写
    assert sorted(mapped_dict.to_list(), key=lambda x: str(x[0])) == [("age", 25), ("name", "ALICE")]


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
    assert sorted(items, key=lambda x: str(x[0])) == [("age", 25), ("name", "Alice")]


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
    assert sorted(combined_dict.to_list(), key=lambda x: str(x[0])) == [("age", 25), ("name", "Alice")]


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
    assert sorted(result, key=lambda x: str(x[0])) == sorted(expected, key=lambda x: str(x[0]))
