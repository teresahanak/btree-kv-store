import bisect

class Node:
    
    def __init__(self, keys=None, values=None, children=None, parent=None):
        self.keys = keys or []
        self.values = values or []
        self.parent = parent
        self.set_children(children)

    def __len__(self):
        return len(self.values)

    def set_children(self, children):
        self.children = children or []
        for child in self.children:
            child.parent = self

    def is_leaf(self):
        return len(self.children) == 0

    def contains_key(self, key):
        return key in self.keys

    def get_value(self, key):
        for i, k in enumerate(self.keys):
            if k == key:
                return self.values[i]
        print(f'Key Error: "{key}" not found')
        return None

    def get_insert_index(self, key):
        return bisect.bisect(self.keys, key)

    def _update_entry(self, key, value):
        for i, k in enumerate(self.keys):
            if k == key:
                self.values[i] = value

    def insert_update_entry(self, key, value):
        if self.contains_key(key):
            self._update_entry(key, value)
        else:
            insert_index = self.get_insert_index(key)
            self.keys.insert(insert_index, key)
            self.values.insert(insert_index, value)
            return insert_index  # insert_index used for insert_child call on split_with_parent

    def split(self):
        if self.parent is None:
            return self._split_no_parent()
        return self._split_with_parent()

    def _split_no_parent(self):
        split_index = len(self) // 2
        key_to_move_up = self.keys[split_index]
        value_to_move_up = self.values[split_index]
        right_node = Node(
            self.keys[split_index + 1 :],
            self.values[split_index + 1 :],
            self.children[split_index + 1 :],
        )
        self.keys = self.keys[:split_index]
        self.values = self.values[:split_index]
        self.children = self.children[: split_index + 1]
        parent = Node([key_to_move_up], [value_to_move_up], [self, right_node])
        return parent

    def _insert_child(self, insert_index, child):
        self.children.insert(insert_index, child)
        child.parent = self

    def _split_with_parent(self):
        split_index = len(self) // 2
        key_to_move_up = self.keys[split_index]
        value_to_move_up = self.values[split_index]
        right_node = Node(
            self.keys[split_index + 1 :],
            self.values[split_index + 1 :],
            self.children[split_index + 1 :],
        )
        self.keys = self.keys[:split_index]
        self.values = self.values[:split_index]
        self.children = self.children[: split_index + 1]
        insert_index = self.parent.insert_update_entry(key_to_move_up, value_to_move_up)
        self.parent._insert_child(insert_index + 1, right_node)
        return self.parent