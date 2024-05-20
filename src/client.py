import requests
import json
 
data = {
    "message": "Does PartSelect generally have good fridges?",
}

resp = requests.post('http://0.0.0.0:8080/chat/', data=json.dumps(data))
print(resp.text)