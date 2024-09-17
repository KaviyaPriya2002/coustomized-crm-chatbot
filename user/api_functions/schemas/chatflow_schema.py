from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId

# Define a strict structure for the "nodes" field
class NodeSchema(Schema):
    id = fields.String()
    type = fields.String(required=True, validate=validate.OneOf(["text", "input", "output"]))  # Example types
    data = fields.Dict(required=True)

# Define a strict structure for the "edges" field
class EdgeSchema(Schema):
    start = fields.String(required=True, validate=validate.Length(min=1))
    to = fields.String(required=True, validate=validate.Length(min=1))
    type = fields.String(required=True)  # Example edge types

# Main dynamic schema for flow
def create_dynamic_flow_schema():
    return Schema.from_dict({
        "chatbot_id": fields.String(required=True, validate=validate.Length(equal=24)),  # Ensure chatbot_id is 24 chars
        "nodes": fields.List(fields.Nested(NodeSchema), required=True),  # Use the strict NodeSchema
        "edges": fields.List(fields.Nested(EdgeSchema), required=True)   # Use the strict EdgeSchema
    })()

# Custom validator to check if a field is a valid ObjectId
def validate_object_id(value):
    if not ObjectId.is_valid(value):
        raise ValidationError("Invalid ObjectId.")

# Example validation for ObjectId
fields.String(validate=validate_object_id)
