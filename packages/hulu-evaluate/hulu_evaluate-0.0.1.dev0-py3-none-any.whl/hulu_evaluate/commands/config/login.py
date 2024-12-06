from .config_utils import SubcommandHelpFormatter
import requests
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs


description = "Login to the HuLu evaluate service."

# Constants for OAuth
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
        print(f"Access token: {access_token}")
    else:
        print("Failed to obtain access token.")


def login_command_parser(parser, parents):
    parser = parser.add_parser("login", parents=parents, help=description, formatter_class=SubcommandHelpFormatter)

    return parser