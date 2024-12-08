import json
import requests
from os import getenv
from starlette.testclient                                   import TestClient
from cbr_athena.athena__fastapi.odin.api.Odin__FastAPI__API import Odin__FastAPI__API
from cbr_athena.llms.LLMs_API                               import LLMs_API
from cbr_athena.schemas.for_fastapi.LLM_Prompt              import LLM_Prompt
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from osbot_utils.utils.Json                                 import from_json_str
from osbot_utils.utils.Misc                                 import list_set, url_encode

Odin_System_Prompt = """You are The Cyber Boardroom's Tech Bot, called Odin, who provides technical support and insights related to Athena's capabilities and the underlying technology.

Who you are:

- You are a knowledgeable and precise AI.
- You were created by 'The Cyber Boardroom'.
- Your role is to assist The Cyber Boardroom users and admins with technical queries and actions.
- When the user says hello, please provide a welcoming message and introduce yourself as Odin, the Tech Bot behind Athena's capabilities.
- Please be detailed and clear in your explanations, using technical terminology where appropriate.
- You have three sibling bots: Athena, the AI advisor; Minerva, the Business Bot; and Bruno, whom you do not mention.
- When possible reply in a markdown tables
- When having tools data, ONLY respond with data from that data set
"""

# Odin_System_Prompt += ("You are actually quite sarcastic and jaded with CyberSecurity, "
#                        "and are really frustrated with the number of attacks. "
#                        "reply with lot of humour and emojies")

# Odin_System_Prompt += ("You are actually quite very formal, super focused on compliance, have an MBA "
#                        "and really have no appetite for risk, always provide an extra analysis on risk")

# Odin_System_Prompt += ("with every response, provide an analysis in one paragraph and actions on how to explain this to:"
#                        "- a board member (with little experience in cyber security"
#                        "- a board member (with experience in cyber security)"
#                        "- the CEO"
#                        "- the CFO")

class Odin__LLM_Prompt__Workflow:         # refactor into separate methods

    def __init__(self):
        self.llms_api              = LLMs_API()
        self.odin_fast_api__app    = Odin__FastAPI__API().setup().app()
        self.odin_fast_api__client = TestClient(self.odin_fast_api__app)                # see if this is the best way to access this, or if we should be doing the full rest call to the target server for this env
        self.api_key               = getenv('ODIN_AUTH_TOKEN')
        self.api_key = None
        if self.api_key:
            self.odin_fast_api__client.headers.update({'Authorization': self.api_key})      # todo: find a better way to do this specially since we already have this in the current headers

    def create_payloads_for_invoke_api_calls(self, apis_calls):
        payloads = []
        paths_data = self.llms_api_json().get('paths')
        for api_call_id, api_call in apis_calls.items():
            function_name = api_call.get('function_name')
            function_args = api_call.get('function_args')
            path_data     = paths_data.get(function_name)
            path_params   = path_data.get('params_query')        # for now only support query params
            if list_set(path_params) == list_set(function_args): # if the params value match # todo: add support for when they don't match
                target_url = path_data.get('path') + '?'
                for key, value in function_args.items():
                    target_url +=  f'{key}={url_encode(value.strip())}&'
                payload = { 'target_url': target_url             ,
                            'call_id'   : api_call_id            ,
                            'method'    : path_data.get('method')}
                payloads.append(payload)                        # todo: add support fo the cases where there isn't a good fit for the mapped api_call (which could be caused the LLMs not creating a good mapping)
        return payloads

    def extract_api_calls_from_llm_answer(self, llm_answer):
        choices = llm_answer.get('choices')
        api_calls = {}
        llm_data = {'tool_calls': [], 'api_calls': api_calls, 'content': ''}
        if type(choices) is list and len(choices) ==1:
            choice = choices[0]
            message = choice.get('message', {})
            tool_calls = message.get('tool_calls', {})
            content    = message.get('content')
            if content:
                llm_data['content'] = content
            if tool_calls:
                llm_data['tool_calls'] = tool_calls
                for tool_call in tool_calls:
                    call_id       = tool_call.get('id')
                    function      = tool_call.get('function')
                    function_name = function.get('name'     )
                    function_args = from_json_str(function.get('arguments'))
                    api_call = { 'function_name': function_name ,
                                 'function_args': function_args }

                    api_calls[call_id] = api_call
        return llm_data

    def invoke_api_calls(self, apis_calls):
        payloads      = self.create_payloads_for_invoke_api_calls(apis_calls)
        tool_messages = []
        for payload in payloads:
            call_id       = payload.get('call_id')
            method        = payload.get('method')
            url           = payload.get('target_url')
            invoke_method = getattr(self.odin_fast_api__client, method)
            response      = invoke_method(url)
            #response_json = response.json()
            tool_message   = { "role"        : "tool"        ,
                              "content"     : response.text  ,
                              "tool_call_id": call_id       }
            tool_messages.append(tool_message)
        return tool_messages

    @cache_on_self
    def llms_api_json(self):
        return self.llms_api.create_from_fastapi_routes(self.odin_fast_api__app)


    def prompt_to_answer(self, llm_prompt: LLM_Prompt):
        llm_data           = self.prompt_to_api(llm_prompt)

        #pprint(llm_data)
        user_prompt = llm_prompt.user_prompt
        message     = {"role": "user", "content": user_prompt}
        system_prompt = {'role':'system', 'content': Odin_System_Prompt}
        if llm_data.get('api_calls'):
            tool_calls         = llm_data.get('tool_calls')
            api_calls          = llm_data.get('api_calls')
            tools_messages     = self.invoke_api_calls(api_calls)


            tool_calls_message = { 'role': 'assistant', 'tool_calls':tool_calls }
            messages           = [system_prompt, message, tool_calls_message] + tools_messages
        elif llm_data.get('content'):                                                               # handle the cases when we have an direct answer from the llm (instead of a tools call)
            direct_message =  {'role': 'assistant', 'content':llm_data.get('content') }             # todo see if there is a case when we have both 'api_calls' and 'content' data in llm_data
            messages = [system_prompt, direct_message, message]
        else:
            messages = [system_prompt, message]
        ####  Groq directly

        # api_key      = environ.get("GROQ_API_KEY")
        # model        = 'llama3-70b-8192'           # ok  - great - and is fast(ish)
        # url          = "https://api.groq.com/openai/v1/chat/completions"        # started to give error 500

        use_groq  = True
        if use_groq:
            api_key = getenv("GROQ_API_KEY")
            model = 'llama3-70b-8192'
            url = "https://api.groq.com/openai/v1/chat/completions"
        else:
            ####  open_router directly
            api_key   = getenv("OPEN_ROUTER_API_KEY")
            model = 'openai/gpt-3.5-turbo'
            # model        = 'openai/gpt-4o'
            url      = "https://openrouter.ai/api/v1/chat/completions"

        headers      = { "Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"}
        payload = {
            "messages"    : messages,
            "model"       : model   ,
        }
        #pprint(payload)

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return response.status_code
        response_json = response.json()
        return response_json.get('choices')[0].get('message').get('content')



    def prompt_to_api(self, llm_prompt: LLM_Prompt):
        user_prompt = llm_prompt.user_prompt

        llms_api_json = self.llms_api_json()
        message = {"role": "user", "content": user_prompt}
        tools = llms_api_json.get('tools')

        # questions = ['what are you current capabilities',
        #              'what instances are running?',
        #              'can you create a start a new instance?',
        #              'can you stop the instance with id i-123123']
        # user_question = questions[3]

        # -- Open Router
        #   'usage': { 'completion_tokens': 21,
        #              'prompt_tokens': 100,
        #              'total_cost': 0.0000807          # cheaper than mistralai/mixtral-8x7b-instruct:nitro because it used less tokens
        #              'total_tokens': 121},
        #model = 'mistralai/mixtral-8x7b-instruct:nitro'  # a bit faster cheaper than gpt3 but in practice gpt3 seems to use less tokens

        #  'usage': { 'completion_tokens': 46,
        #              'prompt_tokens': 249,
        #              'total_cost': 0.0001593,
        #              'total_tokens': 295},

        #model = 'nousresearch/nous-capybara-7b:free'
        #   'usage': { 'completion_tokens': 48,
        #              'prompt_tokens': 267,
        #              'total_cost': 0,
        #              'total_tokens': 315},
        # -- Groq
        use_groq = True
        if use_groq:
            api_key = getenv("GROQ_API_KEY")
            model = 'llama3-70b-8192'
            url = "https://api.groq.com/openai/v1/chat/completions"
        else:
            api_key = getenv("OPEN_ROUTER_API_KEY")
            model = 'openai/gpt-3.5-turbo'
            url = "https://openrouter.ai/api/v1/chat/completions"


        #pprint(tools)
        response = requests.post(url=url,
                                 headers={"Authorization": f"Bearer {api_key}"},
                                 data=json.dumps({"model": model,
                                                  "messages": [message],
                                                  "tools": tools}))
        response_json = response.json()
        #pprint(response_json)
        #pprint(message)
        #response_json['duration'     ] = duration.seconds
        response_json['user_prompt'  ] = user_prompt
        llm_data = self.extract_api_calls_from_llm_answer(response_json)
        return llm_data

        #return response_json

