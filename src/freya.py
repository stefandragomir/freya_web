import os

from fy_args   import FY_Arguments
from fy_os     import FY_Create_Dir
from fy_os     import FY_Read_Txt_File
from fy_os     import FY_Write_Txt_File
from fy_os     import FY_Delete_File
from fy_err    import FY_Err_Env_Inconsistent
from fy_err    import FY_Err_Env_Exists
from fy_err    import FY_Err_Env_Lock
from fy_logger import FY_Logger
from fy_config import FY_Config
from fy_com    import FY_Com


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Environment(object):

    def __init__(self):

        self.path_dir      = ""
        self.path_lock     = ""
        self.path_config   = ""
        self.path_log      = ""
        self.config        = None
        self.logger        = None

    def __check_env(self):

        if not os.path.exists(self.path_dir):
            raise FY_Err_Env_Inconsistent("Environment path does not exist")

        if not os.path.exists(self.path_config):
            raise FY_Err_Env_Inconsistent("Environment configuration path does not exist")

        if not os.path.exists(self.path_log):
            raise FY_Err_Env_Inconsistent("Environment log path does not exist")

    def get_lock(self):

        # TO RMEOVE

        # if not self.__is_lock():        
        #     FY_Write_Txt_File(self.path_lock, str(os.getpid()))
        # else:
        #     _pid = FY_Read_Txt_File(self.path_lock)
        #     raise FY_Err_Env_Lock("Another process is using this environment with PID [%s]" % (_pid))

        pass

    def __is_lock(self):

        return os.path.exists(self.path_lock)

    def __release_lock(self):

        if self.__is_lock():        

            FY_Delete_File(self.path_lock)

    def __load_paths(self,path):
        
        path = os.path.abspath(path)

        self.path_dir      = os.path.split(path)[0] 
        self.path_config   = path
        self.path_log      = os.path.join(self.path_dir, 'freya.log')
        self.path_lock     = os.path.join(self.path_dir, 'freya.pid')

        if not os.path.exists("freya.log"):
            
            FY_Write_Txt_File(self.path_log, "")

    def __unload_paths(self):

        self.path_dir      = ""
        self.path_config   = ""
        self.path_log      = ""
        self.path_lock     = ""

    def load(self,path):

        #load all paths except the configuration files
        self.__load_paths(path)

        #check if the environment is consistent
        self.__check_env()

        #load the configuration files
        self.config = FY_Config(self.path_config)
        self.config.load()

        #create the log file
        self.logger = FY_Logger(
                                console=True,
                                path=self.path_log,
                                level=self.config.logger.level,
                                max_size=self.config.logger.max_size)

    def unload(self):

        self.config = None
        self.logger = None

        self.__release_lock()

        self.__unload_paths()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Freya(object):

    def __init__(self):

        self.__env = FY_Environment()

    def __get_default_env_path(self):

        _path = os.path.split(__file__)[0]
        _path = os.path.split(_path)
        _path = os.path.join("freya.config")

        return _path

    def run(self):

        _args = FY_Arguments().get_arguments()

        if _args.start != None:

            self.__start()

        if _args.stop != None:
            
            self.__stop()

        if _args.restart != None:
            
            self.__restart()

    def __start(self):

        self.__env.load(self.__get_default_env_path())

        self.__env.get_lock()

        self.__env.logger.info("Starting Freya Server...")
        
        _com = FY_Com(self.__env)
        
        _com.start()

        self.__env.logger.info("Done")

    def __stop(self):

        self.__env.load()

        self.__env.logger.info("Stopping Freya Server...")

        _com = FY_Com(self.__env)
        
        _com.stop()

        self.__env.logger.info("Done")

    def __restart(self):

        self.__stop()

        self.__start()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    Freya().run()
