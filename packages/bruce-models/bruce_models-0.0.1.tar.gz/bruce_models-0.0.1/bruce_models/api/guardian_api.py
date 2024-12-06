import requests
from typing import Optional, Dict, TypedDict
import threading
from bruce_models import Api

class GuardianApiParams(TypedDict):
    """
    Represents the parameters for the Guardian API.
    """
    base_url: Optional[str]
    session_id: Optional[str]
    env: Optional[str]

class GuardianApi:
    """
    A basic API wrapper for making HTTP requests.
    """
    def __init__(self, params: GuardianApiParams):
        self._loading = True
        self._lock = threading.Lock()
        self._init(params)

    @property
    def loading(self) -> bool:
        return self._loading

    def _init(self, params):
        try:
            # If no env was supplied, set to PROD.
            self.env = params.get("env", "PROD")
            self.base_url = params.get("base_url")
            self.session_id = params.get("session_id")

            # If no base_url was supplied, we'll calculate it based on the env.
            if not self.base_url:
                if self.env == "DEV":
                    self.base_url = "https://guardian.nextspace-dev.net/"
                elif self.env == "STG":
                    self.base_url = "https://guardian.nextspace-stg.net/"
                elif self.env == "UAT":
                    self.base_url = "https://guardan.nextspace-uat.net/"
                else:
                    self.base_url = "https://guardian.nextspace.host/"
            
            self._loading = False
        except Exception as e:
            self._loading = False
            raise e

    def set_session_id(self, session_id: str):
        """
        Sets the x-sessionid header for all future requests.
        """
        self.session_id = session_id

    def get_env(self):
        """
        Returns the current environment.
        """
        return self.env

    def _build_headers(self) -> Dict[str, str]:
        """
        Builds the headers for all requests that are sent.
        """
        headers = {
            "Content-Type": "application/json"
        }
        if self.session_id:
            headers["x-sessionid"] = self.session_id
        return headers

    def get(self, url: str) -> Dict:
        """
        Sends a GET request to the API.
        The URL should be absolute.
        """
        self._wait_for_loading()
        response = requests.get(url, headers=self._build_headers())
        return Api.parse_result(response)

    def GET(self, url: str) -> Dict:
        """
        Sends a GET request to the API.
        The URL should be relative to the base URL.
        """
        self._wait_for_loading()
        full = f"{self.base_url}/{url.lstrip('/')}"
        return self.get(full)
    
    def _wait_for_loading(self):
        """
        Blocks further requests until the loading state is set to False.
        This method will prevent further requests until initialization is complete.
        """
        with self._lock:
            while self._loading:
                pass