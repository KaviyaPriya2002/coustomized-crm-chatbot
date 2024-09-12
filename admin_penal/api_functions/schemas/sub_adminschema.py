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


class UpdateSchema(Schema):
    username = fields.String(required=False)
    email = fields.Email(required=False)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    confirm_password = fields.String(required=False)
    role = fields.String(required=False)

    # @validates_schema
    # def validate_passwords(self, data, **kwargs):
    #     password = data.get('password')
    #     confirm_password = data.get('confirm_password')
    #
    #     if password or confirm_password:
    #         if not (password and confirm_password):
    #             raise ValidationError('Both password and confirmation password must be provided.')
    #         if password != confirm_password:
    #             raise ValidationError('Passwords do not match.')