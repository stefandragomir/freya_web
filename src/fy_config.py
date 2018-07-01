import json
import os
from pprint import pprint

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Notifications(object):

    def __init__(self):

        self.host      = None
        self.port      = None
        self.receivers = []
        self.cc        = []
        self.bcc       = []

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Logger(object):

    def __init__(self):

        self.use      = False
        self.max_size = ""
        self.level    = ""

"""****************************************************************************
*******************************************************************************
****************************************************************************"""

class FY_Config(object):

    def __init__(self,path):

        self.__path          = path
        self.__paths_configs = []
        self.notifications   = _FY_Config_Notifications()
        self.logger          = _FY_Config_Logger()

    def __get_config_files(self):

        self.__paths_configs = []

        for _root, _dirs, _files in os.walk(self.__path):
            
            for _file in _files:
                
                self.__paths_configs.append(os.path.join(_root, _file))

    def load(self):

        self.__get_config_files()

        _data = []

        for _path_config in self.__paths_configs:

            with open(_path_config) as _config_file:

                _data.append(json.load(_config_file))

        pprint(_data) 




