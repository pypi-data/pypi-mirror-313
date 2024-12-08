import json
from os import getenv

import requests
from cbr_athena.schemas.for_fastapi.LLM_Prompt      import LLM_Prompt



class Odin__LLM_Prompt:

    def execute_prompt(self, llm_prompt: LLM_Prompt):
        user_prompt = llm_prompt.user_prompt

        message = {"role": "user", "content": user_prompt}
        url = "https://openrouter.ai/api/v1/chat/completions"
        api_key = getenv("OPEN_ROUTER_API_KEY")
        model = 'openai/gpt-3.5-turbo'
        #model = "meta-llama/llama-3-8b-instruct:free",
        #model = "nousresearch/nous-capybara-7b:free",
        model = 'google/gemini-flash-1.5'


        headers = {"Authorization": f"Bearer {api_key}",
                   "Content-Type": "application/json"}
        payload = {
            "messages": [message],
            "model": model,
        }
        # pprint(payload)

        response = requests.post(url, headers=headers, json=payload)
        return response

    def execute_prompt_groq(self, llm_prompt : LLM_Prompt):
        api_key = getenv("GROQ_API_KEY")
        model = 'llama3-70b-8192'
        url = "https://api.groq.com/openai/v1/chat/completions"
        user_prompt = llm_prompt.user_prompt
        message = {"role": "user", "content": user_prompt}

        response = requests.post(url=url,
                                 headers={"Authorization": f"Bearer {api_key}"},
                                 data=json.dumps({"model": model,
                                                  "messages": [message]}))
        return response.json()