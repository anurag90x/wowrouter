dynamic_whitelist = ['integer', 'string']


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
            if current == '':
                node.children[''] = route_action
                return

            if current[0] in node.children:
                return _add(node.children[current[0]], current[1:])

            curr = current[0]
            variable_binding = dynamic_binding(curr)
            if variable_binding:
                node.children[str(type(curr))] = Node(variable_binding)
            else:
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
            if type(current[0]) in node.children:
                # this is the actual variable binding name
                bindings.update({
                    node.children[type(current[0])]: current[0],
                })
                return _find(
                    node.children[type(current[0])],
                    current[1:],
                    bindings
                )

            return False
        return _find(self.root, path)


def dynamic_binding(segment):
    dyn_tags = segment[0] == '<' and segment[-1] == '>'
    if (dyn_tags and segment[1:-1] in dynamic_whitelist):
        return segment.split(':')[-1]
