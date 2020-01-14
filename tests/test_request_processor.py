from app import RequestProcessor
import router
import unittest


class TestRequestProcessor(unittest.TestCase):
    def  test_process_request(self):
        env_input = {
            'wsgi.input': 'doge'
        }
        def test_action(**kwargs):
            yield 200, {'x-token': 123}
            yield  kwargs.get('action')

        app_router = router.router.Router()
        app_router.add_route('/doge/<action:string>', test_action)
        processor = RequestProcessor(
            env_input,
            app_router
        )
        expected_prebody_response = {
            'status': 200,
            'headers': {'x-token': 123},
        }
        response = processor.process_request()
        self.assertEqual(
            expected_prebody_response,
            response.next()
        )
        self.assertEqual(
            'woof',
            response.next()
        )
