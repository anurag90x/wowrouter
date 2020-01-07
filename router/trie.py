class Node:
    def __init__(self, val):
        self.val = val
        self.children = {}

    def __eq__(self, other):
        return self.val == other.val


class Trie:
    def __init__(self):
        self.root = Node('')

    def add(self, path, route_action):
        def _add(node, current):
            if current == []:
                node.children[''] = route_action
                return

            if current[0] in node.children:
                return _add(node.children[current[0]], current[1:])

            curr = current[0]
            node.children[curr] = Node(curr)
            return _add(node.children[curr], current[1:])
        return _add(self.root, path)

    def get_paths(self):
        def _find(node):
            if getattr(node, '__call__', None):
                yield ''
                return

            for child in node.children.values():
                val_generator = _find(child)
                for val in val_generator:
                    yield node.val + val
        return _find

    def find(self, path, bindings):
        def _find(node, current):
            if (len(node.children) == 1 and
                    getattr(node.children.values()[0], '__call__', None)):
                return node.children.values()[0]

            if current[0] in node.children:
                return _find(
                    node.children[current[0]],
                    current[1:]
                )
            dynamic_children = self._get_dynamic_children(node.children)
            for child in dynamic_children:
                    name_and_type = child.val.split(':')
                    var_name = name_and_type[0][2:]
                    bindings.update({var_name: current[0][1:]})
                    found = _find(child, current[1:])
                    if found:
                        return found
                    bindings.pop(var_name)

            return False
        return _find(self.root, path), bindings

    def _get_dynamic_children(self, children):
        def is_dynamic(val):
            return len(val) > 2 and val[1] == '<' and val[-1] == '>'
        return [child for child in children.values() if is_dynamic(child.val)]
