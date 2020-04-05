"""Main application module"""
import swagger_ui
import tornado.ioloop
import tornado.web

from app.handlers import CarBrandHandler
from init_swagger import generate_swagger_file

SWAGGER_API_OUTPUT_FILE = "./swagger.json"


def make_app():
    handlers = [
        (r"/brands", CarBrandHandler),
    ]

    # Initialize Tornado application
    app = tornado.web.Application(handlers)

    # Generate a fresh Swagger file
    generate_swagger_file(handlers=handlers, file_location=SWAGGER_API_OUTPUT_FILE)

    # Start the Swagger UI. Automatically generated swagger.json can also
    # be served using a separate Swagger-service.
    swagger_ui.tornado_api_doc(
        app,
        config_path=SWAGGER_API_OUTPUT_FILE,
        url_prefix="/swagger/spec.html",
        title="Car Brand API",
    )

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
