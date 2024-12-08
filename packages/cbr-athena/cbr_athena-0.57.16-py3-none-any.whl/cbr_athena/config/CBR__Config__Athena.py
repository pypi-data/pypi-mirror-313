from cbr_athena.utils.Version                       import version__cbr_athena
from cbr_shared.config.CBR__Config                  import CBR__Config
from cbr_shared.config.CBR__Config__Active          import CBR__Config__Active
from cbr_shared.config.CBR__Config__Data            import CBR__Config__Data
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.base_classes.Type_Safe             import Type_Safe


class CBR__Config__Athena(Type_Safe):       # todo: refactor out this method since we can now get all this from server_config__cbr_website objects which is on the cbr-shared module
    override__aws_enabled : bool

    def aws_enabled(self):
        if self.cbr_config().aws_enabled():
            return True
        if self.override__aws_enabled:
            return True
        return False

    def aws_disabled(self):
        enabled = self.aws_enabled()
        return enabled == False

    @cache_on_self
    def cbr_config(self) -> CBR__Config:
        return self.cbr_config_active().cbr_config

    @cache_on_self
    def cbr_config_active(self) -> CBR__Config__Active:
        return self.cbr_config_data().create_cbr_config_active__from_current_config_file()

    def cbr_config_data(self):
        return CBR__Config__Data()

    def cbr_config_athena(self):
        cbr_config = self.cbr_config()
        return dict(aws_enabled = self.aws_enabled() ,
                    cbr_config  = cbr_config         ,
                    version     = version__cbr_athena)

cbr_config_athena = CBR__Config__Athena()