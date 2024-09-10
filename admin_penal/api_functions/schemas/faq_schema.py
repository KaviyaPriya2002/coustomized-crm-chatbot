from marshmallow import Schema, fields, validate

class FAQSchema(Schema):
    question = fields.Str(required=True, validate=validate.Length(min=5))
    answer = fields.Str(required=True, validate=validate.Length(min=5))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Schema for a single FAQ and a list of FAQs
faq_schema = FAQSchema()
faqs_schema = FAQSchema(many=True)
