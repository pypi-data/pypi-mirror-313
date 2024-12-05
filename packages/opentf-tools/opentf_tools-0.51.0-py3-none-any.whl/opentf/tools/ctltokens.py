# Copyright 2021-2023 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl"""

from typing import Any, Dict, List, Optional, Union

import os
import sys

from datetime import datetime

import jwt

from opentf.tools.ctlcommons import (
    _is_command,
    _get_arg,
    _error,
    _fatal,
    _warning,
    _ensure_options,
)

########################################################################

# pylint: disable=broad-except


########################################################################
# Help messages

GENERATE_TOKEN_HELP = '''Generate a signed token

Examples:
  # Generate token interactively
  opentf-ctl generate token using path/to/private.pem

  # Generate a non-expiring token non-interactively
  opentf-ctl generate token using path/to/private.pem --algorithm=RS512 --issuer=acme --suject=alice --expiration='' --output-file=alice.token

Options:
  --algorithm=algo: the algorithm to use (required)
  --issuer=issuer: the token issuer (required)
  --subject=subject: the token subject (required)
  --expiration=exp: the token expiration date, empty ('') if the token should not expire, in YYYY/MM/DD format otherwide (required)
  --output-file=o: the output file (default: stdout)

Usage:
  opentf-ctl generate token using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VIEW_TOKEN_HELP = '''View token payload

Example:
  # Display token payload
  opentf-ctl view token $TOKEN

Usage:
  opentf-ctl view token TOKEN [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VALIDATE_TOKEN_HELP = '''Validate token signature

Example:
  # Validate token
  opentf-ctl check token $TOKEN using path/to/public.pub

Usage:
  opentf-ctl check token TOKEN using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# JWT tokens

ALLOWED_ALGORITHMS = [
    'ES256',  # ECDSA signature algorithm using SHA-256 hash algorithm
    'ES384',  # ECDSA signature algorithm using SHA-384 hash algorithm
    'ES512',  # ECDSA signature algorithm using SHA-512 hash algorithm
    'RS256',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
    'RS384',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
    'RS512',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
    'PS256',  # RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
    'PS384',  # RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
    'PS512',  # RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512
]


def _load_pem_private_key(privatekey: str) -> Any:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    from cryptography.exceptions import UnsupportedAlgorithm

    try:
        with open(privatekey, 'rb') as keyfile:
            pem = keyfile.read()
        try:
            return serialization.load_pem_private_key(pem, None, default_backend())
        except ValueError as err:
            _fatal(
                'This does not seem to be a valid private key in PEM format: %s.', err
            )
        except TypeError:
            from getpass import getpass

            try:
                passphrase = getpass(
                    'This private key is encrypted, please enter the passphrase: '
                )
                if not passphrase:
                    _fatal('Passphrase cannot be empty, the private key is encrypted.')
                return serialization.load_pem_private_key(
                    pem, passphrase.encode('utf-8'), backend=default_backend()
                )
            except ValueError as err:
                _fatal(str(err))
    except UnsupportedAlgorithm as err:
        _fatal(
            'The serialized key type is not supported by the OpenSSL version "cryptography" is using: %s.',
            err,
        )
    except IsADirectoryError:
        _fatal(
            'The specified private key must be a file, not a directory: %s.', privatekey
        )
    except FileNotFoundError:
        _fatal('The specified private key could not be found: %s.', privatekey)


def _get_input(
    long: str, short: str, default: Optional[str] = None, required: bool = False
) -> str:
    value = _get_arg(f'--{short}=')
    if value is None:
        value = input(long) or None
    if value is None and default:
        value = default
    if required and value is None:
        while not value:
            _warning(f'The {short} cannot be empty.')
            value = input(long)
    return (value or '').strip()


def _generate_token(privatekey: str) -> None:
    private_key = _load_pem_private_key(privatekey)
    algorithm = _get_input(
        'Please specify an algorithm (RS512 if unspecified): ',
        'algorithm',
        default='RS512',
    )
    print('The specified algorithm is:', algorithm)
    issuer = _get_input(
        'Please enter the issuer (your company or department): ',
        'issuer',
        required=True,
    )
    subject = _get_input(
        'Please enter the subject (you or the person you are making this token for): ',
        'subject',
        required=True,
    )
    exp = _get_input(
        'Please specify an expiration date in YYYY/MM/DD format (never if unspecified): ',
        'expiration',
    )
    if exp:
        try:
            exp = int(datetime.strptime(exp, '%Y/%m/%d').timestamp())
        except ValueError:
            _fatal('Invalid expiration date format, must be YYYY/MM/DD.')

    try:
        payload: Dict[str, Union[str, int]] = {'iss': issuer, 'sub': subject}
        if exp:
            payload['exp'] = exp
        token = jwt.encode(payload, private_key, algorithm=algorithm)
    except NotImplementedError:
        _fatal('Algorithm not supported: %s.', algorithm)
    except Exception as err:
        _fatal('Could not generate token: %s.', err)

    if outputfile := _get_arg('--output-file='):
        if os.path.exists(outputfile) and (
            input('The output file already exists.  Overwrite? (y/n): ').lower() != 'y'
        ):
            _fatal('Aborted')
        print('Writing token to:', outputfile)
        with open(outputfile, 'w', encoding='utf-8') as outfile:
            outfile.write(token)
    else:
        print('The signed token is:')
        print(token)


def generate_token(privatekey: str) -> None:
    """Generate JWT token.

    Optional command-line options

    --algorithm ALGORITHM: the algorithm to use (default: RS512)
    --issuer ISSUER: the issuer
    --subject SUBJECT: the subject
    --expiration EXPIRATION: the expiration date in YYYY/MM/DD format
    --output-file FILE

    # Required parameters

    - privatekey: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        _generate_token(privatekey)
    except KeyboardInterrupt:
        print('^C')
        sys.exit(1)


def view_token(token: str) -> None:
    """View JWT token payload.

    # Required parameters

    - token: a non-empty string (a JWT token)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        print('The token payload is:')
        if 'exp' in payload:
            payload['exp'] = datetime.fromtimestamp(payload['exp']).strftime('%Y/%m/%d')
        print(payload)
    except Exception as err:
        _error('The specified token is invalid: %s', err)
        print(token)
        sys.exit(2)


def check_token(token: str, keyname: str) -> None:
    """Check JWT token signature.

    # Required parameters

    - token: a non-empty string (a JWT token)
    - keyname: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(keyname, 'r', encoding='utf-8') as keyfile:
            key = keyfile.read()
    except IsADirectoryError:
        _fatal('The specified public key must be a file, not a directory: %s.', keyname)
    except FileNotFoundError:
        _fatal('The specified public key could not be found: %s.', keyname)

    try:
        payload = jwt.decode(token, key, algorithms=ALLOWED_ALGORITHMS)
        print(
            f'The token is signed by the {keyname} public key.  The token payload is:'
        )
        print(payload)
    except jwt.exceptions.InvalidSignatureError:
        _error('The token is not signed by %s.', keyname)
        sys.exit(102)
    except (TypeError, AttributeError) as err:
        _fatal(
            'The specified key does not looks like a public key.'
            + '  Got "%s" while reading the provided key.',
            err,
        )
    except ValueError as err:
        _fatal(err.args[0])
    except Exception as err:
        _fatal('Could not validate token signature: %s.', err)


########################################################################
# Helpers


def print_tokens_help(args: List[str]) -> None:
    """Display help."""
    if _is_command('generate token', args):
        print(GENERATE_TOKEN_HELP)
    elif _is_command('view token', args):
        print(VIEW_TOKEN_HELP)
    elif _is_command('check token', args):
        print(VALIDATE_TOKEN_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


########################################################################
# Main


def tokens_cmd():
    """Process tokens command."""
    if _is_command('generate token using _', sys.argv):
        pem = _ensure_options(
            'generate token using _',
            sys.argv[1:],
            extra=[
                ('--algorithm',),
                ('--issuer',),
                ('--subject',),
                ('--expiration',),
                ('--output-file',),
            ],
        )
        generate_token(pem)
        sys.exit(0)
    if _is_command('view token _', sys.argv):
        if len(sys.argv) > 4:
            _fatal(
                f'"opentf-ctl view token" does not take options.  Got "{" ".join(sys.argv[4:])}".'
            )
        view_token(sys.argv[3])
        sys.exit(0)
    if _is_command('check token _ using _', sys.argv):
        if len(sys.argv) > 6:
            _fatal(
                f'"opentf-ctl check token" does not take options.  Got "{" ".join(sys.argv[6:])}".'
            )
        check_token(sys.argv[3], sys.argv[5])
        sys.exit(0)
    if _is_command('check token _', sys.argv):
        _fatal('Missing required parameter.  Use "check token --help" for details.')
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
