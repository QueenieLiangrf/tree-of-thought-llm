import os
from groq import Groq
import backoff

completion_tokens = prompt_tokens = 0

# Initialize Groq Client
client = Groq()

# Define a backoff decorator
@backoff.on_exception(backoff.expo, Exception)  # Using generic Exception for Groq API
def completions_with_backoff(**kwargs):
    # Groq's API call
    return client.chat.completions.create(**kwargs)

def gpt(prompt, model="llama3-groq-70b-8192-tool-use-preview", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    # Set up messages for Groq API
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)

def chatgpt(messages, model="llama3-groq-70b-8192-tool-use-preview", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        # Groq API call with backoff
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        # Process response
        for chunk in res:
            outputs.append(chunk.choices[0].delta.content or "")
            # Log completion tokens and prompt tokens
            completion_tokens += chunk.usage.completion_tokens
            prompt_tokens += chunk.usage.prompt_tokens
    return outputs

def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    # Placeholder for cost calculation (example values for Groq)
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.05 + prompt_tokens / 1000 * 0.02  # Adjust as per Groq's pricing
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}

# # Example usage
# prompt = "What is the capital of France?"
# response = groq(prompt)
# print(response)

# import os
# import openai
# import backoff 

# completion_tokens = prompt_tokens = 0

# api_key = os.getenv("OPENAI_API_KEY", "")
# if api_key != "":
#     openai.api_key = api_key
# else:
#     print("Warning: OPENAI_API_KEY is not set")
    
# api_base = os.getenv("OPENAI_API_BASE", "")
# if api_base != "":
#     print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
#     openai.api_base = api_base

# @backoff.on_exception(backoff.expo, openai.error.OpenAIError)
# def completions_with_backoff(**kwargs):
#     return openai.ChatCompletion.create(**kwargs)

# def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
#     messages = [{"role": "user", "content": prompt}]
#     return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    
# def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
#     global completion_tokens, prompt_tokens
#     outputs = []
#     while n > 0:
#         cnt = min(n, 20)
#         n -= cnt
#         res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
#         outputs.extend([choice["message"]["content"] for choice in res["choices"]])
#         # log completion tokens
#         completion_tokens += res["usage"]["completion_tokens"]
#         prompt_tokens += res["usage"]["prompt_tokens"]
#     return outputs
    
# def gpt_usage(backend="gpt-4"):
#     global completion_tokens, prompt_tokens
#     if backend == "gpt-4":
#         cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
#     elif backend == "gpt-3.5-turbo":
#         cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
#     return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}
