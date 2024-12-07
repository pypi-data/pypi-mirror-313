from field_mapper.mapper import FieldMapper


def validate_email(value: str) -> bool:
    """Custom validator for email format."""
    return "@" in value and "." in value


fields = {
    "name": {"type": str, "max_length": 50, "required": True},
    "email": {"type": str, "max_length": 100, "required": True, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required": False}
}
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number"
}

mapper = FieldMapper(fields, field_map)

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "invalid-email"},
    {"name": "Charlie", "email": "charlie@example.com"}
]
# data_validate = {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"}
# print(mapper.validate(data_validate))
processed_data = mapper.process(data)
print(processed_data)
