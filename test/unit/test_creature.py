import pytest

from model.creature import Stat


def test_stat_init():
    max_value = 10
    some_stat = Stat(max_value)
    assert some_stat.cur == some_stat.max == max_value


def test_stat_cur_setter():
    max_value = 10
    some_stat = Stat(max_value)

    some_stat.cur = -1
    assert some_stat.cur == 0

    some_stat.cur = max_value + 1
    assert some_stat.cur == max_value


@pytest.mark.parametrize("fullness", (1, 0.5, 0))
def test_stat_max_higher(fullness):
    max_starting_value = 10
    cur_starting_value = fullness * max_starting_value
    some_stat = Stat(max_starting_value)
    some_stat.cur = cur_starting_value

    some_stat.max += 1
    assert some_stat.max == max_starting_value + 1
    assert some_stat.cur == cur_starting_value + 1


@pytest.mark.parametrize("delta", (0, 1, 2))
def test_stat_max_lower(delta):
    max_starting_value = 10
    cur_starting_value = max_starting_value - delta
    some_stat = Stat(max_starting_value)
    some_stat.cur = cur_starting_value

    some_stat.max -= 1
    assert some_stat.max == max_starting_value - 1
    assert some_stat.cur == min(cur_starting_value, some_stat.max)
