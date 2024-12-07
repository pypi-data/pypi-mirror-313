from typing import List, Dict, Any, Callable, Union, Type

from field_mapper.exc.exception import FieldValidationError, MissingFieldError, InvalidTypeError, InvalidLengthError, \
    CustomValidationError


class FieldMapper:
    def __init__(self, fields: Dict[str, Dict[str, Union[Type, int, Callable, bool]]], field_map: Dict[str, str]):
        self.fields = fields
        self.field_map = field_map
        self.error = []

    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate fields based on the constraints provided in the `fields` dictionary.
        """
        missing = []
        type_errors = []
        length_errors = []
        value_errors = []
        custom_errors = []

        for field, constraints in self.fields.items():
            is_required_field = constraints.get("required_field", True)
            is_required_value = constraints.get("required_value", True)
            expected_type = constraints.get("type")
            max_length = constraints.get("max_length")
            custom_validator = constraints.get("custom")
            value = data.get(field)

            # Check for missing fields
            if is_required_field and field not in data:
                missing.append(field)
                continue

            # Skip validation for optional fields if not present
            if not is_required_field and value is None:
                continue

            # Check required_value if specified
            if is_required_value and not value and value != 0:
                value_errors.append(field)

            # Validate type
            if value is not None and expected_type and not isinstance(value, expected_type):
                type_errors.append(field)

            # Validate max length for strings
            if value is not None and max_length and isinstance(value, str) and len(value) > max_length:
                length_errors.append(field)

            # Apply custom validation if defined
            if value is not None and custom_validator and callable(custom_validator):
                try:
                    if not custom_validator(value):
                        custom_errors.append(field)
                except Exception as e:
                    custom_errors.append(field)

        if missing:
            raise MissingFieldError("Missing required fields", missing, data)
        if value_errors:
            raise ValueError("Required fields must have non-empty values", value_errors)
        if type_errors:
            raise InvalidTypeError("Invalid field types", type_errors, data)
        if length_errors:
            raise InvalidLengthError("Fields exceeding max length", length_errors, data)
        if custom_errors:
            raise CustomValidationError("Custom validation failed", custom_errors, data)

    def map(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map internal fields to the target field names.
        """
        return {
            self.field_map.get(key, key): value
            for key, value in data.items()
            if key in self.field_map
        }

    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of data entries, validating and src fields.
        """
        if not isinstance(data, list):
            raise ValueError("Input data must be a list of dictionaries.")

        result = []
        for entry in data:
            try:
                self.validate(entry)
                mapped_data = self.map(entry)
                result.append(mapped_data)
            except FieldValidationError as exc:
                self.error.append(f"(Error Details: {exc} | Validation Error for data: {exc.problematic_data})")
                print(f"Error Details: {exc} | Validation Error for data: {exc.problematic_data}")
        return result

