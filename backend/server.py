from wsgiref.simple_server import make_server
from src.routes import ROUTES
from src.middleware import JSONMiddleware
from backend.main import initialize_app


import falcon


app = falcon.App(middleware=[JSONMiddleware()], independent_middleware=True)

for route in ROUTES:
    app.add_route(route[0], route[1]())


if __name__ == '__main__':
    initialize_app()
    with make_server('', 8000, app) as httpd:
        print(f"Server running on localhost:8000")
        httpd.serve_forever()
