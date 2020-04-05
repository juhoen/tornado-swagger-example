"""Handlers module"""
import json
from datetime import datetime

from tornado.web import RequestHandler

from .schemas import CarBrandSchema

# Let this be our database,
# purely for demonstration :)
CAR_BRAND_DATABASE = []


class BaseHandler(RequestHandler):
    """Application base handler"""

    def json_response(self, status, data):
        """Helper method for sending response containing json data
        """
        self.set_header("Content-Type", "application/json")
        self.set_status(status)
        self.write(json.dumps(data, default=str))
        self.finish()


class CarBrandHandler(BaseHandler):
    """Car brand handler"""

    def get(self):
        """Return all the cars brands from our "database"
        ---
        tags: [Car brands]
        summary: Get car brands
        description: Get all the car defined brands

        responses:
            200:
                description: List of car brands
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                CarBrandSchema
        """
        self.json_response(200, CAR_BRAND_DATABASE)

    def post(self):
        """Adds new car brand into our "database"
        ---
        tags: [Car brands]
        summary: Create a car brand
        description: Create a new car brand

        requestBody:
            description: New car brand data
            required: True
            content:
                application/json:
                    schema:
                        CarBrandCreateSchema

        responses:
            201:
                description: Success payload containing newly created car brand information
                content:
                    application/json:
                        schema:
                            CarBrandCreateSuccessSchema

            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema

        """

        # Parse request body and then do the validation. json.loads might
        # raise errors. Error handling is missing for the sake of simplicity.
        car_brand = json.loads(self.request.body)
        validation_errors = CarBrandSchema().validate(car_brand)

        # Case: Provided data was invalid
        # > Return error message
        if validation_errors:
            self.json_response(400, {"success": False, "errors": validation_errors})

        # Case: Provided data was valid
        # > Add data to database and return success
        else:
            car_brand["created_at"] = datetime.utcnow()
            CAR_BRAND_DATABASE.append(car_brand)
            self.json_response(201, {"success": True, "car_brand": car_brand})
