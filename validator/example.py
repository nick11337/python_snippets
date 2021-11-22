from datetime import datetime
from enum import Enum
from typing import List, TypedDict, Optional, Dict

from validator import is_optional_enum, is_optional_datetime, is_optional_not_empty_string, \
    is_optional_email, is_defined_string, is_optional_bool, is_optional_date_in_past, sanitize, validate_and_raise, validate


class ExampleCustomer(TypedDict):
    username: str
    email: str
    firstname: str
    lastname: str
    birthday: str
    gender: str
    telephone_number: str

    another_id: str
    another_id2: str
    ofc_number: str

    hashed_password: str


CUSTOMER_SANITIZER = {
    'username': [is_optional_not_empty_string()],
    'email': [is_optional_email()],
    'firstname': [is_optional_not_empty_string()],
    'lastname': [is_optional_not_empty_string()],
    'birthday': [is_optional_date_in_past('%Y-%m-%d')],
    'telephone_number': [is_optional_not_empty_string()],
    'another_id': [is_optional_not_empty_string()],
    'another_id2': [is_optional_not_empty_string()],
    'hashed_password': [is_optional_not_empty_string()]
}

example_customer_valid = ExampleCustomer(
    username="User123",
    email="test@test.de",
    firstname="Nick",
    lastname="Meier",
    birthday="1994-01-01",
    telephone_number="1234567",
    another_id="1234",
    another_id2="12345",
    hashed_password="HashFOR123"
)
example_customer_invalid = ExampleCustomer(
    username="User123",
    email="testtest.de",  # Wrong mail-format
    firstname="Nick",
    lastname="Meier",
    birthday="1994-01-01",
    telephone_number="1234567",
    another_id="1234",
    another_id2="12345",
    hashed_password=""  # Not allowed to be empty
)


print(sanitize(example_customer_valid, CUSTOMER_SANITIZER))
print(sanitize(example_customer_invalid, CUSTOMER_SANITIZER))

print(validate(example_customer_valid, CUSTOMER_SANITIZER))
print(validate(example_customer_invalid, CUSTOMER_SANITIZER))

print(validate_and_raise(example_customer_valid, CUSTOMER_SANITIZER))
print(validate_and_raise(example_customer_invalid, CUSTOMER_SANITIZER))

