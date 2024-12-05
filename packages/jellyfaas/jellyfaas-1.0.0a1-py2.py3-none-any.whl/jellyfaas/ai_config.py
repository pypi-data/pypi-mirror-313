import requests
import logging

from .exceptions import *

logger = logging.getLogger(__name__)

class AIConfig:

    # Member "consts"
    _AUTH_ENDPOINT:   str = "https://api.jellyfaas.com/auth-service/v1/validate"
    _HEADER_API_KEY:      str = "x-jf-apikey"

    # Member variables
    _api_key: str = None
    _token: str = None
    _token_expiry: str = None
    _do_debug = None

    

    def __init__(self, api_key: str, debug=False) -> None:
        self._do_debug = debug
        self.__auth(api_key)
    
    def __auth(self, api_key=None):
        """
        Authenticate with the JellyFAAS API using the provided API key.

        :param api_key The API key for JellyFAAS.
        :raises AuthenticationFailedException If authentication fails.
        """
        try:
            self.__debug(f"Starting __auth method with api_key={api_key}")
            
            self.__debug("Setting auth token")
            auth_response = requests.get(self._AUTH_ENDPOINT, headers={self._HEADER_API_KEY: api_key})
            
            self.__debug(f"Received response: {auth_response.status_code}")
            auth_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            
            response_json = auth_response.json()  # Dumping the response as a JSON string
            self.__debug(f"Response JSON: {response_json}")

            self._api_key = api_key
            self._token = response_json["token"]
            self._token_expiry = response_json["expiry"]

            self.__debug("Successfully set auth token")

        except Exception as err:
            if auth_response.status_code == 401:
                error_message = "401 Client Error: Invalid API key"
                logger.error(error_message)
                raise AuthenticationFailedException(error_message)
            else:
                error_message = f"Authentication error occurred: {err}"
                logger.error(error_message)
                raise AuthenticationFailedException(err)
        finally:
            self.__debug("Finished __auth method")

    def __debug(self, msg):
        """
        Log a debug message.

        :param msg The message to log.
        """
        if self._do_debug: logger.debug(msg)