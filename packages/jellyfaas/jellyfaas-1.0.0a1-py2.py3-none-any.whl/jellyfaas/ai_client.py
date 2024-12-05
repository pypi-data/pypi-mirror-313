import ast
import base64
import json
import os
import time
import requests
import logging
from typing import Any, Dict, Type
from io import BufferedReader, BytesIO, TextIOWrapper
from pydantic import BaseModel

from .ai_config import AIConfig
from .ai_provider import *
from .exceptions import *

logger = logging.getLogger(__name__)

class AIClient:

    _QUERY_SERVICE_ENDPOINT: str = 'https://ai.jellyfaas.com/query-service/v1'
    _HEADER_API_KEY:      str = "x-jf-apikey"

    # TODO repleace these with config props
    # Member variables
    _api_key: str = None
    _token: str = None
    _token_expiry: str = None
    _do_debug = False

    _vector_database_name = None
    _vector_database_connection_string = None

    _rdbms_connection_string = None
    _rdbms_tables = None

    _functions = []

    def __init__(self, config: AIConfig) -> None:
        self._api_key      = config._api_key
        self._token        = config._token
        self._token_expiry = config._token_expiry
        self._do_debug     = config._do_debug
    
    def lookup_function(self, function):

        if type(function) != Dict:
            raise JellyFaasException('Expected function dict')
        
        function_id = function.get('id', None)
        if function_id == None:
            raise JellyFaasException('Expected function id')

        query_params = {
            'id': function_id
        }

        function_version = function.get('version', None)
        if function_version != None:
            query_params['version'] = function_version

        function_size= function.get('size', None)
        if function_size != None:
            query_params['size'] = function_size

        self.debug(f"Starting lookup_function method with function_id={function_id}")
        
        try:
            lookup_response = requests.get(
                self.LOOKUP_ENDPOINT,
                headers={self._HEADER_API_KEY: self._config._api_key},
                params=query_params
            )
            
            self.debug(f"Received response: {lookup_response.status_code}")
            lookup_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            lookup_response_json = lookup_response.json()  # Parse the response as a JSON string
            self.debug(f"Response JSON: {lookup_response_json}")

            function_details = {
                    'id': function_id,
                    'version': function_version,
                    'size': function_size,
                    'dns': lookup_response_json.get("dns", None),
                    'requirements': lookup_response_json.get("requirements", None)
                }
            
            self._functions.append(function_details)

            self.debug("Successfully looked up function")

            return self

        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            logger.error(error_message)
            raise FunctionLookupException(error_message)
        except Exception as err:
            error_message = f"Other error occurred: {err}"
            logger.error(error_message)
            raise FunctionLookupException(f"Other error occurred: {err}")

    
    def search_function(self):
        pass

    def connect_vector_database(self, database_name, connection_string = None):
        if database_name == None:
            raise JellyFaasException('Invalid database name')
        
        self._vector_database_name = database_name
        if connection_string != None:
            self._vector_database_connection_string = connection_string
        
        return self

    def query(self, query, rag_query=None, rdbms_query=None):

        if self._vector_database_name != None:
            return self._vector_query(query, rag_query)
        
        if self._rdbms_connection_string != None:
            return self._rdbms_query(query, rdbms_query)
    
    def _vector_query(self, query, rag_query=None):

        # Prepare the request body
        request_body = {
            "query": query,
            "mongo_embeddings_collection": self._vector_database_name,
            "mongo_connection_string": self._vector_database_connection_string,
            "mongo_embeddings_database": 'RAG_Embeddings',
        }

        # Optional RAG query
        if rag_query:
            request_body["rag_query"] = rag_query

        # Log for debugging if enabled
        if self._do_debug:
            print(f"Request Body: {json.dumps(request_body, indent=2)}")

        # Make the request to the 'query-vectordb' API
        try:
            headers = {"jfwt": self._token}
            response = requests.post(
                url=self._QUERY_SERVICE_ENDPOINT,
                headers=headers,
                json=request_body
            )

            if response.status_code == 200:
                result = response.json()
                if self._do_debug:
                    print(f"Response: {json.dumps(result, indent=2)}")
                return result['answer']
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def _rdbms_query(self, query, rdbms_query=None):

        # Prepare the request body
        request_body = {
            "query": query,
            "tables": self._rdbms_tables,
            "mysql_connection_string": self._rdbms_connection_string,
            "ai_platform": "gemini"
        }

        # Optional RAG query
        if rdbms_query:
           request_body["rdbms_query"] = rdbms_query

        # Log for debugging if enabled
        if self._do_debug:
            print(f"Request Body: {json.dumps(request_body, indent=2)}")

        # Make the request to the 'query-vectordb' API
        try:
            headers = {"jfwt": self._token}
            response = requests.post(
                url='https://ai.jellyfaas.com/query-service/v1/rdbms',
                headers=headers,
                json=request_body
            )

            result = response.json()
            if response.status_code == 200:
                if self._do_debug:
                    print(f"Response: {json.dumps(result, indent=2)}")
                return result['answer']
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")

    def upload(self, file, database_name, blocking=True):
        try:
            print(f'Uploading file(s)...')
            headers = {"jfwt": self._token}
            response = requests.post(
                url='https://ai.jellyfaas.com/embedder-service/v1/upload',
                params={
                    'collection_name': database_name
                },
                headers=headers,
                files={
                    'file': file
                }
            )

            if response.status_code != 202:
                raise Exception(f"Error {response.status_code}: {response.text}")
           
            result = response.json()
            upload_id = result['upload_id']

            print('Upload finished')

            if blocking == False:
                return upload_id
        
            print('Embedding file(s)...')

            while(True):
                status = self.get_upload_status(upload_id)
                if status['status'] == 'completed':
                    break
                time.sleep(1)
            
            print('File successfully embedded')

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def get_upload_status(self, id):
        try:
            
            headers = {"jfwt": self._token}
            response = requests.get(
                url='https://ai.jellyfaas.com/embedder-service/v1/status',
                params={
                    'upload_id': id
                },
                headers=headers,
            )

            if response.status_code == 200:
                result = response.json()
                if self._do_debug:
                    print(f"Response: {json.dumps(result, indent=2)}")
                return result
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query vector database: {str(e)}")
    
    def connect_sql_database(self, connection_string, tables):
        self._rdbms_connection_string = connection_string
        self._rdbms_tables = tables
        return self

    def reset(self):
        self._rdbms_connection_string = None
        self._rdbms_tables = None
        self.connect_vector_database('')
        return self