import math
from .node import Node

class UnrolledLinkedList:
    def __init__(self, data = None, size_of_node = 1):
        self.size_of_node = size_of_node
        self.head = Node()
        self.data_len = len(data)
        self.nodes_count = math.ceil(len(data) / size_of_node)

        if data is None:
            data = list()

        self.head.data = data[:size_of_node]
        self.head.size_of_node = len(self.head.data)
        if self.nodes_count > 1:
            self.head.next = Node()
            temp_next = self.head.next
            for i in range(1, self.nodes_count):
                temp_next.data = data[i * size_of_node:(i + 1) * size_of_node]
                temp_next.size_of_node = len(temp_next.data)
                if i != self.nodes_count - 1:
                    temp_next.next = Node()
                    temp_next = temp_next.next

    def print_list(self):
        temp_next = self.head
        for i in range(self.nodes_count):
            print(f"Node {i}: {' '.join(map(str, temp_next.data))}")
            temp_next = temp_next.next

    def __len__(self):
        return self.data_len

    def find_by_index(self, index):
        if self.__len__() <= index < 0:
            return None
        elements_count = 0
        temp_next = self.head
        for i in range(self.nodes_count):
            if elements_count <= index <= (elements_count + temp_next.size_of_node -1):
                return temp_next.data[index - elements_count]
            elements_count += temp_next.size_of_node
            temp_next = temp_next.next

    def delete_by_index(self, index):
        if self.__len__() <= index < 0:
            return None
        elements_count = 0
        temp_next = self.head
        for i in range(self.nodes_count):
            if elements_count <= index <= (elements_count + temp_next.size_of_node -1):
                del temp_next.data[index - elements_count]
                temp_next.size_of_node -= 1
                self.data_len -= 1
                if self.__len__() == 0:
                    self.head = None
                    self.nodes_count = 0
                return True
            elements_count += temp_next.size_of_node
            temp_next = temp_next.next

    def append(self, value):
        temp = self.head

        while temp.next:
            temp = temp.next

        if temp.size_of_node < self.size_of_node:
            temp.data.append(value)
            temp.size_of_node += 1
        else:
            new_node = Node()
            new_node.data.append(value)
            new_node.size_of_nodes = 1
            temp.next = new_node
        self.data_len += 1

    def insert(self, index, value):
        temp_next = self.head
        size_of_node = 0

        while temp_next:
            if size_of_node <= index < size_of_node + len(temp_next.data):
                break
            size_of_node += len(temp_next.data)
            temp_next = temp_next.next

        insert_position = index - size_of_node
        temp_next.data.insert(insert_position, value)
        temp_next.size_of_node += 1
        self.data_len += 1

        if len(temp_next.data) > self.size_of_node:
            new_node = Node()
            mid_index = len(temp_next.data) // 2
            new_node.data = temp_next.data[mid_index:]
            new_node.size_of_node = len(new_node.data)
            temp_next.data = temp_next.data[:mid_index]
            temp_next.size_of_node = len(temp_next.data)

            new_node.next = temp_next.next
            temp_next.next = new_node
            self.nodes_count += 1
    def balance(self, size_of_node = None):
        if size_of_node is None:
            size_of_node = self.size_of_node
        data = []
        temp_next = self.head
        for i in range(self.nodes_count):
            data.extend(temp_next.data)
            temp_next = temp_next.next
        self.__init__(data, size_of_node)


