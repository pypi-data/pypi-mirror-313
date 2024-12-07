"""Enum block tests"""
import pytest

from mr_star_ble.commands import (
    format_brightness_command,
    format_color_command,
    format_command,
    format_power_command,
)


def test_format_command():
    """Test base command formatting"""
    assert format_command(0x01, [0x02, 0x03]) == bytes([
        0xBC, 0x01, 0x02, 0x02, 0x03, 0x55])
    try:
        format_command(1, [])
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True

def test_format_power_command():
    """Test power command formatting"""
    assert format_power_command(True) == bytes([
        0xBC, 0x01, 0x01, 0x01, 0x55])
    assert format_power_command(False) == bytes([
        0xBC, 0x01, 0x01, 0x00, 0x55])

def test_format_brightness_command():
    """Test brightness command formatting"""
    assert format_brightness_command(0) == bytes([
        0xBC, 0x05, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])
    assert format_brightness_command(1) == bytes([
        0xBC, 0x05, 0x06, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])
    assert format_brightness_command(0.5) == bytes([
        0xBC, 0x05, 0x06, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x55])

    try:
        format_brightness_command(2)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True
    try:
        format_brightness_command(-1)
        pytest.fail(Exception("Expected ValueError"))
    except ValueError:
        assert True


def test_format_color_command():
    """Test color command formatting"""
    assert format_color_command((0, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0x00, 0x03, 0xe8, 0x00, 0x00, 0x55])
    assert format_color_command((120, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0x78, 0x03, 0xE8, 0x00, 0x00, 0x55])
    assert format_color_command((240, 100)) == bytes([
        0xBC, 0x04, 0x06, 0x00, 0xF0, 0x03, 0xE8, 0x00, 0x00, 0x55])
