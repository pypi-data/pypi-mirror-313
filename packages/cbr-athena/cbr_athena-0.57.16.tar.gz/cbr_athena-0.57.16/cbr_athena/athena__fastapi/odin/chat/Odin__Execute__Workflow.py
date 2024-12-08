from cbr_athena.llms.providers.open_router.LLM__Open_Router import LLM__Providers, LLM__Models__Open_Router
from cbr_athena.llms.tasks.LLM__Task__Chat_Completion       import LLM__Task__Chat__Completion
from cbr_athena.schemas.for_fastapi.LLM_Prompt              import LLM_Prompt
from cbr_athena.schemas.llm_actions.LLM__Request            import LLM__Request
from osbot_utils.helpers.Random_Guid                        import Random_Guid


class Odin__Execute__Workflow:

    def execute_task__from__llm_prompt(self, llm_prompt: LLM_Prompt):
        llm_prompt_data = llm_prompt.dict()
        llm_task        = LLM__Task__Chat__Completion()

        llm_prompt_data['chat_thread_id'] = Random_Guid(llm_prompt.chat_thread_id)
        llm_prompt_data['model'         ] = LLM__Models__Open_Router.LLAMA_3_8B__FREE
        llm_prompt_data['model_provider'] = LLM__Providers.OPEN_ROUTER

        llm_request         = LLM__Request(**llm_prompt_data)
        results = []
        # for i in range(0,10):
        #     result = {**llm_task.execute(llm_request), '_index': i}
        #     results.append(result)
        result = llm_task.execute(llm_request)
        results.append(result)
        #pprint(llm_task.dydb_cbr_workflows.size())
        return results

