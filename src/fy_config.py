import json
import os
from pprint    import pprint
from fy_err    import FY_Err_Config

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


    def __print(self):

        _txt = ""
        _txt += "HOST     : %s\n" % (self.host,)
        _txt += "PORT     : %s\n" % (self.port,)
        _txt += "RECEIVERS: %s\n" % (self.receivers,)
        _txt += "CC       : %s\n" % (self.cc,)
        _txt += "BCC      : %s\n" % (self.bcc,)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Logger(object):

    def __init__(self):

        self.use      = False
        self.max_size = ""
        self.level    = ""

    def __print(self):

        _txt = ""
        _txt += "USE        : %s\n" % (self.use,)
        _txt += "MAX SIZE   : %s\n" % (self.max_size,)
        _txt += "LEVEL      : %s\n" % (self.level,)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Socket(object):

    def __init__(self):

        self.host            = None
        self.port            = None
        self.max_connections = None

    def __print(self):

        _txt = ""
        _txt += "HOST   : %s\n" % (self.host,)
        _txt += "PORT   : %s\n" % (self.port,)
        _txt += "MAX CON: %s\n" % (self.max_connections,)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Host(object):

    def __init__(self):

        self.name     = ""
        self.socket   = _FY_Config_Socket()

    def __print(self):

        _txt = ""
        _txt += "HOST NAME: %s\n" % (self.name,)
        _txt += str(self.socket)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Config(object):

    def __init__(self,path):

        self.path            = path
        self.notifications   = _FY_Config_Notifications()
        self.logger          = _FY_Config_Logger()
        self.hosts           = []

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
                            self.hosts[-1].socket.host = data['hosts'][_host_name]['socket']['host']
                        else:
                            raise FY_Err_Config("Missing configuration: hosts->host->socket->host")

                        if 'port' in data['hosts'][_host_name]['socket']:
                            self.hosts[-1].socket.port = data['hosts'][_host_name]['socket']['port']
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

        with open(self.path,'r') as _config_file:

            _data = json.load(_config_file)

        self.__load_logger(_data)
        self.__load_notifications(_data)
        self.__load_hosts(_data)

    def __print(self):

        _txt = ""
        _txt += "PATH %s\n" % (self.path,)
        _txt += "---------------------------------------\n"
        _txt += str(self.notifications)
        _txt += "---------------------------------------\n"
        _txt += str(self.logger)
        _txt += "---------------------------------------\n"

        for _host in self.hosts:
            _txt += "---------------------------------------\n"
            _txt += str(_host)
            _txt += "---------------------------------------\n"

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()      



