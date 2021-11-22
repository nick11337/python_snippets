<h1>Set different environment variables</h1>

This is a useful small function to set different variables/constants for different environments,
for example in a pipeline that deploys code to several environments.

Dev -> Test -> Prod


**How to use:**
- in the env.py file you can set the different stacks or environments just by adding a new row
```py
  class Stacks(str, ExtendedEnum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
  ```
- in Vars you can set the variables that are used in the different environments. Just add a new one in CAPSLOCK like in the example. 
```py
  class Vars(str, ExtendedEnum):
    STACK = 'STACK'
    TEST1 = 'TEST1'
    TEST2 = 'TEST2'
  ```
- in the CONFIGURATION you can add the actual value of the variable in the different environments.
```py
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
```
- in the example.py there is an example how to use the variables. First you have to assign a stack, e.g. ```Stacks.DEV```. Afterwards you can get the value of the variable with ```get_config(Vars.TEST1)```. If you set the ```assign_stack``` dynamically you can work with all the variables in the different environments.
```py
from env import get_config, Vars, assign_stack, Stacks
assign_stack(stack=Stacks.DEV)
print(get_config(Vars.TEST1))
print(get_config(Vars.TEST2))
```