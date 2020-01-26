from collections import deque


class TreeNode:
    def __init__(self, label, metadata):
        self.label = label
        self.metadata = metadata
        self.childs = {}

    def add_child(self, label, tree_node):
        self.childs[label] = tree_node


class Tree:
    def __init__(self, root_label, root_metadata=None):
        self.root = TreeNode(root_label, root_metadata)

    def print_all_nodes(self):
        nodes_queue = deque([(self.root.label, self.root)])
        while nodes_queue:
            path_prefix, node = nodes_queue.popleft()
            print('---', path_prefix)
            for child_label, child_node in node.childs.items():
                print(child_label)
                if child_node.childs:
                    nodes_queue.append((
                        '{}/{}'.format(path_prefix, child_label),
                        child_node
                    ))

    def flatten_to_dict(self):
        result = {}
        nodes_queue = deque([(self.root.label, self.root)])
        while nodes_queue:
            path_prefix, node = nodes_queue.popleft()
            result[path_prefix] = node.metadata
            for child_label, child_node in node.childs.items():
                nodes_queue.append((
                    '{}/{}'.format(path_prefix, child_label),
                    child_node
                ))
        return result
