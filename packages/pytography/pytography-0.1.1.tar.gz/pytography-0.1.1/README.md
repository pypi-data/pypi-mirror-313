# Pytography

A Python library that provides secure password hashing and JSON Web Token (JWT) functionality.

## Installation

```bash
pip install pytography
```
## Quick Start
### Password Hashing with Scrypt (Default)
```python
from pytography import PasswordHashLibrary

encoded_password = PasswordHashLibrary.encode(password="password")
is_valid = PasswordHashLibrary.verify(password="password", encoded_password=encoded_password)
```

### Password Hashing with PBKDF2
```python
from pytography import PasswordHashLibrary

encoded_password = PasswordHashLibrary.encode(password="password", algorithm="pbkdf2")
is_valid = PasswordHashLibrary.verify(password="password", encoded_password=encoded_password)
```

### JSON Web Token (JWT)
```python
from pytography import JsonWebToken
from datetime import datetime, timedelta, UTC

now = datetime.now(UTC)
exp = (now + timedelta(seconds=7200)).timestamp()

# Create a token
token = JsonWebToken.encode(payload={"exp": exp, "user_id": 123}, key="key")

# Decode token to get payload
header, payload, signature = JsonWebToken.decode(token=token)

# Verify token
is_valid = JsonWebToken.verify(token=token, key="key")
```

## License
This project is licensed under the terms of the LICENSE file included in the repository.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


