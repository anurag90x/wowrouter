from router import router

class Application:
    def __init__(self, env, response_handler):
        self.env = env
        self.start_response = response_handler
        self.router = router.Router()


    def __call__(self):
        self.processsor = RequestProcessor(self.env, self.router)
        response = self.processor.process_request()
        status, response_headers = response.next()
        self.start_response(status, response_headers)
        yield response.next()


class RequestProcessor:
    def __init__(self, env, router):
        self.input_stream = env.get('wsgi.input')
        self.router = router

    def process_request(self):
        request = Request(self.input_stream)
        action = self.router.load_route(request.path())()

        status, response_headers = action.next()
        yield {'status': status, 'headers': response_headers}

        yield action.next()


class Request:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def path(self):
        return '/doge/woof'
