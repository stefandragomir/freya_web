import os

from fy_args   import FY_Arguments
from fy_logger import FY_Logger
from fy_config import FY_Config
from fy_com    import FY_Com
from fy_env    import FY_Environment

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Freya(object):

    def __init__(self):

        self.env = FY_Environment()

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

        self.env.logger.info("Starting Freya Server...")
        
        _com = FY_Com(self.env)
        
        _com.start()

        self.__env.logger.info("Done")

    def stop(self):

        self.env.load()

        self.env.logger.info("Stopping Freya Server...")

        _com = FY_Com(self.env)
        
        _com.stop()

        self.env.lock.release()

        self.env.logger.info("Done")

    def restart(self):

        self.stop()

        self.start()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    Freya().run()
