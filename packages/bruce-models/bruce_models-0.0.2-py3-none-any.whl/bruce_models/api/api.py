import requests
from typing import Dict

class Api:
    @staticmethod
    def parse_result(result: requests.Response) -> Dict:
        """
        Parses the result of an API request to a Nextspace endpoint.
        """
        if result.status_code >= 400 or result.status_code < 200:
            error = result.json()
            raise Exception(error)
        
        # Technically, our API can return other types such as a raw CSV file.
        # However, it is very rare.
        # If we need to update this method, we can check for the type and wrap non-json (CSV) in a dict.

        return result.json()