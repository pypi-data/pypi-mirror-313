import base64
from enum import Enum
import json
from typing import List
from pydantic import BaseModel, Field, model_validator


class FunctionRequirementsQueryParam(BaseModel):
    name: str
    required: bool = Field(default=False)

class FunctionRequirementsFile(BaseModel):
    extensions: List[str]
    required: bool = Field(default=False)

class FunctionRequirementsJsonSchema(BaseModel):
    pass

class FunctionRequirementsBodyType(Enum):
    NONE = 0
    JSON = 1
    FILE = 2

class FunctionRequirements(BaseModel):
    request_type: str = Field(alias='requestType')
    query_params: List[FunctionRequirementsQueryParam] = Field(alias='queryParams', default=None)
    
    input_json_schema_encoded: str = Field(alias='inputJsonSchemaEncoded', default=None)
    input_file: FunctionRequirementsFile = Field(alias='inputFile', default=None)
    input_json_schema: dict = None

    output_json_schema_encoded: str = Field(alias='outputJsonSchemaEncoded', default=None)
    output_file: FunctionRequirementsFile = Field(alias='outputFile', default=None)
    output_json_schema: FunctionRequirementsJsonSchema = None
    
    input_body_type: FunctionRequirementsBodyType = FunctionRequirementsBodyType.NONE
    output_body_type: FunctionRequirementsBodyType = FunctionRequirementsBodyType.NONE

    @model_validator(mode='after')
    def decode(self):
        try:
            if self.input_json_schema_encoded != None:
                inputJsonSchemaBytes = base64.b64decode(self.input_json_schema_encoded)
                inputJsonSchemaString = inputJsonSchemaBytes.decode('utf-8')
                self.input_json_schema = json.loads(inputJsonSchemaString)
            if self.output_json_schema_encoded != None:
                outputJsonSchemaBytes = base64.b64decode(self.output_json_schema_encoded)
                outputJsonSchemaString = outputJsonSchemaBytes.decode('utf-8')
                self.output_json_schema = json.loads(outputJsonSchemaString)
            return self
        except Exception as e:
            raise TypeError('Failed to decode function requirements from server')

    @model_validator(mode='after')
    def check_inputs(self):
        exclusive_fields = {
            'input_json_schema': FunctionRequirementsBodyType.JSON,
            'input_file': FunctionRequirementsBodyType.FILE
        }
        non_none_count = 0
        for field in exclusive_fields:
            if getattr(self, field) != None:
                non_none_count += 1
                self.input_body_type = exclusive_fields[field]
        if non_none_count > 1:
            raise ValueError("Only one of 'input_json_schema', 'input_file' can be set.")
        return self
    
    @model_validator(mode='after')
    def check_outputs(self):
        exclusive_fields = {
            'output_json_schema': FunctionRequirementsBodyType.JSON, 
            'output_file': FunctionRequirementsBodyType.FILE
        }
        non_none_count = 0
        for field in exclusive_fields:
            if getattr(self, field) != None:
                non_none_count += 1
                self.output_body_type = exclusive_fields[field]        
        if non_none_count > 1:
            raise ValueError("Only one of 'output_json_schema', 'output_file' can be set.")
        return self



class LookupFunctionResponse(BaseModel):
    dns: str
    requirements: FunctionRequirements
