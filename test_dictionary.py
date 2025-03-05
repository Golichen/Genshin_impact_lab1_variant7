from typing import Any
from dictionary import Dictionary


def test_add():
    # Test adding key-value pairs
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.get("name") == "Alice"
    dictionary.add("age", 25)
    assert dictionary.get("age") == 25


def test_get():
    # Test getting values by key
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("nonexistent") is None


def test_remove():
    # Test removing key-value pairs
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)
    dictionary.remove("name")
    assert dictionary.get("name") is None
    assert dictionary.get("age") == 25


def test_size():
    # Test the size of the dictionary
    dictionary = Dictionary()
    assert dictionary.size() == 0
    dictionary.add("name", "Alice")
    assert dictionary.size() == 1
    dictionary.add("age", 25)
    assert dictionary.size() == 2
    dictionary.remove("name")
    assert dictionary.size() == 1


def test_member():
    # Test checking if a key exists
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    assert dictionary.member("name") is True
    assert dictionary.member("nonexistent") is False


def test_from_list():
    # Test building dictionary from a list
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("age") == 25


def test_to_list():
    # Test converting dictionary to a list
    dictionary = Dictionary()
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)

    # Get sorted key-value pairs
    result = sorted(dictionary.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    # Assert result matches expected
    assert result == expected


def test_filter():
    # Test filtering dictionary by a predicate
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25), ("height", 170)])
    filtered_dict = dictionary.filter(lambda k, v: isinstance(v, int))  # Filter integer values

    result = sorted(filtered_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("height", 170)]

    assert result == expected


def test_map():
    # Test mapping values in the dictionary
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])

    # Define mapping function
    def map_function(value: Any) -> Any:
        return value.upper() if isinstance(value, str) else value

    # Apply mapping function to each value
    mapped_dict = dictionary.map(map_function)

    result = sorted(mapped_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "ALICE")]

    assert result == expected


def test_reduce():
    # Test reducing values in the dictionary
    dictionary = Dictionary()
    dictionary.from_list([("a", 1), ("b", 2), ("c", 3)])
    result = dictionary.reduce(lambda acc, v: acc + v, 0)  # Sum values
    assert result == 6


def test_iter():
    # Test iterating over the dictionary
    dictionary = Dictionary()
    dictionary.from_list([("name", "Alice"), ("age", 25)])
    items = list(iter(dictionary))

    result = sorted(items, key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    assert result == expected


def test_empty():
    # Test the empty dictionary
    dictionary = Dictionary.empty()
    assert dictionary.size() == 0
    assert dictionary.to_list() == []


def test_concat():
    # Test concatenating two dictionaries
    dictionary1 = Dictionary()
    dictionary1.from_list([("name", "Alice")])
    dictionary2 = Dictionary()
    dictionary2.from_list([("age", 25)])
    combined_dict = dictionary1.concat(dictionary2)

    result = sorted(combined_dict.to_list(), key=lambda x: str(x[0]))
    expected = [("age", 25), ("name", "Alice")]

    assert result == expected


def test_monoid_properties():
    # Test monoid properties (identity and associativity)
    empty_dict = Dictionary.empty()
    dict1 = Dictionary()
    dict1.add("a", 1)
    dict1.add("b", 2)

    # Identity property
    assert dict1.concat(empty_dict).to_list() == dict1.to_list()
    assert empty_dict.concat(dict1).to_list() == dict1.to_list()

    # Associativity property
    dict2 = Dictionary()
    dict2.add("c", 3)
    dict3 = Dictionary()
    dict3.add("d", 4)
    left = dict1.concat(dict2).concat(dict3)
    right = dict1.concat(dict2.concat(dict3))
    assert left.to_list() == right.to_list()


def test_none_values():
    # Test handling of None keys and values
    dictionary = Dictionary()

    # Test None key
    try:
        dictionary.add(None, "value")
    except ValueError as e:
        assert str(e) == "None keys are not allowed in this dictionary."

    # Test None value
    try:
        dictionary.add("key", None)
    except ValueError as e:
        assert str(e) == "None values are not allowed in this dictionary."


def test_mixed_types():
    # Test handling of mixed key and value types
    dictionary = Dictionary()

    # Add mixed types
    dictionary.add("name", "Alice")
    dictionary.add("age", 25)
    dictionary.add(42, "answer")

    # Check values
    assert dictionary.get("name") == "Alice"
    assert dictionary.get("age") == 25
    assert dictionary.get(42) == "answer"

    # Convert to list and sort
    result = dictionary.to_list()
    expected = [("name", "Alice"), ("age", 25), (42, "answer")]

    sorted_result = sorted(result, key=lambda x: str(x[0]))
    sorted_expected = sorted(expected, key=lambda x: str(x[0]))

    assert sorted_result == sorted_expected
