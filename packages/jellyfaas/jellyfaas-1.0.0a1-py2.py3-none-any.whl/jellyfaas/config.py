import requests
import logging
from typing import Any, Dict, Type
from pydantic import BaseModel, ValidationError

from .exceptions import *

logger = logging.getLogger(__name__)


class InitParams(BaseModel):
    api_key: str
    debug: bool = False

class AuthResponse(BaseModel):
    token: str
    expiry: str

class Config:

    # Private member "consts"
    _AUTH_ENDPOINT: str = "https://api.jellyfaas.com/auth-service/v1/validate"
    _AUTH_HEADER:    str = "x-jf-apikey"

    # Private member variables
    _api_key:      str  = None
    _token:        str  = None
    _do_debug:     bool = None

    # Public member variables
    is_authenticated: bool = False
 
    def __init__(self, api_key: str, do_debug: bool=False) -> None:
        # Validate input using Pydantic model
        try:
            params = InitParams(api_key=api_key, debug=do_debug)
            self._do_debug = params.debug
            self.__auth(params.api_key)

        except ValidationError as e:
            logger.error(f"Invalid parameters provided: {e}")
            raise ValueError(f"Invalid parameters: {e}")


    def __auth(self, api_key=None):
        """
        Authenticate with the JellyFAAS API using the provided API key.

        :param api_key The API key for JellyFAAS.
        :raises AuthenticationFailedException If authentication fails.
        """

        self.__print_debug(f"Starting __auth method with api_key = {api_key}")
    
        try:
            auth_response = requests.get(
                self._AUTH_ENDPOINT, 
                headers={self._AUTH_HEADER: api_key})
            auth_response.raise_for_status()  # Raise an error for 4xx/5xx status codes
            
           # Parse and validate the response JSON using the Pydantic model
            response_data = AuthResponse(**auth_response.json())

            self._api_key = api_key
            self._token = response_data.token
            self.is_authenticated = True

            self.__print_debug("Successfully authenticated")

        except ValidationError:
            error_message = 'Received invalid authentication data from the server.'
            logger.error(error_message)
            raise AuthenticationFailedException(error_message)
        
        except requests.HTTPError as e:
            if auth_response.status_code == 401:
                error_message = "HTTP error occurred: 401\nInvalid API key"
            else:
                error_message = f"HTTP error occurred: {e}"
            logger.error(error_message)
            raise AuthenticationFailedException(error_message)
        except Exception as e:
                error_message = f"Unknown error occurred: {e}"
                logger.error(error_message)
                raise AuthenticationFailedException(e)
            
        finally:
            self.__print_debug("Finished __auth() method")

    def __print_debug(self, msg):
        """
        Log a debug message.

        :param msg The message to log.
        """
        if self._do_debug: logger.debug(msg)