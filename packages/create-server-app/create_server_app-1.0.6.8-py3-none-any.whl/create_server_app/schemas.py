import os

def create_schemas_folder(server):
    schemas = os.path.join(server, 'schemas')
    os.makedirs(schemas, exist_ok=True)


    schemas_content = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "User",
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "The unique identifier for a user"
        },
        "name": {
            "type": "string",
            "description": "The name of the user"
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "The email address of the user"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "description": "The age of the user"
        },
        "isActive": {
            "type": "boolean",
            "description": "Whether the user is active"
        }
    },
    "required": ["id", "name", "email"]
}"""

    with open(os.path.join(schemas, 'SampleUser.json'), 'w') as f:
        f.write(schemas_content)