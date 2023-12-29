
from fy_fm     import FY_Dir
from fy_fm     import FY_File_Txt
from fy_os     import FY_OS
from fy_config import FY_Config
from fy_logger import FY_Logger

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Environment(object):

    def __init__(self):

        self.path        = FY_OS.cwd()
        self.path_config = self.path.add("config")
        self.path_log    = self.path.add("log") 
        self.path_lock   = self.path.add("lock")

        self.config      = None
        self.logger      = None
        self.lock        = None

    def __is_config_dir(self):

        return self.path_config.exists()

    def __is_log_dir(self):

        return self.path_log.exists()

    def __is_lock_dir(self):

        return self.path_lock.exists()

    def __is_env(self):

        return self.__is_config_dir() and self.__is_log_dir() and self.__is_lock_dir()

    def load(self):

        if self.__is_env():

            self.lock   = FY_Lock(self.path_lock)

            self.config = FY_Config(self.path_config)

            self.config.load()

            self.logger = FY_Logger(
                                    console=True,
                                    path=self.path_log,
                                    level=self.config.logger.level,
                                    max_size=self.config.logger.max_size)
        else:
            raise FY_Err_Env_Not_Exists("Environment not found in CWD")

    def create(self):

        if not self.__is_env():

            if not self.__is_config_dir():

                self.path_config.create()

                FY_Config(self.path_config).save()

            if not self.__is_log_dir():

                self.path_log.create()

            self.logger = FY_Logger(
                                    console=True,
                                    path=self.path_log,
                                    level="debug",
                                    max_size="50000000")

            if not self.__is_lock_dir():

                self.path_lock.create()

            self.logger.info("Created Freya Web default environment in {}".format(self.path))

        else:
            print("Freya Web environment already exists in {}".format(self.path))

        

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Lock(object):

    def __init__(self,path):

        self.path = path.file_txt("freya.pid")

    def is_lock(self):

        return self.path.exists()

    def acquire(self):

        if not self.is_lock():        
            self.path.write(FY_OS.pid())
        else:
            _pid = self.path.read()
            raise FY_Err_Env_Lock("Another process is using this environment with PID [{}]".format((_pid)))

    def release(self):

        if self.is_lock():        

            self.path.delete()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Err_Env_Not_Exists(Exception):
    pass

class FY_Err_Env_Inconsistent(Exception):
    pass

class FY_Err_Env_Lock(Exception):
    pass