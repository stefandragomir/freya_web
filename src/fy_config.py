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
class _FY_Config_Socket(object):

    def __init__(self):

        self.host            = None
        self.port            = None
        self.max_connections = None

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Host(object):

    def __init__(self):
        self.name     = ""
        self.socket   = _FY_Config_Socket()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""

class FY_Config(object):

    def __init__(self,path):

        self.__path          = path
        self.__paths_configs = []
        self.notifications   = _FY_Config_Notifications()
        self.logger          = _FY_Config_Logger()
        self.hosts           = []

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

    def __load_hosts(self,data):

        if 'hosts' in data.keys():

            if len(data['hosts']) > 0:

                for _host_name in data['hosts']:

                    self.hosts.append(_FY_Config_Host())

                    self.hosts[-1].name = _host_name

                    if 'socket' in data['hosts'][_host_name].keys():

                        if 'max_connection' in data['hosts'][_host_name]['socket']:
                            self.hosts[-1].socket.max_connection = data['hosts'][_host_name]['socket']['max_connection']
                        else:
                            raise FY_Err_Config("Missing configuration: hosts->host->socket->max_connection")

                        if 'host' in data['hosts'][_host_name]['socket']:
                            self.hosts[-1].socket.max_connection = data['hosts'][_host_name]['socket']['host']
                        else:
                            raise FY_Err_Config("Missing configuration: hosts->host->socket->host")

                        if 'port' in data['hosts'][_host_name]['socket']:
                            self.hosts[-1].socket.max_connection = data['hosts'][_host_name]['socket']['port']
                        else:
                            raise FY_Err_Config("Missing configuration: hosts->host->socket->port")
                    else:
                        raise FY_Err_Config("Missing configuration: hosts->host->socket")            
            else:
                raise FY_Err_Config("Missing configuration: hosts->host")
        else:
            raise FY_Err_Config("Missing configuration: hosts")

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
        self.__load_hosts(_data)

        



