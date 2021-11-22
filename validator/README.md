<h1>Validate incoming data with several rules</h1>

This functions are used to either sanitize, validate or validate_and_raise incoming data with applied rules.

Functions:
- ```sanitize()```
  - This function checks the values of different keys with the applied rules. If any rule is not satisfied the key is getting removed and the "clean" dictionary is returned.
- ```validate()```
  - This function checks the values of the different keys with the applied rules and returns a dictionary of the keys with the error_messages if any rule is not satisfied. Otherwise it returns ```{}```
- ```validate_and_raise()```
  - This function checks the values of the different keys with the applied rules and raises an error if any rule is not satisfied. The exceptions can be modified in the validator.py at the top.
<hr>
  
**How to use:**

In the ```example.py``` you can find different examples. I created one VALID and one INVALID customer.
```py 
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
```
Afterwards all three functions are used:
```py
print(sanitize(example_customer_valid, CUSTOMER_SANITIZER))
print(sanitize(example_customer_invalid, CUSTOMER_SANITIZER))
```
The first function just returns the full example_customer_valid, because all rules are satisfied. The second sanitize function returns the customer without the fields email and hashed_password.```py
```py
print(validate(example_customer_valid, CUSTOMER_SANITIZER))
print(validate(example_customer_invalid, CUSTOMER_SANITIZER))
```
The first validate function returns an empty dictionary, because all rules are satisfied. The second validate function returns a dictionary with the keys email and hashed_passwords and the value is the error_message of the rule.

```py
print(validate_and_raise(example_customer_valid, CUSTOMER_SANITIZER))
print(validate_and_raise(example_customer_invalid, CUSTOMER_SANITIZER))
```
The first validate_and_raise function returns None, because all rules are satisfied. The second validate_and_raise function raises an error.

