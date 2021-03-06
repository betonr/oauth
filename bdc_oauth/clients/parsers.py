"""
validation of client controllers schemas
"""

from datetime import datetime
from cerberus import Validator

def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d') if s else None

def client_base():
    return {
        'client_name': {"type": "string", "empty": False, "required": True},
        'client_secret': {"type": "string", "empty": False, "required": True},
        'type_secret': {"type": "string", "empty": False, "required": True, "allowed": ["file", "string"]},
        'client_uri': {"type": "string", "empty": False, "required": True},
        'redirect_uri': {"type": "string", "empty": False, "required": True}
    }

def date_expiration():
    return {
        'expired_at': {"type": "date", "coerce": to_date, "required": False, "empty": True}
    }

def client_create():
    return dict(client_base(), **date_expiration())


def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True
