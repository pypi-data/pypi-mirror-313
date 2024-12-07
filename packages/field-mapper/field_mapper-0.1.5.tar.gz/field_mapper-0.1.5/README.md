### Field Mapper: Documentation

Field Mapper is a Python library for validating, mapping, and transforming data fields. It supports type checking, length constraints, optional fields, and custom validation rules, making it perfect for structured data validation.

### Installation
Install the library using pip
```bash
pip install field-mapper
```

### Quick Start
1. Define Fields
Create a dictionary to define the rules for your data fields.
```python
fields = {
    "name": {"type": str, "max_length": 50},
    "email": {"type": str, "max_length": 100, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required": False},
}
```

2. Prepare Data
The input should be a list of dictionaries.
```python
data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "123456789"},
    {"name": "Bob", "email": "invalid-email", "phone": "987654321"},
]
```

3. Data Process
Use the process method to check and transform the data.

```python
from field_mapper import FieldMapper

fields = {
    "name": {"type": str, "max_length": 50},
    "email": {"type": str, "max_length": 100, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required": False},
}

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "123456789"},
    {"name": "Bob", "email": "invalid-email", "phone": "987654321"},
]

mapper = FieldMapper(fields)
processed_data = mapper.process(data)
print(processed_data)

```

4. Custom Validation
Define custom validation logic for specific fields.

```python
def validate_email(value):  
    import re  
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):  
        raise ValueError(f"Invalid email address: {value}")  

#Add the custom validator in the field definition:
fields = {
    "email": {"type": str, "custom": validate_email},
}

```

5. Optional Fields
Mark fields as optional with required: False. 
If check_optional_fields=True is set, their presence is mandatory but values can be empty:
```python
fields = {
    "phone": {"type": str, "max_length": 15, "required": False},
}
mapper = FieldMapper(fields, check_optional_fields=True)  

```

### Example usage

```python
from field_mapper import FieldMapper


def validate_email(value: str) -> bool:
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
processed_data = mapper.process(data)
print(processed_data)

```
