KEYS_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "array",
        "items": {
            "type": "string",
        },
    },
}

TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "group": {"type": "string"},
        "key": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "typeSchema": {"type": "object"},
    },
    "required": ["group", "key", "name", "description", "typeSchema"],
    "additionalProperties": False,
}

GROUP_SCHEMA = {
    "type": "object",
    "additionalProperties": TYPE_SCHEMA,
}

GROUPS_SCHEMA = {
    "type": "object",
    "additionalProperties": GROUP_SCHEMA,
}
