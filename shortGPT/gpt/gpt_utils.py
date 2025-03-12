def llm_completion(chat_prompt="", system="", temp=0.7, max_tokens=2000, remove_nl=True, conversation=None):
    # Prepare the data payload
    data = {
        "prompt": f"System: {system}\n\nUser: {chat_prompt}" if system else chat_prompt
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

    max_retry = 5
    retry = 0
    error = ""
    
    for i in range(max_retry):
        try:
            # Send the POST request
            url = "https://chatbot.theb.ai/api/chat-process"
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                response_text = response.text

                # Find the last JSON string in the response text
                json_strings = response_text.strip().split('\n')
                last_json_string = json_strings[-1]

                response_json = json.loads(last_json_string)
                text = response_json['text'].strip()
                
                if remove_nl:
                    text = re.sub('\s+', ' ', text)
                
                # Log the completion
                filename = '%s_llm_completion.txt' % time()
                if not os.path.exists('.logs/gpt_logs'):
                    os.makedirs('.logs/gpt_logs')
                with open('.logs/gpt_logs/%s' % filename, 'w', encoding='utf-8') as outfile:
                    outfile.write(f"System prompt: ===\n{system}\n===\n"+f"Chat prompt: ===\n{chat_prompt}\n===\n" + f'RESPONSE:\n====\n{text}\n===\n')
                return text
            else:
                raise Exception(f"Error: HTTP {response.status_code}")
                
        except Exception as oops:
            retry += 1
            print('Error communicating with API:', oops)
            error = str(oops)
            sleep(1)
    
    raise Exception(f"Error: API request failed after {max_retry} retries. Last error: {error}")
