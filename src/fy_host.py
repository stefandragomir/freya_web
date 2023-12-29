
from fy_os             import FY_OS
from fy_os             import FY_Thread
from fy_types          import FY_Base_List
from fy_socket         import FY_Socket

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Host():

    def __init__(self,host,logger):

        self.host   = host
        self.logger = logger
        self.thread = None

    def start(self):

        self.logger.debug("FY_Host: start [{}]".format(self.host.name))

        self.thread = FY_Thread(
                                self.host.name,
                                self.run,
                                self.logger)

        self.thread.begin()  

    def stop(self):

        self.logger.debug("FY_Host: stop [{}]".format(self.host.name))

        self.thread.end()

    def run(self):

        print("running host...")

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



