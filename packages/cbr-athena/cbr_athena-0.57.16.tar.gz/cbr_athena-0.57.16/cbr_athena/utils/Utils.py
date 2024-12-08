from os import environ

from osbot_utils.utils.Misc import date_time_now


class Utils:

    @staticmethod
    def current_execution_env():
        return environ.get('EXECUTION_ENV', 'LOCAL')

    def date_today(self):
        return date_time_now(date_time_format='%Y-%m-%d')       # force the correct value of date