import pytest

from alg_lab1.main import unroll_linked_list
from modules.unrolled_linked_list import UnrolledLinkedList

def test_initialization():
    unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
    assert len(unroll_linked_list) == 4, "Длина должна быть равна количеству переданных элементов при инициализации"

def test_find_by_index():
    unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
    assert unroll_linked_list(1) == 2, "Элемент с индекса 1 должен равняться 2"

def test_delete_by_index():
    unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
    #print(len(unroll_linked_list))
    unroll_linked_list.delete_by_index(1)
    assert (len(unroll_linked_list) == 3 and unroll_linked_list.find_by_index(1) == 3), "Проблема либо в длине, либо в смещении"

def test_of_append():
    unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
    unroll_linked_list.append(1)
    assert len(unroll_linked_list) == 1, "После вставки нового эдемента должна увеличиться длина"

def test_of_insert():
    pass

def test_of_balace():
    pass