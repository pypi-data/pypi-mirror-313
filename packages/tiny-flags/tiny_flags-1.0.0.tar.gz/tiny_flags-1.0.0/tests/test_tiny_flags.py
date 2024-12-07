# tests/test_bitfield.py
from collections import OrderedDict

import pytest

from tiny_flags import TinyFlags


@pytest.fixture
def manager():
    fields = OrderedDict(
        [("language", ["english", "spanish", "french"]), ("dark_mode", False), ("notifications", True)]
    )
    manager = TinyFlags(fields)
    return manager


def test_boolean_fields(manager):
    # Test initial values
    assert manager.get_value("dark_mode") is False
    assert manager.get_value("notifications") is True

    # Test setting values
    manager.set_value("dark_mode", True)
    assert manager.get_value("dark_mode") is True


def test_option_fields(manager):
    print("\nDebug info:")
    print(f"Bit positions: {manager.bit_positions}")
    print(f"Bit widths: {manager.bit_widths}")
    print(f"Option mappings: {manager.option_mappings}")
    print(f"Current bitfield value: {bin(manager.bitfield.value)}")

    # Test initial value
    value = manager.get_value("language")
    print(f"Retrieved language value: {value}")

    assert manager.get_value("language") == "english"

    # Test initial value (should default to first option)
    print(manager.get_value("language"))
    assert manager.get_value("language") == "english"

    # Test setting valid option
    manager.set_value("language", "spanish")
    assert manager.get_value("language") == "spanish"

    # Test invalid option
    with pytest.raises(ValueError):
        manager.set_value("language", "invalid_language")


def test_invalid_field():
    fields = OrderedDict([])
    manager = TinyFlags(fields)
    with pytest.raises(ValueError):
        manager.get_value("nonexistent_field")


def test_bit_width_calculation():
    fields = OrderedDict(
        [
            ("two_options", ["a", "b"]),  # Should use 1 bit
            ("three_options", ["a", "b", "c"]),  # Should use 2 bits
            ("four_options", ["a", "b", "c", "d"]),  # Should use 2 bits
        ]
    )
    manager = TinyFlags(fields)

    assert manager.bit_widths["two_options"] == 1
    assert manager.bit_widths["three_options"] == 2
    assert manager.bit_widths["four_options"] == 2


def test_bitfield_persistence():
    fields = OrderedDict([("option", ["a", "b", "c"]), ("flag", True)])
    manager = TinyFlags(fields)

    # Set some values
    manager.set_value("option", "b")
    manager.set_value("flag", False)

    # Store the bitfield value
    value = manager.bitfield.value

    # Create new manager with same fields
    new_manager = TinyFlags(fields)
    new_manager.bitfield.value = value

    # Check values persisted
    assert new_manager.get_value("option") == "b"
    assert new_manager.get_value("flag") is False
