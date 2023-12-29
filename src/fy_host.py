
from fy_os             import FY_OS
from fy_os             import FY_Thread
from fy_types          import FY_Base_List
from fy_socket         import FY_Socket
from functools         import partial

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Host():

    def __init__(self,host,logger):

        self.host   = host
        self.logger = logger
        self.thread = None
        self.conn   = None

    def start(self):

        self.logger.debug("FY_Host: start [{}]".format(self.host.name))

        self.conn = FY_Socket(
                                    self.host.host,
                                    self.host.port,
                                    self.logger)

        self.conn.open()

        self.thread = FY_Thread(
                                self.host.name,
                                partial(self.run, self.host, self.conn),
                                self.logger)

        self.thread.begin()  

    def stop(self):

        self.logger.debug("FY_Host: stop [{}]".format(self.host.name))

        self.thread.end()

    def run(self,host,conn):

        conn.listen(max_conn=host.max_connections)

        _data = conn.read(nob=1024)

        _data = _data.decode("utf-8")

        print(_data)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Hosts():

        def __init__(self,env):

            self.env   = env
            self.hosts = FY_Base_List()

        def start(self):

            self.env.logger.debug("FY_Hosts: start")

            for _config_host in self.env.config.hosts:

                _host = FY_Host(_config_host, self.env.logger)

                self.hosts.add(_host)

                _host.start()  

        def stop(self):

            self.env.logger.debug("FY_Hosts: stop")

            for _host in self.hosts:

                _host.stop()

            self.hosts = FY_Base_List()



