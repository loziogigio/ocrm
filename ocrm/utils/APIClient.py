from bs4 import BeautifulSoup  # make sure to install this library, it's not included in Python's standard library
import requests
from requests.exceptions import RequestException

class LaravelAPIService:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "http://ocm.offerte-crociere.com"
        self.csrf_token = "xvhP1MrRvUjdGa3PFglh3rPNqJMecUqprT8NzrsZ"

        self.session.cookies.set("XSRF-TOKEN", "eyJpdiI6IlZ6OWdFMEtvRW1qTjZqbXp1MFlWcGc9PSIsInZhbHVlIjoickxzSnJVcEIrWkhOaUoxSzVSb3dldzM4XC9nTFM0V1lCSlNSSnlhcEFSZGdmK2FWMEhJdVk1WWdFRmNYT2dSMzhrcTVaU2k4NTBnUitnYXZcL05vNWhXZz09IiwibWFjIjoiNTA1NmRiZThjYmUyMDAxOTUxZTNhMTU0MjA0NjdhNzFkYmQ3NTgzOTFkY2Y0ZTM0MDljYThiODIyOTAyNDczMiJ9")
        self.session.cookies.set("laravel_session","eyJpdiI6IjlQb0d4R2lPWDQ1bXJrXC93eWdNZWV3PT0iLCJ2YWx1ZSI6IitLMjJrdXYrd1wvRk5Fa2wxSng5b1gxQ2JzaTZ4enhwcDNFU3A5T3VQZTRwXC9IdkZ3SzFnUHRKaHVsdUk5TkZFd1VBS3RhUFdDSUJWcW5DR2VHSDdidlE9PSIsIm1hYyI6IjVmYmQwY2JmYTFhOWI2NTVjNTc0YjBlYjUyMmVhYjdjMTFiMjllYzZhZTNmMDhmNmIwMTg4NDVkYWFkYmQ3YjIifQ%3D%3D");

    def make_request(self,  method='GET',url="/", data=None):
        
        """
        General method for making authenticated requests to the Laravel API.
        """
        if not self.csrf_token:
            raise Exception("Session is not authenticated.")


        headers = {
            'X-CSRF-TOKEN': self.csrf_token,  # Include CSRF token in the headers for authenticated requests
            # Add other necessary headers
        }

        response = self.session.request(method,  self.base_url+url, json=data, headers=headers)

        # Handle the response (e.g., check status code, parse response body)
        if response.ok:
            return response.json()  # Adjust based on the expected response format
        else:
            response.raise_for_status()

    # Define other methods as needed for various API endpoints