## Welcome to "Hello World" with GitHub Actions

JattMones' experimentation with github actions and python.

### Pre-reqs
- Have python3 installed on your device.
- Have python and pip properly configured, available to use the internet.

### Adding your python virtual environment (.venv) and packages.

1. From repo root run `python -m venv .venv`
  - Verify the `.venv` folder was created
2. Nested within the `.venv` folder there should be a `.activate` file.
  - Windows: `Scripts\Activate` Mac/Ubuntu: `bin/activate`
3. Execute this script from your terminal (you should see `(.venv)` appended to the beginning of you cwd in the terminal)
4. Run `pip install -r requirements.txt`

Congrats! You've now successfully set-up your python virtual environment.

### Our python action
Our python action will follow the below steps:
1. Run pylint against all python test files
2. Run our pytest suite

### Our pytest suite
[Pytest docs]()
1. Our pytest configuration is defined in `conftest.py`
2. All tests within the tests folder are executed
