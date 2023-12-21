
from fy_types import FY_Base_List

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Config_Notifications(object):

    def __init__(self):

        self.host      = "localhost"
        self.port      = "587"
        self.receivers = [""]
        self.cc        = [""]
        self.bcc       = [""]

    def load(self,data):

        if 'host' in data.keys():
            self.host = data['host']
        else:
            raise FY_Err_Config("Missing configuration: notifications->host")
        
        if 'port' in data.keys():
            self.port = data['port']
        else:
            raise FY_Err_Config("Missing configuration: notifications->port")
        
        if 'receivers' in data.keys():
            self.receivers = data['receivers']
        else:
            raise FY_Err_Config("Missing configuration: notifications->receivers")

        if 'cc' in data.keys():
            self.cc = data['cc']
        else:
            raise FY_Err_Config("Missing configuration: notifications->cc")
        
        if 'bcc' in data.keys():
            self.bcc = data['bcc']
        else:
            raise FY_Err_Config("Missing configuration: notifications->bcc")

    def serial(self):

        return {
                    "host"     : self.host,
                    "port"     : self.port,
                    "receivers": self.receivers,
                    "cc"       : self.cc,
                    "bcc"      : self.bcc
                }

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
        self.max_size = "50000000"
        self.level    = "debug"

    def load(self,data):

        if 'use' in data.keys():
            self.use = data['use']=="True"
        else:
            raise FY_Err_Config("Missing configuration: logger->use")
        if 'max_size' in data.keys():
            self.max_size = data['max_size']
        else:
            raise FY_Err_Config("Missing configuration: logger->max_size")
        if 'level' in data.keys():
            self.level = data['level']
        else:
            raise FY_Err_Config("Missing configuration: logger->level")

    def serial(self):

        return {
                    "use"      : self.use,
                    "max_size" : self.max_size,
                    "level"    : self.level,
                }

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

        self.host            = "localhost"
        self.port            = "80"
        self.max_connections = "1"

    def load(self,data):

        if 'max_connection' in data:
            self.max_connection = data['max_connection']
        else:
            raise FY_Err_Config("Missing configuration: hosts->host->socket->max_connection")

        if 'host' in data:
            self.host = data['host']
        else:
            raise FY_Err_Config("Missing configuration: hosts->host->socket->host")

        if 'port' in data:
            self.port = data['port']
        else:
            raise FY_Err_Config("Missing configuration: hosts->host->socket->port")

    def serial(self):

        return {
                    "host"            : self.host,
                    "port"            : self.port,
                    "max_connections" : self.max_connections,
                }

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

    def load(self,data):

        if 'socket' in data.keys():

            self.socket.load(data['socket'])

        else:
            raise FY_Err_Config("Missing configuration: hosts->host->socket")            

    def serial(self):

        return {
                    "socket" : self.socket.serial(),
                }

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
class _FY_Config_Hosts(FY_Base_List):

    def __init__(self):

        FY_Base_List.__init__(self)

    def load(self,data):

        if len(data) > 0:

            for _name in data:

                _host = _FY_Config_Host()

                _host.name = _name

                _host.load(data[_name])

                self.add(_host)
        else:
            raise FY_Err_Config("Missing configuration: hosts->host")

    def serial(self):

        _data = {}

        for _host in self:

            _data.update({_host.name: _host.serial()})

        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Config(object):

    def __init__(self,path):

        self.path            = path.file_json("config")
        self.notifications   = _FY_Config_Notifications()
        self.logger          = _FY_Config_Logger()
        self.hosts           = _FY_Config_Hosts()

        self.hosts.add(_FY_Config_Host())
        self.hosts[-1].name = "default"

    def __load_notifications(self,data):

        self.notifications = _FY_Config_Notifications()

        if 'notifications' in data.keys():

            self.notifications.load(data["notifications"])

        else:
            raise FY_Err_Config("Missing configuration: notifications")
        
    def __load_logger(self,data):

        self.logger = _FY_Config_Logger()

        if 'logger' in data.keys():

            self.logger.load(data["logger"])

        else:
            raise FY_Err_Config("Missing configuration: logger")

    def __load_hosts(self,data):

        self.hosts = _FY_Config_Hosts()

        if 'hosts' in data.keys():

           self.hosts.load(data["hosts"])

        else:
            raise FY_Err_Config("Missing configuration: hosts")

    def load(self):

        _data = self.path.read()

        self.__load_logger(_data)
        self.__load_notifications(_data)
        self.__load_hosts(_data)

    def save(self):

        _data = {
                    "notifications": self.notifications.serial(),
                    "logger"       : self.logger.serial(),
                    "hosts"        : self.hosts.serial(),
                }

        self.path.write(_data)

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

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Err_Config(Exception):
    pass
