import requests

def gpt_chat_api(message, conversation):
    url = 'http://localhost:8080'
    headers = {'Content-Type': 'application/json'}

    data = {
        'message': message,
        'temperature': 0.7,
        'max_tokens': 150,
        'conversation': conversation.copy()
    }

    response = requests.post(url, headers=headers, json=data)
    assistant_reply = response.json()['response']
    conversation.append({"role": "user", "content": message})
    conversation.append({"role": "assistant", "content": assistant_reply})

    return conversation

def test_gpt_chat():
    conversation = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        conversation = gpt_chat_api(user_input, conversation)

        # Print the most recent response from the assistant
        print("Bot:", conversation[-1]['content'])

if __name__ == '__main__':
    test_gpt_chat()
