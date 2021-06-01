import json
import requests

data = {
    }
'''
requests.post(
    url='http://127.0.0.1:5000/register/',
    json=json.dumps(data)
    )
'''

response = requests.get(url='http://127.0.0.1:5000/')
