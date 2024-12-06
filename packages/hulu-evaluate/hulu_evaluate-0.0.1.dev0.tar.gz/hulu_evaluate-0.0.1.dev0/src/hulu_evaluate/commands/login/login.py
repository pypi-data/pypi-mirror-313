import argparse
from urllib.parse import urlencode, urlparse, parse_qs

CLIENT_ID = '511275226645-8u3bnb947hag0a8okcu7vbbkvqtjthqb.apps.googleusercontent.com'
REDIRECT_URI = 'https://hulu.nytud.hu/accounts/google/login/callback/'
SCOPE = 'email profile'
RESPONSE_TYPE = 'token'
STATE = 'n5fv8s4SI3Mg'  # Example state token

# This is the base URL for Google's OAuth authorization endpoint
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'


def get_auth_url():
    """Constructs the Google OAuth implicit flow URL."""
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': RESPONSE_TYPE,
        'scope': SCOPE,
        'state': STATE
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    return auth_url


def extract_access_token_from_url(redirect_response):
    """Extracts the access token from the redirect URL."""
    # Parse the URL fragment (part after '#')
    parsed_url = urlparse(redirect_response)
    fragment_params = parse_qs(parsed_url.fragment)

    # Extract the access token from the fragment parameters
    access_token = fragment_params.get('access_token', [None])[0]
    
    if access_token:
        print(f"Access token obtained: {access_token}")
    else:
        print("Error: No access token found.")
    
    return access_token


def handle_oauth_flow():
    """Handles the implicit OAuth flow to obtain a bearer token."""
    # Step 1: Get the authorization URL and ask the user to open it
    auth_url = get_auth_url()
    print("Please visit the following URL to log in:")
    print(auth_url)

    # Step 2: User will be redirected to the redirect URI after successful login.
    # The access token will be in the fragment part of the URL
    redirect_response = input("Paste the full redirect URL (after login) here: ")

    # Step 3: Extract the access token from the fragment
    access_token = extract_access_token_from_url(redirect_response)

    if access_token:
        return access_token


def login_command(args):
    """Handles the login command by calling the OAuth flow."""
    access_token = handle_oauth_flow()
    config_file = args.config_file
    if config_file:
        with open(config_file, 'w') as f:
            f.write(f"access_token: {access_token}")


def login_command_parser(subparsers=None):
    """Sets up the argument parser for the login command."""
    if subparsers is not None:
        parser = subparsers.add_parser("login", description='Lets you login to HuLu')
    else:
        parser = argparse.ArgumentParser("HuLu evaluate login command", description='Lets you login to HuLu')

    parser.add_argument(
        "--config_file",
        default=None,
        help=(
            "The path to use to store the config file. Will default to a file named default_config.yaml in the cache "
            "location, which is the content of the environment `HF_HOME` suffixed with 'accelerate', or if you don't have "
            "such an environment variable, your cache directory ('~/.cache' or the content of `XDG_CACHE_HOME`) suffixed "
            "with 'huggingface'."
        ),
    )

    # Set the function to execute for the 'login' command
    if subparsers is not None:
        parser.set_defaults(func=login_command)
    return parser
