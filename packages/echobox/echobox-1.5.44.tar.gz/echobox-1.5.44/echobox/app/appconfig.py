from echobox.tool.utils import Singleton


class ConfigData():
    __metaclass__ = Singleton

    def __init__(self):
        self._env = None
        self._app_name = None
        self._app_config = {}

    def get_env(self):
        return self._env

    def get_app_name(self):
        return self._app_name

    def init(self, app_name, env=None, app_config={}):
        self._app_name = app_name
        if env is not None:
            self._env = env
        self._app_config = app_config

    def get_app_config(self):
        return self._app_config


appconfig = ConfigData()
