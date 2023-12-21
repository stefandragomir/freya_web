
import socket
import signal

from threading import Thread
from threading import Event
from time      import sleep
from fy_os     import FY_OS

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Com_Socket(object):

    def __init__(self,logger):

        self.logger     = logger
        self.socket     = None
        self.connection = None
        self.address    = None
        self.host       = None
        self.port       = None

    def write(self,data):

        self.logger.debug("Socket: writting data [%s]" % (data,))

        self.connection.send(data)

    def read(self,nr_of_bytes):
        
        _data = self.connection.recv(nr_of_bytes)

        self.logger.debug("Socket: read data [%s]" % (_data,))

        return _data

    def open(self,host,port):

        self.logger.debug("Socket: Opening socket on %s with port %s" % (host,port))

        self.socket = socket.socket(
                                        socket.AF_INET, 
                                        socket.SOCK_STREAM)

        self.socket.bind((host, int(port)))

        self.logger.debug("Socket: Socket opened")

    def wait_for_connection(self,max_connections):

        self.logger.debug("Socket: waiting for connection...")

        self.socket.listen(max_connections)

        self.logger.debug("Socket: connection detected")

        self.connection, self.address = self.socket.accept()

        self.logger.debug("Socket: connection accepted")

    def close(self):

        self.logger.debug("Socket: Closing socket")

        self.socket.close()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Com_Thread(Thread):

    def __init__(self,host,logger):

        self.host   = host
        self.logger = logger

        #initialise the thread object
        Thread.__init__(self)

        #create control events
        self.__stop_event    = Event()
        self.__stopped_event = Event()

        self.logger.debug("_FY_Com_Thread: creating thread: %s" % (self.host.name,))

    def stop_running(self):

        self.logger.debug("_FY_Com_Thread: stopping thread: %s" % (self.host.name,))

        #reset the confirmed stop event just in case
        self.__stopped_event.clear()

        #trigger the stop event
        self.__stop_event.set()
        
        #wait to see if the thread stopped
        self.__stopped_event.wait(1)

    def start_running(self):

        #clear the two control events
        self.__stop_event.clear()
        self.__stopped_event.clear()

        self.logger.debug("_FY_Com_Thread: starting thread: %s" % (self.host.name,))

        self.start()

    def run(self):

        self.socket = _FY_Com_Socket(self.logger)

        self.logger.debug("_FY_Com_Thread: opening socket thread for host: %s" % (self.host.name,))

        self.socket.open(self.host.socket.host,self.host.socket.port)

        while not self.__stop_event.wait(0.1):  

            sleep(1) 
            print("tick")                        
            
            # self.__socket.wait_for_connection(self.__host.socket.max_connections)

            # _data = self.__socket.read(4096)

            # if _data:

            #     print(data)

        #clear the stop event
        self.__stop_event.clear()

        #trigger the confirmation event to tell all this thread has stopped      
        self.__stopped_event.set()

        self.logger.debug("_FY_Com_Thread: thread stopped for host: %s" % (self.host.name,))
           
"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Com(object):

    def __init__(self,env):

        self.env          = env
        self.host_threads = []

    def register_to_signals(self):

        if not FY_OS.is_windows():

            signal.signal(signal.SIGUSR1, self.clbk_signals)

    def clbk_signals(signum, stack):
    
        if signal.SIGUSR1 == signum:

            for _thread in self.host_threads:

                _thread.stop_running()

    def start(self):

        self.env.logger.debug(self.env.config)

        for _host in self.__env.config.hosts:

            _thread = _FY_Com_Thread(_host,self.env.logger)
            _thread.start_running()

            self.host_threads.append(_thread)

        self.register_to_signals()

    def stop(self):

        for _thread in self.host_threads:

            _thread.stop_running()





