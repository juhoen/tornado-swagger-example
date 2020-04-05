"""Schemas module"""
from marshmallow import Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        ordered = True


# RESPONSES
# =========


class BaseSuccessSchema(BaseSchema):
    success = fields.Boolean(
        required=True,
        description='This is always "True" when a request succeeds',
        example=True,
    )


class BaseErrorSchema(BaseSchema):
    success = fields.Boolean(
        required=True,
        description='This is always "False" when a request fails',
        example=False,
    )


class BadRequestSchema(BaseErrorSchema):
    errors = fields.Dict(
        required=False,
        description="Attached request body validation errors",
        example={"name": ["Missing data for required field."]},
    )


# CAR BRANDS
# ==========


class CarBrandSchema(BaseSchema):
    """Complete car brand schema"""

    name = fields.Str(
        required=True,
        description="Name of the car brand",
        example="Mercedes-Benz",
        validate=validate.Length(min=1, max=16),
    )
    established = fields.Int(
        required=True,
        description="Year when the car brand was established",
        example=1926,
        validate=validate.Range(min=1886, max=2100),
    )
    created_at = fields.DateTime(
        required=False,
        description="The time at which the car brand was created in the database",
    )


class CarBrandCreateSchema(CarBrandSchema):
    class Meta:
        ordered = True
        exclude = ("created_at",)


class CarBrandCreateSuccessSchema(BaseSuccessSchema):
    car_brand = fields.Nested(
        CarBrandSchema,
        required=True,
        description="Validated and newly created car brand information",
    )
