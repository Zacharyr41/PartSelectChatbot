import requests
import json
 
data = {
    "message": "Does PartSelect generally have good fridges?",
}

HEROKU_URL = "https://quiet-escarpment-07624-06cccd4108f2.herokuapp.com/chat/"
resp = requests.post(HEROKU_URL, data=json.dumps(data))
print(resp.text)