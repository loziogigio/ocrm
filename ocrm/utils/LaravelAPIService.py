from bs4 import BeautifulSoup  # make sure to install this library, it's not included in Python's standard library
import requests
from requests.exceptions import RequestException

class LaravelAPIService:
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url
        self.csrf_token = self._get_csrf_token()


    def _get_csrf_token(self,url =""):
        """
        Retrieve CSRF token by parsing the HTML content of a given page of the Laravel app.
        """
        response = self.session.get(f"{url}")  # this could be the login page or any page that contains CSRF token
        
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            # If the CSRF token is in a hidden input, you'd find it like this:
            hidden_input = soup.find('input', {'name': '_token'})
            
            if hidden_input:
                return hidden_input.get('value')
            else:
                raise ValueError("Unable to find CSRF token in HTML.")
        else:
            response.raise_for_status()

    def login_to_laravel(self, username, password):
        """
        Login to the Laravel API and handle CSRF token.
        """
        login_url = f"{self.base_url}/login"
        self.csrf_token = self._get_csrf_token(login_url)  # Make sure we have a fresh token

        if not self.csrf_token:
            raise Exception("Could not retrieve CSRF token.")

        # In some cases, the CSRF token needs to be sent within form data during login
        payload = {
            '_token': self.csrf_token,  # Laravel expects the CSRF token in the payload with the name '_token'
            'username': username,  # Adjust these payload entries to match your actual login form fields
            'password': password,
        }

        response = self.session.post(login_url, data=payload)  # Using 'data' instead of 'json' to match typical form submission

        if not response.ok:
            response.raise_for_status()  # Will provide more detail on why the login failed

    def make_request(self,  url, data=None):
        """
        General method for making authenticated requests to the Laravel API.
        """
        if not self.csrf_token:
            raise Exception("Session is not authenticated.")


        headers = {
            'X-CSRF-TOKEN': self.csrf_token,  # Include CSRF token in the headers for authenticated requests
            # Add other necessary headers
        }

        response = self.session.request( self.base_url+url, json=data, headers=headers)

        # Handle the response (e.g., check status code, parse response body)
        if response.ok:
            return response.json()  # Adjust based on the expected response format
        else:
            response.raise_for_status()

    # Define other methods as needed for various API endpoints