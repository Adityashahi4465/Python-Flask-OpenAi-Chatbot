import functions_framework
import openai
from dotenv import load_dotenv
import os

# Global variable to store conversation history
conversation = []

def gpt_chat(request):
    global conversation

    # Get the input data from the request
    request_json = request.get_json(silent=True)
    message = request_json.get('message', '')
    model = 'gpt-3.5-turbo'
    temperature = request_json.get('temperature', 0.7)
    max_tokens = request_json.get('max_tokens', 150)

    load_dotenv()
    # OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Append the new message to the conversation
    conversation.append({"role": "user", "content": message})

    # Concatenate the conversation history into a single prompt with '\n' as a delimiter
    prompt = "\n".join([f"{message['role']}: {message['content']}" for message in conversation])

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful assistant."}] + conversation[-5:],
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Extract the assistant's reply and return it
    assistant_reply = response['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": assistant_reply})
    return {'response': assistant_reply}
