from  marshmallow import Schema,fields,validate
class CreateBot(Schema):
    bot_name = fields.String(required=True,validate=validate.Length(min=3, max=50))
    description = fields.String(required=True)
    bot_type = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
