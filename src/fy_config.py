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

    def __load_notifications(self,data):

        if 'notifications' in data.keys():
            if 'host' in data['notifications'].keys():
                self.notifications.host = data['notifications']['host']
            else:
                raise FY_Err_Config("Missing configuration: notifications->host")
            
            if 'port' in data['notifications'].keys():
                self.notifications.port = data['notifications']['port']
            else:
                raise FY_Err_Config("Missing configuration: notifications->port")
            
            if 'receivers' in data['notifications'].keys():
                self.notifications.receivers = data['notifications']['receivers']
            else:
                raise FY_Err_Config("Missing configuration: notifications->receivers")

            if 'cc' in data['notifications'].keys():
                self.notifications.cc = data['notifications']['cc']
            else:
                raise FY_Err_Config("Missing configuration: notifications->cc")
            
            if 'bcc' in data['notifications'].keys():
                self.notifications.bcc = data['notifications']['bcc']
            else:
                raise FY_Err_Config("Missing configuration: notifications->bcc")

        else:
            raise FY_Err_Config("Missing configuration: notifications")
        
    def __load_logger(self,data):

        if 'logger' in data.keys():
            if 'use' in data['logger'].keys():
                self.logger.use = data['logger']['use']=="True"
            else:
                raise FY_Err_Config("Missing configuration: logger->use")
            if 'max_size' in data['logger'].keys():
                self.logger.max_size = data['logger']['max_size']
            else:
                raise FY_Err_Config("Missing configuration: logger->max_size")
            if 'level' in data['logger'].keys():
                self.logger.level = data['logger']['level']
            else:
                raise FY_Err_Config("Missing configuration: logger->level")
        else:
            raise FY_Err_Config("Missing configuration: logger")

    def load(self):

        _data = {}

        self.__get_config_files()

        _json_datas = []

        for _path_config in self.__paths_configs:

            with open(_path_config) as _config_file:

                _json_datas.append(json.load(_config_file))

        for _json_data in _json_datas:

            _data = {**_data,**_json_data}

        self.__load_logger(_data)
        self.__load_notifications(_data)

        



