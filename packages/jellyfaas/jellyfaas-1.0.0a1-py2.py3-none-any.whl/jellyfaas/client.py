import ast
import base64
from enum import Enum
import os
import requests
import logging
from typing import Any, Dict, List, Literal, Type
import jsonschema
from io import BufferedReader, BytesIO, TextIOWrapper
from pydantic import BaseModel, Field, ValidationError, model_validator
from http.client import responses
from .config import Config
from .exceptions import *
from .structs.function_requirements import *

logger = logging.getLogger(__name__)

class Client:
    """
    A client for interacting with the JellyFAAS API. It is not recommended to access attributes of this class directly; instead, use "public" class functions as per the documentation.

    :attribute _api_key (str) The API key used for authentication.
    :attribute _token (str) The authentication token.
    :attribute _token_expiry (str) The expiration time for the token.
    :attribute _version (str) The version of the function to lookup.
    :attribute _size (str) The size of the function to lookup.
    :attribute _response (Any) The response from the invoked function.
    """

    # Member "consts"
    _LOOKUP_ENDPOINT: str = "https://api.jellyfaas.com/auth-service/v1/lookup"
    _HEADER_API_KEY:  str = "x-jf-apikey"
    _HEADER_TOKEN:    str = "jfwt"

    # Member variables
    _config: Config = None
    _version: str = None
    _function_requirements = None
    _function_dns: str = None
    _query_params = None
    _body = None
    _body_type: FunctionRequirementsBodyType = FunctionRequirementsBodyType.NONE
    _response = None    

    def __init__(self, config: Config) -> None:      
        """
        Initializes and authenticates the Client with the provided config object.

        :param config A JellyFAAS Client config object.

        :raises AuthenticationFailedException If authentication fails.
        """
        if not isinstance(config, Config):
            raise JellyFaasException('Invalid parameter: config must be of type \'jellyfaas.Config\'')
        
        if not config.is_authenticated:
            raise JellyFaasException('Invalid config object: unauthenticated')
        
        self._config = config
    
    def set_version(self, version: int) -> 'Client':
        if not isinstance(version, int) or version <= 0:
            raise JellyFaasException('Version must be a positive int')
        
        if self._function_dns != None:
            raise JellyFaasException('set_version() may only be called before lookup_function()')

        self._version = version

    def lookup_function(self, function_id: str) -> 'Client':
        """
        Lookup a function by its ID.

        :param function_id (str) The ID of the function to look up.

        :return: Client The current client instance.

        :raises FunctionLookupException If the function lookup fails.
        """
        self.__print_debug(f"Starting lookup_function method with function_id={function_id}")

        if not isinstance(function_id, str):
            raise JellyFaasException('Invalid parameter: function_id must be of type \'str\'')

        query_params = {
            "id": function_id,        
        }
        
        if self._version != None: 
            query_params["version"] = self._version 

        try:
            lookup_response = requests.get(
                self._LOOKUP_ENDPOINT,
                headers={self._HEADER_API_KEY: self._config._api_key},
                params=query_params
            )
            
            lookup_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            resp = LookupFunctionResponse(**lookup_response.json())
            self._function_dns = resp.dns
            self._function_requirements = resp.requirements
            
            return self
        
        except ValidationError as e:
            error_message = f"Error validating function response from server {e}"
            raise FunctionLookupException(error_message)
        except FunctionLookupException as e:
            raise FunctionLookupException(e)
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            raise FunctionLookupException(error_message)
        except Exception as e:
            error_message = f"Other error occurred: {e}"
            raise FunctionLookupException(error_message)


    def set_function_query_params(self, query_params: Dict[str, str], do_validation=True):

        if not isinstance(query_params, dict):
            raise JellyFaasException('Invalid parameter: function_id must be of type \'Dict\'')

        if any((not isinstance(val, str)) for val in query_params.keys()):
            raise JellyFaasException('Invalid parameter: all query param keys must be of type \'str\'')
        
        if any((not isinstance(val, str)) for val in query_params.values()):
            raise JellyFaasException('Invalid parameter: all query param values must be of type \'str\'')

        if self._function_requirements.query_params == None:
            if do_validation:
                raise JellyFaasException('Function does not take query params')
            else:
                logger.warning('Function does not take query params')

        try:
            self.__validate_query_params(query_params)
        except JellyFaasException as e:
            if do_validation:
                raise JellyFaasException(e)
            else:
                logger.warning('Invalid query params')
        
        self._query_params = query_params
        return self

    
    def set_function_body(self, body, do_validation=True):
        match self._function_requirements.input_body_type:
            case FunctionRequirementsBodyType.NONE:
                raise JellyFaasException('Could not set function body. Function does not take body')
            case FunctionRequirementsBodyType.JSON:
                self.set_function_json_body(body, do_validation)
            case FunctionRequirementsBodyType.FILE:
                self.set_function_file_body(body, do_validation)
        return self


    def set_function_json_body(self, body: dict | BaseModel, do_validation=True):

        try:
            if hasattr(body, 'model_dump'):
                body = body.model_dump()
        except TypeError:
            pass
        except Exception as e:
            raise JellyFaasException(f'Could not deserialize body: {e}')
        
        if not isinstance(body, dict):
            raise JellyFaasException(f'Could not deserialize body or body is not a dict')

        if do_validation:
            has_schema_body = self._function_requirements.input_json_schema != None

            if not has_schema_body: 
                raise JellyFaasException('Validation error: function spec has no \'inputJsonSchema\' attribute')
            if body == None:
                raise JellyFaasException('Validation error: body is not specified')
            
            try:
                valid, message = self.__validate(schema=self._function_requirements.input_json_schema, data=body)
                if not valid:
                    raise ValueError(message)
            except ValueError as e:
                error_message = f"Validation error: {e}"
                raise SetRequestException(error_message)
              
        self._body = body
        self._body_type = FunctionRequirementsBodyType.JSON
        return self

    def set_function_file_body(self, body, do_validation=True):
        if do_validation:
            schema = self._function_requirements.input_file

            if schema == None: 
                raise JellyFaasException('Validation error: function spec has no \'inputFile\' attribute')
            
            required = schema.required
            if required and body == None:
                error_message = f"Request file is not provided but is required by function spec"
                raise SetRequestException(error_message)  
        
            if body != None:

                # Strip all leading '.'s and make lowercase all input and schema extensions
                _, extension = os.path.splitext(body.name)
                extension = extension.lower().lstrip('.')
                valid_extensions = schema.extensions
                valid_extensions = [s.lower().lstrip('.') for s in valid_extensions]

                if valid_extensions != []: # Empty 'extensions' list treated as accepting all files
                    if not (extension in valid_extensions):
                        error_message = f"Request file does not have a valid extension for this function: {extension} but expected {valid_extensions}"
                        raise SetRequestException(error_message)

        self._body = body
        self._body_type = FunctionRequirementsBodyType.FILE
        return self
    
    def __validate_query_params(self, query_params: Dict[str, str]):
        

        for i in range(len(self._function_requirements.query_params)):

            name = self._function_requirements.query_params[i].name
            required = self._function_requirements.query_params[i].required

            if required and (name not in query_params):
                raise JellyFaasException(f'Missing query param: "{name}" not specified')
        return True


    def invoke(self, output_class: type = None, do_validation: bool = True, raise_for_status: bool = True):
        """
        Invoke the function with the set parameters and body.

        :param output_class: The type to deserialize the output into (e.g., Pydantic model or BytesIO).
        :param do_validation: Whether to validate input/output types and query parameters.
        :param raise_for_status: Whether to raise an error for non-2xx responses.
        :return: A tuple of the client instance and the response content (deserialized if applicable).
        """
        self.__print_debug("Starting invoke method")

        # Validation
        if do_validation:
            pass
            # if not self._function_dns or not self._config.is_authenticated or not self._function_requirements:
            #     error_message = "Endpoint, token, and request requirements must be set."
            #     raise InvocationException(error_message)

            # if self._function_requirements.input_body_type != self._body_type:
            #     expected = self._function_requirements.input_body_type
            #     error_message = (
            #         f"Invalid function body type. Expected {expected} but got {self._body_type}. "
            #         "If this is intentional, call `invoke` with `do_validation=False`."
            #     )
            #     raise InvocationException(error_message)

            # if output_class is not None:
            #     error_message = (
            #         f"Invalid output type. Expected a class or None, but got {type(output_class).__name__}. "
            #         "If this is intentional, call `invoke` with `do_validation=False`."
            #     )
            #     raise InvocationException(error_message)

        # Prepare request
        method = self._function_requirements.request_type
        headers = {
            self._HEADER_TOKEN: self._config._token,
            "Content-Type": "application/json",
        }
        self.__print_debug(f"Invoking with headers={headers}, data={self._body}, params={self._query_params}")
        print(self._body)
        # Send request
        try:
            if isinstance(self._body, dict):
                resp = requests.request(
                    method,
                    self._function_dns,
                    headers=headers,
                    params=self._query_params,
                    json=self._body,
                )
            elif isinstance(self._body, (BufferedReader, TextIOWrapper)):
                resp = requests.request(
                    method,
                    self._function_dns,
                    headers=headers,
                    params=self._query_params,
                    data=self._body.read(),
                )
            elif self._body_type == FunctionRequirementsBodyType.NONE:
                resp = requests.request(
                    method,
                    self._function_dns,
                    headers=headers,
                    params=self._query_params
                )
            else:
                error_message = 'Unsupported data type for request. Expected dict or file.'
                raise InvocationException(error_message)

            self.__print_debug(f"Received response: {resp.status_code}")
            self._response = resp

            if raise_for_status:
                resp.raise_for_status()

            # Handle output type
            if output_class is None:
                return self, resp

            if output_class == BytesIO:
                return self, BytesIO(resp.content)

            if self._function_requirements.output_json_schema:
                try:
                    if output_class:
                        return self, output_class.parse_obj(resp.json())  # Assuming Pydantic model
                    else:
                        return self, self._response.json()
                except Exception as e:
                    raise InvocationException(f"Error parsing response JSON: {e}")
            else:
                return self, None

        except requests.exceptions.HTTPError as http_err:
            error_message = (
                f"Function invocation responded with 4xx or 5xx status code. "
                f"If this is expected, set `raise_for_status=False`.\n"
                f"{resp.status_code} {resp.reason}: {resp.content}\n"
            )
            raise InvocationException(error_message) from http_err
        except Exception as err:
            raise InvocationException(f"Other error occurred: {err}") from err


    def __print_debug(self, msg):
        """
        Log a debug message.

        :param msg (str) The message to log.
        """
        if (not hasattr(self, '_config')) or self._config == None: logger.debug(msg)
        elif self._config._do_debug: logger.debug(msg)

    def set_debug_mode(self, do_debug: bool):
        if do_debug == True or do_debug == False:
            self._do_debug = do_debug
            return self
        else:
            raise JellyFaasException("Invalid `set_debug_mode` parameter. Must be True|False")

    def __validate(self, schema, data):
        """
        Validate the given data against the provided schema.

        :param schema (dict) The schema to validate against.
        :param data (dict) The data to validate.

        :return: tuple A tuple containing a boolean indicating success and a message.

        :raises ValueError If validation fails.
        """
        try:
            if schema == None:
                return True, None
            if 'type' not in schema:
                return False, "Schema is missing 'type' key"
            
            jsonschema.validate(data, schema)
            return True, None
        
        except Exception as e:
            return False, e

