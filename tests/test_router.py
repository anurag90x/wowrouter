import router
import unittest

def doge():
        return 'x'


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.thing = router.router.Router()

    def test_add_routes(self):
        self.thing.add_route('/doge', doge)
        self.thing.add_route('/dog1', doge)
        self.thing.add_route('/doge/woof', doge)
        self.thing.add_route('/meow', doge)
        expected_routes = ['/doge', '/meow', '/dog1', '/doge/woof']
        self.assertEqual(
            sorted(expected_routes),
            sorted([t for t in self.thing.show_routes()])
        )

    def test_load_route(self):
        self.thing.add_route('/doge', doge)
        route_action = self.thing.load_route('/doge')
        self.assertEqual('x', route_action())
