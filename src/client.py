import requests
import json
from constants import HEROKU_URL
 
data = {
    "message": "Does PartSelect generally have good fridges?",
}


resp = requests.post(HEROKU_URL, data=json.dumps(data))
print(resp.text)