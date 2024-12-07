from field_mapper.mapper import FieldMapper


def validate_email(value: str) -> bool:
    """Custom validator for email format."""
    return "@" in value and "." in value

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}
data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "charlieexample.com", "phone": "453543535", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "34534523", "income":0}
]
mapper = FieldMapper(fields, field_map)
# data_validate = {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"}
# print(mapper.validate(data_validate))
processed_data = mapper.process(data)
print("Output:", processed_data)
print("Error:",mapper.error)
