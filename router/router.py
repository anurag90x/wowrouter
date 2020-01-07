from trie import Trie


class Router:
    def __init__(self):
        self.trie = Trie()

    def add_route(self, route, route_action):
        self.trie.add(route, route_action)

    def show_routes(self):
        root = self.trie.root
        th = []
        for thing in self.trie.get_paths()(root.children.values()[0]):
            th.append(thing)
        return th

    def load_route(self, route):
        return self.trie.find(route, {})
