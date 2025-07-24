# test the server by running client.py or this code
import requests

url = 'http://127.0.0.1:8000/predict'
data = {"text": "This is a great example of a BERT model in action."}

response = requests.post(url, json=data)
print(response.json())
