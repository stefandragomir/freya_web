import os

from fy_args import FY_Arguments
from fy_os   import FY_Create_Dir
from fy_os   import FY_Read_Txt_File
from fy_os   import FY_Write_Txt_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Environment(object):

	def __init__(self,cwd):
		"""
		Description:
			Constructor for the Freya environment object
			This class will contain all paths to all files needed by freya from an environment
			This class will also contain the methods for:
				- creating an environment
				- checking if an environment is ok
				- loading an environment
		Args:
	        path (string): path to the folder where the environment is or will be 

    	Returns:
        	nothing
		"""

		self.__cwd           = os.getcwd()
		self.__name          = None
		self.__path          = None
		self.__path_pid      = None
		self.__path_config   = None
		self.__path_log      = None

		self.__paths_configs = []
		self.__paths_logs    = []

	def __check_env(self):

		pass

	def create_env(self,name):
		"""
		Description:
			Method that will create a fresh environment

		Args:
	        name (string): name of the environment

    	Returns:
        	nothing
		"""

		self.__path = os.path.join(self.__cwd,name)

		#check if and environment with this name exists
		if os.path.exists(self.__path):
			

		#create the environment folder
		self.__name = name


		#create configuration folder and store path
		self.__path_config   = os.path.join(self.__path,'config')
		FY_Create_Dir(self.__path_config)

		#create pid file and store path
		self.__path_pid      = os.path.join(self.__path,'freya.pid')
		FY_Write_Txt_File(self.__path_pid, str(os.getpid()))

		#create log folder and store path
		self.__path_log      = os.path.join(self.__path,'log')
		FY_Create_Dir(self.__path_log)

		#create default configuration file and store path
		self.__paths_configs = [os.path.join(self.__path_config,"default.config")]

		_path_default_config = os.path.split(__file__)[0]
		_path_default_config = os.path.join(_path_default_config,'default.config')

		_default_config = FY_Read_Txt_File(_path_default_config)
		FY_Write_Txt_File(self.__paths_configs[0], _default_config)

	def load_env(self):

		pass

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Freya(object):

	def __init__(self):
		"""
		Description:
			Main class for the Freya Web Server
			It will interpret the command line parameters and execute them
		
		Args:
	        none

    	Returns:
        	nothing
		"""

		self.__env = FY_Environment()

	def run(self):

		_args = FY_Arguments().get_arguments()

		if _args.start != None:
			self.__start(self.__env)

		if _args.stop != None:
			self.__stop(self.__env)

		if _args.restart != None:
			self.__restart(self.__env)

		if _args.createenv != None:
			self.__create_env(self.__env,_args.createenv)

	def __create_env(self,env):

		self.__env.create_env()

	def __start(self,env):

		pass

	def __stop(self,env):

		pass

	def __restart(self,env):

		self.__stop(env)

		self.__start(env)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
if __name__ == "__main__":

	Freya().run()
