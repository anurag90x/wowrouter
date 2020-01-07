from trie import Trie
import functools


class Router:
    def __init__(self):
        self.trie = Trie()

    def add_route(self, route, route_action):
        segments = ['/' + seg for seg in route.split('/')]
        self.trie.add(segments, route_action)

    def show_routes(self):
        root = self.trie.root
        th = []
        for thing in self.trie.get_paths()(root.children.values()[0]):
            th.append(thing)
        return th

    def load_route(self, route):
        segments = ['/' + seg for seg in route.split('/')]
        action, bindings = self.trie.find(segments, {})
        return functools.partial(action, **bindings)
