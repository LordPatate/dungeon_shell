import itertools
import unittest
import pytest

from utils import Container


class Item:
    def __init__(self, name):
        self.name = name


class EmptyContainerTest(unittest.TestCase):
    def setUp(self):
        self.container = Container[Item]()
        print(self.container.details)

    def test_false_on_creation(self):
        assert bool(self.container) is False

    def test_iter(self):
        for _ in self.container:
            assert False


class PopulatedContainerTest:
    def __init__(self, number_of_items, item_name_generator):
        self.container = Container[Item]()
        self.names = [next(item_name_generator) for _ in range(number_of_items)]
        self.items = [Item(name) for name in self.names]
        for item in self.items:
            self.container.push(item)

        print(self.container.details())


@pytest.mark.parametrize('item_name_generator', [
         (f'item{i}' for i in itertools.count()),
         (f'item{i % 2}' for i in itertools.count()),
 ])
@pytest.mark.parametrize('number_of_items', range(1, 10, 2))
def test_false_once_emptied(number_of_items, item_name_generator):
    test = PopulatedContainerTest(number_of_items, item_name_generator)
    for name in test.names:
        test.container.remove(name)
    assert bool(test.container) is False


@pytest.mark.parametrize('item_name_generator', [
         (f'item{i}' for i in itertools.count()),
         (f'item{i % 2}' for i in itertools.count()),
 ])
@pytest.mark.parametrize('number_of_items', range(1, 10, 2))
def test_iter(number_of_items, item_name_generator):
    test = PopulatedContainerTest(number_of_items, item_name_generator)
    for name in test.names:
        assert name in test.container
