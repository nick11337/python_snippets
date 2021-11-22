import logging
from datetime import datetime
from typing import Callable, Dict, List, Tuple, Any

import json
from validators.email import email as valid_email
from validators.url import url as valid_url


class ExampleException(Exception):
    def __init__(self, error_code: int = None, error_message: str = 'Error', exception: Exception = None):
        if exception is None:
            self._error_code = error_code
            self._error_message = error_message
        else:
            self._error_code = 500
            self._error_message = f'{type(exception).__name__} - {exception}'

        logging.warning(f'ExampleException : {self._error_message}')

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_message(self) -> str:
        return self._error_message


class InvalidRequest(ExampleException):
    def __init__(self, validation_results: Dict):
        super().__init__(400, error_message=self.message_from_dictionary(validation_results))

    @staticmethod
    def message_from_dictionary(validation_results: Dict):
        return list(validation_results.items())[0][1][0]['message']


def is_defined_bool():
    def validate_it(key, v):
        return _ok() if v is not None and isinstance(v, bool) else _error(f'{key} should be set and boolean')

    return validate_it


def is_true_bool():
    def validate_it(key, v):
        return _ok() if v is True else _error(f'{key} should be set to True')

    return validate_it


def is_false_bool():
    def validate_it(key, v):
        return _ok() if v is True else _error(f'{key} should be set to False')

    return validate_it


def is_defined_string():
    def validate_it(key, v):
        return _ok() if v is not None and isinstance(v, str) else _error(f'{key} should be set and string')

    return validate_it


def is_not_empty_string():
    def validate_it(key, v):
        return _ok() if isinstance(v, str) and len(v) > 0 else _error(f'{key} should be non-empty string')

    return validate_it


def is_optional_not_empty_string():
    def validate_it(key, v):
        return _ok() if v is None or (isinstance(v, str) and len(v) > 0) else _error(
            f'{key} should be non-empty string')

    return validate_it


def is_optional_number():
    def safe_int(v: Any) -> int:
        try:
            return int(v)
        except ValueError:
            return 0

    def validate_it(key, v):
        return _ok() if v is None or str(v) == str(safe_int(v)) else _error(f'{key} should be integer number')

    return validate_it


def is_optional_bool():
    def safe_bool(v: Any) -> bool:
        try:
            return bool(v)
        except ValueError:
            return False

    def validate_it(key, v):
        return _ok() if v is None or str(v) == str(safe_bool(v)) else _error(f'{key} should be boolean')

    return validate_it


# 2021-07-02T06:01:53.781835+00:00

def is_datetime(expected_format: str = '%Y-%m-%dT%H:%M:%S.%f%z'):
    def parse_datetime(v: str):
        try:
            return datetime.strptime(v, expected_format) if v is not None else None
        except ValueError:
            return None

    def validate_it(key, v):
        date = parse_datetime(v)
        return _ok() if v is not None and date is not None else _error(f'{key} should be valid datetime')

    return validate_it


def is_optional_datetime(expected_format: str = '%Y-%m-%dT%H:%M:%S.%f%z'):
    def parse_datetime(v: str):
        try:
            return datetime.strptime(v, expected_format) if v is not None else None
        except ValueError:
            return None

    def validate_it(key, v):
        date = parse_datetime(v)
        return _ok() if v is None or date is not None else _error(f'{key} should be valid datetime')

    return validate_it


def is_date_in_past(expected_format: str = '%Y-%m-%d'):
    def parse_date(v: str):
        try:
            return datetime.strptime(v, expected_format) if v is not None else None
        except ValueError:
            return None

    def validate_it(key, v):
        date = parse_date(v)
        return _ok() if date is not None and (date < datetime.now()) else _error(f'{key} should be valid date in past')

    return validate_it


def is_optional_date_in_past(expected_format: str = '%Y-%m-%d'):
    def parse_date(v: str):
        try:
            return datetime.strptime(v, expected_format) if v is not None else None
        except ValueError:
            return None

    def validate_it(key, v):
        date = parse_date(v)
        return _ok() if v is None or (date is not None and date < datetime.now()) else _error(
            f'{key} should be valid date in past')

    return validate_it


def is_enum(enum_cls):
    def is_valid_enum(v):
        try:
            enum_cls(v)
            return True
        except ValueError:
            return False

    def validate_it(key, v):
        return _ok() if is_valid_enum(v) else _error(f'{key} should be valid {enum_cls.__name__}')

    return validate_it


def is_optional_enum(enum_cls):
    def is_valid_enum(v):
        try:
            enum_cls(v)
            return True
        except ValueError:
            return False

    def validate_it(key, v):
        return _ok() if v is None or is_valid_enum(v) else _error(f'{key} should be valid {enum_cls.__name__}')

    return validate_it


def is_equal(value: str):
    def validate_it(key, v):
        return _ok() if v == value else _error(f'{key} should be equal {value}')

    return validate_it


def is_positive_number():
    def validate_it(key, v):
        return _ok() if int(v) > 0 else _error(f'{key} should be positive number')

    return validate_it


def is_valid_email():
    def validate_it(key, v):
        return _ok() if isinstance(v, str) and valid_email(v) else _error(f'{key} should be valid e-mail address')

    return validate_it


def is_optional_email():
    def validate_it(key, v):
        return _ok() if v is None or (isinstance(v, str) and valid_email(v)) else _error(
            f'{key} should be valid e-mail address')

    return validate_it


def is_valid_uri():
    def validate_it(key, v):
        return _ok() if isinstance(v, str) and valid_url(v) else _error(f'{key} should be valid URL')

    return validate_it


def validate(target: dict, rules: Dict[str, List[Callable[[any], bool]]]) -> Dict[str, str]:
    return _flatten(_apply_rules(target, rules))


def validate_and_raise(target: dict, rules: Dict[str, List[Callable[[any], bool]]]):
    logging.info(f"Validating: {json.dumps(target)}")

    result = validate(target, rules)

    if len(result) > 0:
        raise InvalidRequest(result)


def sanitize(target: dict, rules: Dict[str, List[Callable[[any], bool]]]) -> dict:
    logging.info(f"sanitizing: {json.dumps(target)} \n {rules}")
    sanitized_target = target.copy()

    for target_key in list(sanitized_target.keys()):
        if target_key not in rules.keys():
            logging.warning(f'sanitize : unexpected key found {target_key}')
            del sanitized_target[target_key]

    result = validate(sanitized_target, rules)

    if len(result) == 0:
        return target

    for key in result:
        top_level_key = key.split('.')[0]
        logging.warning(
            f'sanitize : invalid value found {key} = {sanitized_target.get(key)} : {json.dumps(result.get(key))}')
        if top_level_key in sanitized_target:
            del sanitized_target[top_level_key]

    return sanitized_target


def _apply_rules(target: dict, rules: Dict[str, List[Callable[[any], bool]]]) -> List[Tuple[Any, List[Dict[str, str]]]]:
    if target is None:
        return []
    return list(
        map(
            lambda x:
            (x[0],
             _apply_all_validations(target, x[0], x[1]) if isinstance(x[1], List) else _apply_rules(target.get(x[0]),
                                                                                                    x[1])),
            rules.items()
        ))


def _apply_all_validations(target: dict, key: str, validations: List[Callable[[str, any], bool]]) -> List[
    Dict[str, str]]:
    return list(filter(
        lambda result: result['error'],
        map(
            lambda validation:
            validation(key, target.get(key)),
            validations
        )))


def _ok():
    return {'error': False}


def _error(message: str):
    return {
        'error': True,
        'message': message,
    }


# Borrowed from https://stackoverflow.com/a/6027615
def _flatten(d: List, parent_key='', sep='.') -> Dict:
    items = []
    for k, v in d:
        new_key = parent_key + sep + k if parent_key else k
        if len(v) == 0:
            pass
        elif isinstance(v[0], Tuple):
            items.extend(_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
