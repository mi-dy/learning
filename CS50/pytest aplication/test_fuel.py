from fuel import convert
from fuel import gauge
import pytest
#testing if convert() function returns integer and correctly raises errors
def test_convert():
    assert convert("1/2") == 50
    assert convert("0/1") == 0
    with pytest.raises(ValueError):
        convert("a/b")
    with pytest.raises(ValueError):
        convert("2/1")
    with pytest.raises(ZeroDivisionError):
        convert("0/0")

#testing if gauge() function correctly converts integer to percentage or F or E for full and empty tank
def test_gauge():
    assert gauge(50) == "50%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"
    assert gauge(1) == "E"
    assert gauge(0) == "E"
