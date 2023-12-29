import os

from threading import Thread
from threading import Event
from time      import sleep
from fy_fm     import FY_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_OS():

    def __init__(self):

        pass

    @staticmethod
    def is_windows():

        return os.name == 'nt'

    @staticmethod
    def cwd():

        return FY_Dir(os.path.abspath(os.getcwd()))

    @staticmethod
    def pid():

        return os.getpid()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Cmd():

    _log   = None

    def __init__(self, cwd, user, logger):

        self.__cwd    = cwd
        self.__user   = user
        self.__logger = logger

    def __get_env(self):

        _env = os.environ.copy()

        return _env

    def __get_command(self,cmd):
        
        if FY_OS.is_windows():
            pass
        else:

            cmd = shlex.split(cmd)

            if user != None:

                cmd = ["sudo", "-u", self.__user] + cmd

        return cmd

    def __check_reponse(self,_std_out,std_err):
        """
        Check if response contains errors
        """

        pass

    def call(self,cmd):

        _std_out = ""
        _std_err = ""

        cmd = self.__get_command(cmd)

        if self.__logger != None:
            self.__logger.debug("CMD CWD: %s" % (self.__cwd.path,))
            self.__logger.debug("CMD    : %s" % (str(cmd),))

        try:
            _proc = Popen(
                            cmd,
                            bufsize=0,
                            executable=None, 
                            stdin=None, 
                            stdout=PIPE, 
                            stderr=PIPE, 
                            preexec_fn=None, 
                            close_fds=False, 
                            shell=False, 
                            cwd=self.__cwd.path, 
                            env=self.__get_env(),
                            universal_newlines=False, 
                            startupinfo=None, 
                            creationflags=0)
        except:

            raise FY_Err_Cmd

            if self.__logger != None:
                self.__logger.error("Could not execute command [%s] at cwd [%s]" % (cmd,self.__cwd.path))

        _std_out, _std_err = _proc.communicate()

        self.__check_reponse(_std_out,_std_err)

        return _std_out, _std_err

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Thread(Thread):

    def __init__(self,name,runnable,logger):

        Thread.__init__(self)

        self.name            = name
        self.logger          = logger
        self.runnable        = runnable      
        self.__stop_event    = Event()
        self.__stopped_event = Event()

        self.logger.debug("FY_Thread: creating thread [{}]".format(self.name))

    def end(self):

        self.logger.debug("FY_Thread: stopping thread [{}]".format(self.name,))

        self.__stopped_event.clear()

        self.__stop_event.set()
        
        self.__stopped_event.wait(1)

    def begin(self):

        self.logger.debug("FY_Thread: starting thread [{}]".format(self.name,))

        self.__stop_event.clear()
        
        self.__stopped_event.clear()        

        self.start()

    def run(self,*args):

        self.logger.debug("FY_Thread: running thread: [{}]".format(self.name,))

        while not self.__stop_event.wait(0.1):  

            self.runnable(*args)                      

            sleep(2) 
            
        self.__stop_event.clear()

        self.__stopped_event.set()

        self.logger.debug("FY_Thread: stopped thread [{}]".format(self.name,))

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Err_Cmd(Exception):
    pass