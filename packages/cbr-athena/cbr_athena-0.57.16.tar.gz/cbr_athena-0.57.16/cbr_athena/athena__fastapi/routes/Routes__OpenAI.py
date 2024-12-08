
from cbr_athena.athena__fastapi.routes.Fast_API_Route                               import Fast_API__Routes
from cbr_athena.llms.storage.CBR__Chats_Storage__S3                                 import CBR__Chats_Storage__S3
from cbr_athena.schemas.for_fastapi.GPT_Audio_To_Text                               import GPT_Audio_To_Text
from cbr_athena.schemas.for_fastapi.GPT_Text_To_Audio                               import GPT_Text_To_Audio
from cbr_shared.schemas.base_models.chat_threads.GPT_Prompt_With_System_And_History import GPT_Prompt_With_System_And_History
from cbr_shared.schemas.base_models.chat_threads.LLMs__Chat_Completion              import LLMs__Chat_Completion
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from fastapi import Request

class Routes__OpenAI(Fast_API__Routes):
    path_prefix             : str = 'open_ai'
    cbr_chats_storage_s3    : CBR__Chats_Storage__S3

    @cache_on_self
    def api_open_ai(self):
        from cbr_athena.llms.API_Open_AI import API_Open_AI
        return API_Open_AI().setup()
    #
    # @cache_on_self
    # def logging(self):
    #     from cbr_athena.utils.Logging import Logging
    #     return Logging()
    #
    # def dydb_chat_threads(self):
    #     from cbr_athena.aws.dynamo_db.DyDB__CBR_Chat_Threads import DyDB__CBR_Chat_Threads
    #     return DyDB__CBR_Chat_Threads()


    async def prompt_with_system__not_stream(self, gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, request: Request):
        from cbr_athena.aws.dynamo_db.DyDB__CBR_Chat_Threads import log_llm_chat

        try:
            if self.api_open_ai().open_ai_not_available():
                return "OpenAI not available (need API Key)"
            if gpt_prompt_with_system_and_history.user_data:            # todo: refactor to use new mode
                model = gpt_prompt_with_system_and_history.user_data.get('selected_model', 'gpt-4o')
            else:
                model = 'gpt-4o'
            user_prompt     = gpt_prompt_with_system_and_history.user_prompt
            images          = gpt_prompt_with_system_and_history.images
            system_prompts  = gpt_prompt_with_system_and_history.system_prompts
            histories       = gpt_prompt_with_system_and_history.histories
            #model           = gpt_prompt_with_system_and_history.model.value
            temperature     = gpt_prompt_with_system_and_history.temperature
            seed            = gpt_prompt_with_system_and_history.seed
            max_tokens      = gpt_prompt_with_system_and_history.max_tokens
            async_mode      = False

            gpt_response    = await self.api_open_ai().ask_using_system_prompts(user_prompt=user_prompt,
                                                                                images=images,
                                                                                system_prompts=system_prompts,
                                                                                histories=histories,
                                                                                model=model,
                                                                                temperature=temperature,
                                                                                seed=seed,
                                                                                max_tokens=max_tokens,
                                                                                async_mode=async_mode)

            request_headers = {key: value for key, value in request.headers.items()}            # todo: refactor out
            log_llm_chat(gpt_prompt_with_system_and_history, gpt_response, request_headers)
            return gpt_response
        except Exception as error:
            return f'Error: {error}'

    async def prompt_with_system__stream(self, gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, request: Request):
        from starlette.responses import StreamingResponse
        from cbr_athena.aws.dynamo_db.DyDB__CBR_Chat_Threads import log_llm_chat

        request_id       = self.request_id(request)
        chat_save_result = self.cbr_chats_storage_s3.save_user_request(gpt_prompt_with_system_and_history,request_id)

        async def streamer():
            if self.api_open_ai().open_ai_not_available():
                yield "OpenAI not available (need API Key)"
                return
            if gpt_prompt_with_system_and_history.user_data:            # todo: refactor to use new mode
                model = gpt_prompt_with_system_and_history.user_data.get('selected_model', 'gpt-4o')
            else:
                model = 'gpt-4o'
            user_prompt     = gpt_prompt_with_system_and_history.user_prompt
            images          = gpt_prompt_with_system_and_history.images
            system_prompts  = gpt_prompt_with_system_and_history.system_prompts
            histories       = gpt_prompt_with_system_and_history.histories
            #model           = gpt_prompt_with_system_and_history.model.value
            temperature     = gpt_prompt_with_system_and_history.temperature
            seed            = gpt_prompt_with_system_and_history.seed
            max_tokens      = gpt_prompt_with_system_and_history.max_tokens
            async_mode      = True

            generator       = await self.api_open_ai().ask_using_system_prompts(user_prompt=user_prompt,
                                                                                images=images,
                                                                                system_prompts=system_prompts,
                                                                                histories=histories,
                                                                                model=model,
                                                                                temperature=temperature,
                                                                                seed=seed,
                                                                                max_tokens=max_tokens,
                                                                                async_mode=async_mode)


            gpt_response = ''
            async for answer in generator:
                if answer:
                    gpt_response += answer
                    yield f"{answer}\n"

            llm_chat_completion = LLMs__Chat_Completion(**gpt_prompt_with_system_and_history.model_dump())
            llm_chat_completion.llm_answer = gpt_response

            self.cbr_chats_storage_s3.save_user_response(llm_chat_completion, request_id)

            request_headers = {key: value for key, value in request.headers.items()}
            log_llm_chat(gpt_prompt_with_system_and_history, gpt_response, request_headers)


            #self.logging()          .add_prompt_request(gpt_prompt_with_system_and_history, gtp_response, request_headers)  # todo: remove this one once the dydb_chat_threads is working

        response = StreamingResponse(streamer(), media_type='text/event-stream"; charset=utf-8')
        response.headers.append('cbr__chat_id'       , chat_save_result.get('public_chat_id'        , ''))
        response.headers.append('cbr__chat_thread_id', chat_save_result.get('public_chat_thread__id', ''))
        return response

    def request_id(self, request: Request):
        if request:
            if hasattr(request.state, "request_id"):
                return request.state.request_id


    def add_routes(self):
        from starlette.responses import Response
        from osbot_utils.utils.Misc import base64_to_bytes, bytes_to_base64


        @self.router.post('/prompt_with_system__stream')
        async def prompt_with_system__stream(gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, request: Request):  # = Depends()):
            return await self.prompt_with_system__stream(gpt_prompt_with_system_and_history, request)

        @self.router.post('/audio_to_text')
        async def audio_to_text(gpt_audio_to_text: GPT_Audio_To_Text):
            audio_base_64 = gpt_audio_to_text.audio_base_64
            audio_bytes   = base64_to_bytes(audio_base_64)
            audio_text    = self.api_open_ai().audio_to_text(audio_bytes=audio_bytes)

            return Response(content=audio_text, media_type="text/plain")

        @self.router.post('/text_to_audio')
        async def text_to_audio(gpt_text_to_audio: GPT_Text_To_Audio):
            input_text  = gpt_text_to_audio.audio_text
            audio_bytes = self.api_open_ai().text_to_audio(input_text)
            audio_base_64 = bytes_to_base64(audio_bytes)
            return Response(content=audio_base_64, media_type="text/plain")
