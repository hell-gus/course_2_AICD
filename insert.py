    def insert(self, index, value):
        temp_next = self.head
        elements_count = 0

        while temp_next:
            if elements_count <= index < elements_count + len(temp_next.data):
                break
            elements_count += len(temp_next.data)
            temp_next = temp_next.next

        insert_position = index - elements_count
        temp_next.data.insert(insert_position, value)
        temp_next.count_of_added += 1
        self.data_len += 1

        if len(temp_next.data) > self.size_of_node:
            new_node = Node()
            mid_index = len(temp_next.data) // 2
            new_node.data = temp_next.data[mid_index:]
            new_node.count_of_added = len(new_node.data)
            temp_next.data = temp_next.data[:mid_index]
            temp_next.count_of_added = len(temp_next.data)

            new_node.next = temp_next.next
            temp_next.next = new_node
            self.nodes_count += 1
