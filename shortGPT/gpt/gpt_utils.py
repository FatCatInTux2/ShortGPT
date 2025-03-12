import json
import requests

safeInput = input('Request:  ')

# Prepare the data payload
data = {
    "prompt": safeInput
}
payload = json.dumps(data)

# Set the headers
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Origin": "https://chatbot.theb.ai",
    "Referer": "https://chatbot.theb.ai/"
}

# Send the POST request
url = "https://chatbot.theb.ai/api/chat-process"
response = requests.post(url, data=payload, headers=headers)

# Process the response
if response.status_code == 200:
    response_text = response.text

    # Find the last JSON string in the response text
    json_strings = response_text.strip().split('\n')
    last_json_string = json_strings[-1]

    response_json = json.loads(last_json_string)
    print(response_json['text'])
else:
    print("Error:", response.status_code)
