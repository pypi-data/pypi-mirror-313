# pytest-fixture-forms

[![PyPI version](https://img.shields.io/pypi/v/pytest-fixture-forms)](https://pypi.org/project/pytest-fixture-forms/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-fixture-forms)](https://pypi.org/project/pytest-fixture-forms/)
![Pytest](https://img.shields.io/badge/pytest-7.x%20%7C%208.x-blue)

A powerful pytest plugin that simplifies testing different forms of parameters through dynamic fixture generation. This
plugin is particularly useful for API testing, integration testing, or any scenario where you need to verify behavior
across multiple parameter variations.

## Key Features

- Automatically generates fixtures based on class methods
- Supports dynamic test generation for parameter combinations
- Integrates seamlessly with pytest's parametrization
- Handles nested fixture dependencies elegantly
- Reduces boilerplate in test code

## Installation

Install from PyPI:

```bash
pip install pytest-fixture-forms
```

## Quick Start

Here's a simple example showing how to use pytest-fixture-forms:

```python
from pytest_fixture_forms import FixtureForms
import pytest


class UserCredentials(FixtureForms):
    @pytest.fixture
    def valid_user(self):
        return {"username": "john_doe", "password": "secure123"}

    @pytest.fixture
    def invalid_password(self):
        return {"username": "john_doe", "password": "wrong"}

    @pytest.fixture
    def missing_username(self):
        return {"username": "", "password": "secure123"}


def test_login(user_credentials):
    # This test will run for each form defined in UserCredentials
    response = login_service.authenticate(**user_credentials.value)

    if user_credentials.form == "valid_user":
        assert response.status_code == 200
    else:
        assert response.status_code == 401
```

## Understanding FixtureForms

When you create a class that inherits from `FixtureForms`, the plugin automatically generates several fixtures:

1. `<class_name_snake_case>` - Returns an instance containing the current form and value
2. `<class_name_snake_case>_form` - The name of the current form being tested
3. `<class_name_snake_case>_<form_name>` - The value for a specific form

For example, given a class named `ApiEndpoint`:

```python
class ApiEndpoint(FixtureForms):
    @pytest.fixture
    def get_users(self):
        return "/api/v1/users"

    @pytest.fixture
    def create_user(self):
        return "/api/v1/users/create"


def test_endpoint(api_endpoint):
    # api_endpoint.form will be either "get_users" or "create_user"
    # api_endpoint.value will be the corresponding URL
    response = client.request("GET", api_endpoint.value)
```

## Advanced Usage

### Combining Multiple Forms

You can use multiple `FixtureForms` classes in a single test to test combinations:

```python
class RequestMethod(FixtureForms):
    @pytest.fixture
    def get(self):
        return "GET"

    @pytest.fixture
    def post(self):
        return "POST"


class ApiPath(FixtureForms):
    @pytest.fixture
    def users(self):
        return "/users"

    @pytest.fixture
    def products(self):
        return "/products"


def test_api_combinations(request_method, api_path):
    # This will generate tests for all combinations:
    # GET /users
    # GET /products
    # POST /users
    # POST /products
    response = client.request(request_method.value, api_path.value)
```

### Using with Parametrization

You can control which forms to test using pytest's parametrize:

```python
@pytest.mark.parametrize("request_method_form", ["get"])  # Only test GET requests
@pytest.mark.parametrize("api_path_form", ["users", "products"])
def test_specific_combinations(request_method, api_path):
    response = client.request(request_method.value, api_path.value)
```

### Accessing Fixture Values

Each `FixtureForms` instance provides:

- `form` - The current form name
- `value` - The value returned by the current form's fixture
- `request` - The pytest fixture request object

### Working with Dependencies

Forms can depend on other fixtures:

```python
class AuthenticatedEndpoint(FixtureForms):
    @pytest.fixture
    def user_profile(self, auth_token):  # Depends on auth_token fixture
        return f"/api/v1/profile", {"Authorization": auth_token}


@pytest.fixture
def auth_token():
    return "Bearer xyz123"
```

## How It Works

The plugin uses pytest's collection hooks to:

1. Dynamically register fixtures based on `FixtureForms` class methods
2. Generate test nodes for each combination of parameters
3. Handle fixture dependencies and parametrization

## Best Practices

1. Keep form methods focused on a single variation
2. Use clear, descriptive names for forms
3. Group related forms in a single class
4. Consider using parametrization to control test combinations
5. Document expected behavior for each form

## Understanding Instance Fixtures Lifecycle

When you create a class that inherits from `FixtureForms`, the plugin generates several instance-related fixtures that
work together to provide a robust testing framework. Let's understand these fixtures and their relationships using an
example:

```python
class KeyId(FixtureForms):
    @pytest.fixture
    def arn(self):
        return "arn:aws:123"

    @pytest.fixture
    def id(self):
        return "123"
```

### Instance Fixture Hierarchy

For the `KeyId` class above, the following instance fixtures are created:

1. `key_id_initial_prototype`
    - The most basic instance fixture
    - Not parameterized
    - Neither `form` nor `value` are set
    - Used internally to create the base instance that will be passed to form methods
    - Useful when form methods or dependent fixtures need early access to the instance

2. `key_id_prototype`
    - Built from `key_id_initial_prototype`
    - Parameterized with forms ("arn", "id")
    - Has `form` set but no `value`
    - Used when you need access to the instance and form name before the value is computed
    - Helpful for fixtures that depend on the form but not the value

3. `key_id`
    - The final, fully initialized instance
    - Built from `key_id_prototype`
    - Has both `form` and `value` set
    - The value is computed by calling the corresponding form method
    - This is typically what you'll use in your tests

### Example: Working with Instance Fixtures

Here's how you might use different instance fixtures:

```python
class KeyId(FixtureForms):
    @pytest.fixture
    def arn(self, set_region):
        # self is an instance of KeyId with form="arn", and region="us-east-1" was set because we requested the set_region fixture
        return f"arn:aws:{self.region}"

    @pytest.fixture
    def id(self):
        return "123"


@pytest.fixture
def set_region(key_id_prototype):
    # We can access the form before the value is computed
    if key_id_prototype.form == "arn":
        key_id_prototype.region = "us-east-1"


def test_key_id(key_id):
    # key_id has both form and value set
    assert key_id.form in ["arn", "id"]
    if key_id.form == "arn":
        assert key_id.value == "arn:aws:us-east-1"
    else:
        assert key_id.value == "123"
```

### Instance Fixture Flow

The lifecycle of a `FixtureForms` instance follows this sequence:

1. `key_id_initial_prototype` creates the base instance
2. `key_id_prototype` sets the form based on parametrization
3. Form method is called with the prototype instance as `self`
4. `key_id` receives the computed value and becomes the final instance

This design allows for complex dependencies and interactions between fixtures while maintaining clarity and preventing
circular dependencies.

## Understanding test nodes generation

Take a look at [this example test](/testing/core/test_combinations.py). It demonstrates how the plugin handles complex
parameter combinations. The test uses 3 different parameters, each having 3 possible forms, resulting in 27 unique test
nodes (3 x 3 x 3 combinations).

What makes this plugin special is its handling of parametrized forms. When a form is parametrized, it only multiplies
the test nodes for that specific parameter form, not all combinations. This is different from pytest's standard
parametrization and is why we generate test nodes dynamically.

Why this approach? In standard pytest, when a fixture is parametrized within a test node, those parameters become
permanently linked to that node. This creates unwanted coupling between different parameter forms. By generating a
unique node for each combination of parameter forms, we avoid this coupling and maintain independence between different
parameter variations.

running the test would look like this:

![tmp](https://github.com/user-attachments/assets/101cb983-1027-4a50-ace5-92ffcd3a1a14)

## Advanced Customization

you can also create a base class that inherits from `FixtureForms` and add custom behavior:

```python
class AdvancedFixtureForms(FixtureForms):
    def __init__(self, *args, **kwargs):
        self.custom_form_property = None
        super().__init__(*args, **kwargs)
```
then in your tests:
```python 
class SomeFixtureForm(AdvancedFixtureForms):
    @pytest.fixture
    def form1(self, set_custom_form_property):
        assert self.custom_form_property == "custom form property value"
        return "1"


@pytest.fixture
def set_custom_form_property(some_fixture_form_prototype: SomeFixtureForm):
    some_fixture_form_prototype.custom_form_property = "custom form property value"


def test_advanced_fixture_forms(some_fixture_form: SomeFixtureForm):
    assert some_fixture_form.custom_form_property == "custom form property value"
    assert some_fixture_form.value == "1"
    print(some_fixture_form)
```

## Contributing

Contributions are welcome! This is a new project and there might be bugs or missing features. If you have any
suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.