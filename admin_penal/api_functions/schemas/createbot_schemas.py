from marshmallow import fields,Schema

class CreatebotSchema(Schema):
    chatbot_name = fields.String(required=True)
    chatbot_type = fields.String(required=True)
    chatbot_description = fields.String(required=True)


CreatebotSchema()
