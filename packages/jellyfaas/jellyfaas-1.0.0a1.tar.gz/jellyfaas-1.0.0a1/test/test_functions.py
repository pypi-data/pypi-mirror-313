
import os, sys
from typing import List, Optional
sys.path.insert(0, os.path.abspath('src'))
from jellyfaas import *
import inspect
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

API_KEY = os.getenv('JELLYFAAS_API_KEY')
if not API_KEY:
    raise Exception('No API KEY')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    print(f'{bcolors.ENDC}Starting test suite')
    # test_1() # testqponly
    test_2() # testqpandbodypost
    # test_3()
    # test_4()
    # test_5()
    # test_6()
    # test_7()
    # test_8()
    # test_9()
    # test_10()

# testqponly
def test_1():
    class Response(BaseModel):
        greeting: str
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testqponly'
        ).set_function_query_params(
            {'name': 'john'}
        ).invoke(Response)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

# testqpandbodypost
def test_2():
    class Request(BaseModel):
        name: str
        surname: str

    class Response(BaseModel):
        name: str
        surname: str
        location: str
    

    
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testqpandbodypost'
        ).set_function_query_params({
            "location": "abc123"
        }).set_function_body(
            Request(name="john", surname="smith")
        ).invoke(Response)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

# testqpandbodypost
def test_3():
    class Request(BaseModel):
        name: str
        surname: str

    class Response(BaseModel):
        name: str
        surname: str
    
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testputonly'
        ).set_function_body(
            Request(name="john", surname="smith")
        ).invoke(Response)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

#testpostonly
def test_4():
    class Request(BaseModel):
        name: str
        surname: str

    class Response(BaseModel):
        complete_name: str
    
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testpostonly'
        ).set_function_body(
            Request(name="john", surname="smith")
        ).invoke(Response)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

#testnestedpost
def test_5():

    class Address(BaseModel):
        city: str
        state: str
        street: str
        zip: str

    class Package(BaseModel):
        country_of_origin: str
        description: str
        id: str

    class Example(BaseModel):
        address: Address
        name: str
        packages: List[Package]
    
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testnestedpost'
        ).set_function_body(
            Example(
                address=Address(
                    city="bath",
                    state="new york",
                    street="fifth",
                    zip="96746"
                ), 
                name="john", 
                packages=[
                    Package(
                        country_of_origin="USA",
                        description="goodies",
                        id="42"
                    ),
                    Package(
                        country_of_origin="USA",
                        description="goodies",
                        id="43"
                    )
                ]
            )
        ).invoke(Example)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')



#testfileupload
def test_6():
    with open('output_image.png', 'rb') as file:
        client, resp = Client(Config(API_KEY, True)
            ).lookup_function('testfileupload').set_function_body(file
            ).invoke()
        
        print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

#testdeleteonly
def test_7():

    class Request(BaseModel):
        name: str
        surname: str

    class Data(BaseModel):
        name: str
        surname: str

    class Response(BaseModel):
        data: Optional[Data]
        message: Optional[str]

    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testdeleteonly'
        ).set_function_body(
            Request(
                name="john", 
                surname="smith"
            )
        ).invoke(Response)
    
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

#testarraypost
def test_8():
    class Package(BaseModel):
        country_of_origin: str
        description: str
        id: str

    class Example(BaseModel):
        address: str
        name: str
        packages: List[Package]

    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testarraypost'
        ).set_function_body(
            Example(
                address="House 123 Housevillle Housetopia", 
                name="john",
                packages=[
                    Package(
                        country_of_origin='USA',                
                        description='foo',
                        id='42'
                    ),
                    Package(
                        country_of_origin='UK',                
                        description='bar',
                        id='43'
                    )
                ]
            )
        ).invoke(None, raise_for_status=False)
    
    print(resp.content)
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')

#testarraynestedpost
def test_9():
    class Address(BaseModel):
        city: str
        state: str
        street: str
        zip: str

    class Package(BaseModel):
        country_of_origin: str
        description: str
        id: str

    class Example(BaseModel):
        address: Address
        name: str
        packages: List[Package]
    
    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('testarraynestedpost'
        ).set_function_body(
            Example(
                address=Address(
                    city="Kapa'a",
                    state="HI",
                    street="Kipapa",
                    zip="96746"
                ), 
                name="john",
                packages=[
                    Package(
                        country_of_origin='USA',                
                        description='foo',
                        id='42'
                    ),
                    Package(
                        country_of_origin='UK',                
                        description='bar',
                        id='43'
                    )
                ]
            )
        ).invoke(None, raise_for_status=False)
    
    print(resp.content)
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')


def test_10():

    class Request(BaseModel):
        schema: str 

    class Language(BaseModel):
        language: str
        classes: str

    class Response(BaseModel):
        data: List[Language]

    client, resp = Client(Config(API_KEY, True)
        ).lookup_function('schemaconverter'
        ).set_function_query_params({'languages':'python'}, False
        ).set_function_body(
            Request(schema="eyIkc2NoZW1hIjoiaHR0cHM6Ly9qc29uLXNjaGVtYS5vcmcvZHJhZnQvMjAyMC0xMi9zY2hlbWEiLCJwcm9wZXJ0aWVzIjp7ImFkZHJlc3MiOnsicHJvcGVydGllcyI6eyJjaXR5Ijp7InR5cGUiOiJzdHJpbmcifSwic3RhdGUiOnsidHlwZSI6InN0cmluZyJ9LCJzdHJlZXQiOnsidHlwZSI6InN0cmluZyJ9LCJ6aXAiOnsidHlwZSI6InN0cmluZyJ9fSwidHlwZSI6Im9iamVjdCIsInJlcXVpcmVkIjpbInN0cmVldCIsImNpdHkiLCJzdGF0ZSIsInppcCJdfSwibmFtZSI6eyJ0eXBlIjoic3RyaW5nIn0sInBhY2thZ2VzIjp7Iml0ZW1zIjp7InByb3BlcnRpZXMiOnsiY291bnRyeV9vZl9vcmlnaW4iOnsidHlwZSI6InN0cmluZyJ9LCJkZXNjcmlwdGlvbiI6eyJ0eXBlIjoic3RyaW5nIn0sImlkIjp7InR5cGUiOiJzdHJpbmcifX0sInR5cGUiOiJvYmplY3QiLCJyZXF1aXJlZCI6WyJpZCIsImRlc2NyaXB0aW9uIiwiY291bnRyeV9vZl9vcmlnaW4iXX0sInR5cGUiOiJhcnJheSJ9fSwidHlwZSI6Im9iamVjdCIsInJlcXVpcmVkIjpbIm5hbWUiLCJhZGRyZXNzIiwicGFja2FnZXMiXSwidGl0bGUiOiJHZW5lcmF0ZWQgc2NoZW1hIGZyb20gamVsbHlmYWFzIn0="), 
        ).invoke(Response)

    print(resp.data[0].classes)
    print(f'{bcolors.OKGREEN if client._response.status_code == 200 else bcolors.FAIL}`{inspect.stack()[0][3]}` completed with statuse code: {client._response.status_code}\n{bcolors.ENDC}  Response: {resp}')
 

if __name__ == '__main__':
    main()