import functions_framework
import openai

def gpt_chat(request):
    # Get the input data from the request
    request_json = request.get_json(silent=True)
    message = request_json.get('message', '')
    model = request_json.get('model', 'text-davinci-003')  # Default to text-davinci-003 if model is not specified
    temperature = request_json.get('temperature', 0.7)    # Default to 0.7 if temperature is not specified
    max_tokens = request_json.get('max_tokens', 150)      # Default to 150 if max_tokens is not specified

    # Set your OpenAI GPT-3 API key here
    openai.api_key = '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'

    # Retrieve the conversation history from the request (if any)
    conversation = request_json.get('conversation', [])

    # Append the new message to the conversation
    conversation.append({"role": "user", "content": message})

    # Concatenate the conversation history into a single prompt with '\n' as a delimiter
    prompt = "\n".join([f"{message['role']}: {message['content']}" for message in conversation])

    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Extract the assistant's reply and return it
    assistant_reply = response['choices'][0]['text'].strip()  # Strip leading and trailing whitespace
    return {'response': assistant_reply}
