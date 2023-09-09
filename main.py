import openai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Global variable to store conversation history
conversation = []

app = Flask(__name__)
CORS(app)

def gpt_chat(request_data):
    global conversation

    message = request_data.get('message', '')
    model = 'gpt-3.5-turbo'
    temperature = request_data.get('temperature', 0.7)
    max_tokens = request_data.get('max_tokens', 500)

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
    return assistant_reply

@app.route('/get')
def home():
    return "Hello world";

@app.route('/gpt_chat', methods=['POST'])
def handle_gpt_chat():
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'Invalid request data. Missing "message" key.'}), 400

    request_data = request.json
    response = gpt_chat(request_data)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
