# cheers to Andrei Tchijov https://github.com/leapingbytes

import os
from enum import Enum
from typing import Optional


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Stacks(str, ExtendedEnum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'


class Vars(str, ExtendedEnum):
    STACK = 'STACK'
    TEST1 = "TEST1"
    TEST2 = "TEST2"


CONFIGURATION = {
    Stacks.DEV: {
        Vars.TEST1: 'SET WHATEVER YOU WANT FOR DEV',
        Vars.TEST2: 'SET WHATEVER YOU WANT FOR DEV'
    },
    Stacks.TEST: {
        Vars.TEST1: 'SET WHATEVER YOU WANT FOR TEST',
        Vars.TEST2: 'SET WHATEVER YOU WANT FOR TEST'
    },
    Stacks.PROD: {
        Vars.TEST1: 'SET WHATEVER YOU WANT FOR PROD',
        Vars.TEST2: 'SET WHATEVER YOU WANT FOR PROD'
    }
}

ASSIGNED_STACK: Optional[Stacks] = None


def assign_stack(stack: Optional[Stacks]):
    global ASSIGNED_STACK
    ASSIGNED_STACK = stack


def get_stack() -> Stacks:
    if ASSIGNED_STACK is not None:
        return ASSIGNED_STACK
    if Vars.STACK.value not in os.environ:
        return Stacks.DEV
    else:
        return Stacks(os.environ[Vars.STACK.value])


def get_config(var) -> str:
    stack = get_stack()
    return get_config_for_stack(stack, var)


def get_config_for_stack(stack, var) -> str:
    if var.value not in os.environ:
        if var not in CONFIGURATION[stack]:
            raise Exception(f"Invalid configuration: missing environment variable '{var}'")
        else:
            return CONFIGURATION[stack][var]
    else:
        return os.environ[var.value]
