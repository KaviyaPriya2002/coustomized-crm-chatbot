from marshmallow import ValidationError
import re
def validate_phone_number(phone_number):
    # Example: Validate a 10-digit phone number
    if not re.fullmatch(r'\d{10}', phone_number):
        raise ValidationError('Invalid phone number. It must be 10 digits.')