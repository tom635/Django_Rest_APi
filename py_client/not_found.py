import requests

endpoint='http://127.0.0.1:8000/api/products/2256215'

get_response=requests.get(endpoint)

print(get_response.status_code)
print(get_response.json())


# required field are required when validating with serelizable 
