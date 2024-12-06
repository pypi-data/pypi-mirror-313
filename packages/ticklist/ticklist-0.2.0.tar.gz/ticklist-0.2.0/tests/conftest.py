from typing import Collection


def compare(result: object, expected: object):
    """Compare two objects for equality.

    Using this instead of implementing `__eq__` in the class itself
    as the pytest output on fail is useless for troubleshooting.

    The below code gives clear pointers where stuff goes wrong
    (especially in combination with pytest-icdiff)
    """
    assert type(result) is type(expected)

    assert result.__dict__ == expected.__dict__


def compare_items(items: Collection, *objects):
    assert len(items) == len(
        objects
    ), "actual field-item count not equal to expected field-item count."

    for item, object in zip(items, objects, strict=True):
        compare(item, object)
