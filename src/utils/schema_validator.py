import json
import os
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    """
    Loads and returns the JSON schema from the given path.
    """
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return schema

def validate_data(data, schema_path):
    """
    Validates the input data dictionary against the JSON schema.
    
    Returns:
        True if valid, False otherwise.
    """
    try:
        schema = load_schema(schema_path)
        validate(instance=data, schema=schema)
        return True
    except ValidationError as ve:
        print(f"Validation Error: {ve.message}")
        return False
    except Exception as e:
        print(f"Error loading schema or validating data: {e}")
        return False
