# securify

**Secure and robust input handling for Python applications.**

`securify` is a lightweight library designed to make user interactions more secure. 
Its primary goal is to provide reliable ways to capture sensitive information, like 
passwords, while enforcing strict security constraints.

## Key Features

* **Security First:** Enforces interactive terminal (TTY) usage to prevent insecure 
    input processing.
* **Bot Protection:** Built-in time delay checks to prevent automated script 
    attacks.
* **Double-Entry Verification:** Simple logic to ensure users enter identical 
    passwords.
* **Developer Friendly:** Fully type-hinted, 100% test coverage, and clean 
    exception hierarchies.

## Installation

```bash
pip install .
```

## Quick Start

The core of the library is the `PasswordDoubleCheck` class. It ensures that a 
password is typed correctly twice and that the user is actually sitting at a 
terminal.

```python
from securify.input.password import PasswordDoubleCheck
from securify.input.exceptions import PasswordError

# Initialize with a 1.5-second minimum delay
checker = PasswordDoubleCheck(min_delay=1.5)

try:
    password = checker()
    print("Password successfully verified!")
except PasswordError as e:
    # Handles Mismatch, Speed, or Terminal errors
    print(f"Verification failed: {e}")
```

## Technical Background: Why TTY?

By default, `securify` rejects input that does not come from a real terminal. This 
ensures that the tool **only processes input from a secure, interactive source**. 

If the input is provided through a pipe or another non-interactive process, the 
checker will reject the operation. This prevents the application from being used in 
insecure workflows where passwords might be handled through unsafe channels.

## Development

`securify` is built with a focus on stability and cross-version compatibility. It 
is tested against Python 3.11 up to 3.15-alpha.

### Running Tests
We use `tox` to manage environments and `pytest` for testing:

```bash
tox
```

### Building Documentation
The documentation is built with Sphinx:

```bash
cd doc
make html
```

## License
LGPLv2 or above.
