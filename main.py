from traceback import print_list

from alg_lab1.modules.optimal_node_size import calculate_optimal_node_size
from modules.unrolled_linked_list import UnrolledLinkedList

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

unroll_linked_list = UnrolledLinkedList([1, 2, 3, 4], size_of_node = 4)
unroll_linked_list.insert(2, "33")
unroll_linked_list.print_list()