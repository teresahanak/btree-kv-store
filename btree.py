from node import Node

class BTree:
    def __init__(self, split_threshold=2):
        self.root = Node()
        self.height = 0
        self.size = 0
        self.split_threshold = split_threshold

    def __len__(self):
        return self.size

    def _add(self, current_node, key, value):
        if current_node.is_leaf():
            len_before = len(current_node)
            current_node.insert_entry(key, value)
            if len(current_node) > len_before:
                self.size += 1
        else:
            child_index = current_node.get_insert_index(key)
            self._add(current_node.children[child_index], key, value)
        if len(current_node) > self.split_threshold:
            parent = current_node.split()
            if current_node == self.root:
                self.root = parent
                self.height += 1

    def add(self, key, value):
        self._add(self.root, key, value)


    def _find_node(self, current_node, key):
        if current_node.contains_key(key):
            return current_node
        if current_node.is_leaf():
            return None
        child_index = current_node.get_insert_index(key)
        return self._find_node(current_node.children[child_index], key)

    def contains(self, key):
        node = self._find_node(self.root, key)
        return node is not None

    def get_value(self, key):
        node = self._find_node(self.root, key)
        if node is not None:
            for i, k in enumerate(node.keys):
                if k == key:
                    return node.values[i]