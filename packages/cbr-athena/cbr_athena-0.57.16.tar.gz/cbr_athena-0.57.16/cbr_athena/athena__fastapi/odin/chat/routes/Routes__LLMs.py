from cbr_athena.athena__fastapi.odin.FastApi_Header_Auth                import route_with_auth
from cbr_athena.athena__fastapi.odin.chat.Odin__Execute__Workflow       import Odin__Execute__Workflow
from cbr_athena.athena__fastapi.odin.chat.Odin__LLM_Prompt__Workflow    import Odin__LLM_Prompt__Workflow
from cbr_athena.athena__fastapi.routes.Fast_API_Route                   import Fast_API__Routes
from cbr_athena.schemas.for_fastapi.LLM_Prompt                          import LLM_Prompt

FAST_API_ROUTES__ODIN__CHAT__LLMS = ['/llms/execute-task-from-llm-prompt', '/llms/prompt-to-answer', '/llms/prompt-to-api']

class Routes__LLMs(Fast_API__Routes):
    path_prefix           : str = "llms"
    odin_llm_prompt       : Odin__LLM_Prompt__Workflow
    odin_execute_workflow : Odin__Execute__Workflow


    def add_routes(self):

        @route_with_auth(self.router, 'post', '/execute-task-from-llm-prompt')
        def execute_task__from__llm_prompt(llm_prompt: LLM_Prompt):
            return self.odin_execute_workflow.execute_task__from__llm_prompt(llm_prompt)

        @route_with_auth(self.router, 'post', '/prompt-to-answer')
        def prompt_to_answer(llm_prompt: LLM_Prompt):
            return self.odin_llm_prompt.prompt_to_answer(llm_prompt)

        @route_with_auth(self.router, 'post', '/prompt-to-api')
        def prompt_to_api(llm_prompt : LLM_Prompt):
            return self.odin_llm_prompt.prompt_to_api(llm_prompt)




