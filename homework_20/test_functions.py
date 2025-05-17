import pytest
from functions import Fibonacci, formatted_name

def test_fibonacci_base_cases():
    fib = Fibonacci()
    assert fib(0) == 0
    assert fib(1) == 1

def test_fibonacci_recursive_cases():
    fib = Fibonacci()
    assert fib(5) == 5
    assert fib(10) == 55
    assert fib(15) == 610

def test_fibonacci_cache_growth():
    fib = Fibonacci()
    fib(10)
    assert fib.cache == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

def test_fibonacci_invalid_input():
    fib = Fibonacci()
    with pytest.raises(ValueError):
        fib(-1)
    with pytest.raises(ValueError):
        fib("abc")
    with pytest.raises(ValueError):
        fib(3.5)


def test_formatted_name_without_middle():
    result = formatted_name('john', 'doe')
    assert result == 'John Doe'

def test_formatted_name_with_middle():
    result = formatted_name('john', 'doe', 'michael')
    assert result == 'John Michael Doe'

def test_formatted_name_edge_cases():
    result = formatted_name('ALICE', 'SMITH', '')
    assert result == 'Alice Smith'
    result = formatted_name('a', 'b', 'c')
    assert result == 'A C B'
