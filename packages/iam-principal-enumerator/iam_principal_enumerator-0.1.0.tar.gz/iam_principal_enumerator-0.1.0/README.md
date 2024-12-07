# IAM Principal Enumerator

CLI application that performs unauthenticated IAM principal enumeration against a target AWS account.

The application accepts a custom wordlist containing principal names, and uses these to check for the existence of IAM principals in a target AWS account by attempting to update the trust policy of an attacker-controlled IAM role with the ARN of an IAM principal (user or role) in the target AWS account.

The error message received when updating the trust policy will determine if the IAM princiapl exists in the target account or not.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Examples](#examples)
- [License](#license)

## Installation

1. Install the package using `pip`:

```sh
pip install iam-principal-enumerator
```

## Usage

To run the IAM Principal Enumerator, **ensure your terminal session is authenticated to your own attacker-controlled AWS account**, then use the following command:

```sh
iam-principal-enumerator <account_id> [options]
```

### Options

```plain
usage: iam-principal-enumerator [-h] [-r ENUM_ROLE_NAME] [-w WORDLIST] account_id

Enumerate valid IAM principals in an AWS account.

positional arguments:
  account_id            The target AWS account ID

options:
  -h, --help            show this help message and exit
  -r ENUM_ROLE_NAME, --enum-role-name ENUM_ROLE_NAME
                        The name of the IAM role used for enumeration. The role name will
                        be suffixed with an 8-character random string.
  -w WORDLIST, --wordlist WORDLIST
                        Path to a wordlist to use when enumerating IAM principal names.
```

### Examples

Enumerate IAM principals using the default role name and wordlist:

```sh
iam-principal-enumerator 123456789012
```

Enumerate IAM principals using a custom role name and wordlist:

```sh
iam-principal-enumerator 123456789012 -r CustomRole -w /path/to/wordlist.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
