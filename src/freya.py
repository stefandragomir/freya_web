
from time      import sleep
from fy_args   import FY_Arguments
from fy_host   import FY_Hosts
from fy_env    import FY_Environment
from fy_ctrl   import FY_CtrlServer
from fy_ctrl   import FY_CtrlClient

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Freya():

    def __init__(self):

        self.env   = FY_Environment()
        self.hosts = None

    def run(self):

        _args = FY_Arguments().get_arguments()

        if _args.start:

            self.start()

        if _args.stop:
            
            self.stop()

        if _args.restart:
            
            self.restart()

        if _args.init:

            self.init()

    def init(self):
        
        self.env.create()

    def start(self):

        self.env.load()

        self.env.lock.acquire()

        self.env.logger.info("Starting Freya...")

        self.hosts = FY_Hosts(self.env)

        self.hosts.start()

        self.env.logger.debug("Starting Freya Control Server port [{}]".format(self.env.config.ctrl.port))

        _ctrl_server = FY_CtrlServer(
                                        port=self.env.config.ctrl.port,
                                        shutdown=self.shutdown,
                                        logger=self.env.logger)

        _ctrl_server.start()

        self.env.lock.release()

    def shutdown(self):

        self.hosts.stop()

    def stop(self):

        self.env.load()

        self.env.logger.info("Stopping Freya Server...")

        _ctrl_client = FY_CtrlClient(
                                        port=self.env.config.ctrl.port,
                                        logger=self.env.logger)

        _ctrl_client.connect()

        _ctrl_client.shutdown()

        self.env.logger.info("Done")

    def restart(self):

        self.stop()

        sleep(5)

        self.start()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    Freya().run()
