
# Leetcode Python Wrapper Python Library

A Python wrapper for the Alfa LeetCode API, providing endpoints to retrieve user profiles, badges, solved problems, and more.

## Features
- Fetch user profile, badges, solved problems, and contest details.
- Query problems with filters (tags, difficulty).
- Retrieve trending discussions and daily questions.

## Installation

Install using pip:

```bash
pip install leetcode-api-wrapper
```

## Usage

```python
from LeetcodeWrapper import leetcode_Wrapper

api = leetcode_Wrapper("test_user")

# Get profile details
profile = api.get_profile()
print(profile)
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.




