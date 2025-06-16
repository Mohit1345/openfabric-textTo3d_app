from ollama import Client

def call_llm_generate(model_id: int, prompt: str) -> str:
    client = Client(host="http://host.docker.internal:11434")

    models = ["gemma3:latest"]
    
    if models[model_id] not in models:
        raise ValueError(f"Model '{models[model_id]}' is not supported. Choose from {models}.")

    result = client.generate(model=models[model_id], prompt=prompt)
    return result['response']



# def call_llm_chat(model_id: int, messages: list, tools: list = None) -> str:
#     """
#     Calls the Ollama LLM for chat-style interaction, optionally using tools (functions).

#     Args:
#         model: Name of the model (e.g., 'llama2', 'llama3.1')
#         messages: List of chat messages (e.g., [{'role': 'user', 'content': '...'}])
#         tools: List of Python functions to use as tools (optional)

#     Returns:
#         str: The assistant's response content
#     """
#     models = ["gemma3:latest", "mistral", "gemma:2b"]
#     if models[model_id] not in models:
#         raise ValueError(f"Model '{models[model_id]}' is not supported. Choose from {models}.")
#     response = ollama.chat(model=models[model_id], messages=messages, tools=tools)
#     return response['message']['content']


# print(call_llm_chat(0, [{"role": "user", "content": "Hello, how are you?"}]))
# print(call_llm_generate(0,  "Hello, how are you"))