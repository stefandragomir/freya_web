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

        self.cwd           = os.getcwd()
        self.name          = ""
        self.path          = ""
        self.path_lock     = ""
        self.path_config   = ""
        self.path_log      = ""
        self.config        = None
        self.logger        = None

    def __check_env(self):
        
        if not os.path.exists(self.path):
            raise FY_Err_Env_Inconsistent("Environment path does not exist")

        if not os.path.exists(self.path_config):
            raise FY_Err_Env_Inconsistent("Environment configuration path does not exist")

        if not os.path.exists(self.path_log):
            raise FY_Err_Env_Inconsistent("Environment log path does not exist")

        self.__get_lock()

    def __get_lock(self):

        if not self.__is_lock():        
            FY_Write_Txt_File(self.path_lock, str(os.getpid()))
        else:
            _pid = FY_Read_Txt_File(self.path_lock)
            raise FY_Err_Env_Lock("Another process is using this environment with PID [%s]" % (_pid))

    def __is_lock(self):

        return os.path.exists(self.path_lock )

    def __release_lock(self):

        _locked = self.__is_lock()

        if __locked:        

            FY_Delete_File(self.path_lock)

    def __load_paths(self,name):

        self.name          = name
        self.path          = os.path.join(self.cwd,name)
        self.path_config   = os.path.join(self.path,'config')
        self.path_log      = os.path.join(self.path,'log')
        self.path_lock     = os.path.join(self.path,'freya.lock')

    def __unload_paths(self):

        self.name          = ""
        self.path          = ""
        self.path_config   = ""
        self.path_log      = ""
        self.path_lock     = ""

    def create(self,name):
        
        self.__load_paths(name)

        #check if and environment with this name exists
        if os.path.exists(self.path):
            raise FY_Err_Env_Exists("Environment %s already exists" % (self.name,))         

        #create the environment folder      
        FY_Create_Dir(self.path)

        #create configuration folder
        FY_Create_Dir(self.path_config)

        #create log folder
        FY_Create_Dir(self.path_log)

        #create default configuration file and store path
        _paths_config = os.path.join(self.path_config,"default.config")

        _path_default_config = os.path.split(__file__)[0]
        _path_default_config = os.path.join(_path_default_config,'default.config')

        _default_config = FY_Read_Txt_File(_path_default_config)
        FY_Write_Txt_File(_paths_config, _default_config)

    def load(self,name):

        #load all paths except the configuration files
        self.__load_paths(name)

        #check if the environment is consistent
        self.__check_env()

        #load the configuration files
        self.config = FY_Config(self.path_config)
        self.config.load()

        #create the log file
        self.logger = FY_Logger(
                                name='freya',
                                console=True,
                                path=self.path_log,
                                level=self.config.logger.level,
                                max_size=self.config.logger.max_size)

        #lock the environment
        self.__path_lock = os.path.join(self.path,'freya.pid')
        

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

    def run(self):

        _args = FY_Arguments().get_arguments()

        if _args.start != None:
            self.__start(_args.start)

        if _args.stop != None:
            self.__stop(_args.stop)

        if _args.restart != None:
            self.__restart(_args.restart)

        if _args.createenv != None:
            self.__create_env(_args.createenv)

    def __create_env(self,name):

        self.__env.create(name)

    def __start(self,name):

        self.__env.load(name)

        self.__env.logger.info("Starting Freya Server...")
        
        _com = FY_Com(self.__env)
        print(_com)
        _com.start()

        self.__env.logger.info("Done")

    def __stop(self,name):

        self.__env.load(name)

        self.__env.logger.info("Stopping Freya Server...")

        self.__env.logger.info("Done")

    def __restart(self,name):

        self.__stop(name)

        self.__start(name)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

    Freya().run()
