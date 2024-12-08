from cbr_athena.schemas.llm_actions               import LLM__Request
from cbr_athena.schemas.llm_actions.LLM__Response import LLM__Response
from osbot_utils.base_classes.Kwargs_To_Self      import Kwargs_To_Self


class LLM__Action(Kwargs_To_Self):

    request : LLM__Request
    response: LLM__Response