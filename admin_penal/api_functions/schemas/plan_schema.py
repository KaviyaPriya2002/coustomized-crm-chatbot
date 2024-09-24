from marshmallow import Schema, fields, validates_schema, ValidationError

class ManagePlanSchema(Schema):
    title = fields.Str(required=True)
    is_trial = fields.Bool(required=True)
    price = fields.Float(required=False)  # Conditionally required
    price_crossed = fields.Float(required=False)
    duration_in_days = fields.Int(required=True)
    short_description = fields.Str(required=True)
    allow_chat_tags = fields.Bool(required=True)
    allow_chat_note = fields.Bool(required=True)
    allow_wa_chatbot = fields.Bool(required=True)


    @validates_schema
    def dynamic_validation(self, data, **kwargs):
        is_trial = data.get('is_trial')
        price = data.get('price')


        if is_trial and price is not None:
            raise ValidationError({"price": "Price should not be provided for trial plans."})
        if not is_trial and price is None:
            raise ValidationError({"price": "Price is required for non-trial plans."})
