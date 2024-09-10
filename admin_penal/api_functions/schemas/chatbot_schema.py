from marshmallow import fields,Schema

class IntentSchema(Schema):
    tag = fields.String(required=True)
    # print("tag",tag)
    pattern = fields.List(fields.String(),required=True)
    # print("pattern",pattern)
    response = fields.List(fields.String(),required=True)
    # print("response",response)
    options = fields.List(fields.String(),required=True)
    # print("options",options)

class TemplateSchema(Schema):
    intents = fields.List(fields.Nested(IntentSchema),required=True)
    # print("intents>>>>>>>>>>>>>>>",intents)

template_schema = TemplateSchema()

