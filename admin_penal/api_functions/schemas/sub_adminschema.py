from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    phone_number = fields.String(required=True, validate=validate.Length(equal=10))
    password = fields.String(required=True, validate=validate.Length(min=6))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords must match", field_name='confirm_password')