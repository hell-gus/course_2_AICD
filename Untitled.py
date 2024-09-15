from traceback import print_list

from modules.optimal_node_size import calculate_optimal_node_size
from modules.unrolled_linked_list import UnrolledLinkedList
import time

def check(arr_1, arr_2, n_array = None):
    if n_array is None:
        n_array = calculate_optimal_node_size(len(arr_1))
    unrolled_linked_list = UnrolledLinkedList(arr_1, n_array)
    unrolled_linked_list.print_list()
    print()
    for i in arr_2:
        unrolled_linked_list.delete_by_index(i)
        unrolled_linked_list.print_list()
        print()
    unrolled_linked_list.balance()
    unrolled_linked_list.print_list()

class Node1:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, n):
        self.head = None
        self.length = 0
        self._initialize_list(n)

    def _initialize_list(self, n):
        values = list(range(1, n + 1))
        for value in values:
            self.insert(self.length, value)

    def insert(self, index, value):
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")

        new_node = Node1(value)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self.length += 1

    def delete(self, value):
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self.length -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self.length -= 1
                return True
            current = current.next

        return False

    def str(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values)


for x in [10, 10_000, 100_000]:
    arr = [i for i in range(x)]
    unrolled_list = UnrolledLinkedList(arr, calculate_optimal_node_size(x))
    linked = LinkedList(x)
    for pos in [0, x // 2, x - 1]:

        print(f'size: {x}\npos: {pos}')
        start_time = time.time()
        unrolled_list.delete_by_index(pos)
        print('unrolled list:', time.time() - start_time)

        start_time = time.time()
        linked.delete(pos)
        print('linked list:', time.time() - start_time)

        start_time = time.time()
        arr.remove(pos)
        print('array:', time.time() - start_time, '\n')
unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
unroll_linked_list.insert(2, "33")
unroll_linked_list.print_list()
