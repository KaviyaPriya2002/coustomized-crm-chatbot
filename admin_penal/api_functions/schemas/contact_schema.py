from  marshmallow import Schema,fields,validate
from admin_penal.api_functions.functions.contact_func import validate_phone_number
class ContactForm(Schema):
    name = fields.String(required=True,validate=validate.Length(min=3, max=50))
    phone_number = fields.String(required=True,validate=validate_phone_number)
    email = fields.Email(required=True)
    message = fields.String(required=True)