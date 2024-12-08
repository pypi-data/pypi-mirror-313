from starlette.responses import StreamingResponse, Response

from fastapi import Request

from cbr_athena.athena__fastapi.routes.Fast_API_Route                           import Fast_API__Routes
from cbr_shared.schemas.base_models.chat_threads.GPT_Prompt_With_System_And_History import \
    GPT_Prompt_With_System_And_History


class Routes__Ollama(Fast_API__Routes):
    path_prefix: str = 'ollama'

    def add_routes(self):
        @self.router.post('/prompt_with_system__stream')
        async def prompt_with_system__stream(gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, request: Request):  # = Depends()):
            async def streamer():
                user_prompt     = gpt_prompt_with_system_and_history.user_prompt
                images          = gpt_prompt_with_system_and_history.images
                system_prompts  = gpt_prompt_with_system_and_history.system_prompts
                histories       = gpt_prompt_with_system_and_history.histories
                model           = gpt_prompt_with_system_and_history.model.value
                temperature     = gpt_prompt_with_system_and_history.temperature
                seed            = gpt_prompt_with_system_and_history.seed
                max_tokens      = gpt_prompt_with_system_and_history.max_tokens
                async_mode      = True
                # generator       = self.api_open_ai.ask_using_system_prompts(user_prompt=user_prompt,
                #                                                            images=images,
                #                                                            system_prompts=system_prompts,
                #                                                            histories=histories,
                #                                                            model=model,
                #                                                            temperature=temperature,
                #                                                            seed=seed,
                #                                                            max_tokens=max_tokens,
                #                                                            async_mode=async_mode)
                #
                generator = ['this is in ollama', '.', 'Also', 'here']
                gpt_response = ''
                for answer in generator:
                    if answer:
                        gpt_response += answer
                        yield f"{answer}\n"

            return StreamingResponse(streamer(), media_type="text/plain; charset=utf-8")

