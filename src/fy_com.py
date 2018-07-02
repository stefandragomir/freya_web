
import socket

from threading import Thread
from threading import Event
from time      import sleep

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def _FY_Com_Socket(object):

    def __init__(self,logger):

        self.__logger     = logger
        self.__socket     = None
        self.__connection = None
        self.__address    = None
        self.host         = None
        self.port         = None

    def write(self,data):

        self.__logger.debug("Socket: writting data [%s]" % (data,))

        self.__connection.send(data)

    def read(self,nr_of_bytes):
        
        _data = self.__connection.recv(nr_of_bytes)

        self.__logger.debug("Socket: read data [%s]" % (_data,))

        return _data

    def open(self,host,port):

        self.__logger.debug("Socket: Opening socket on %s with port %s" % (host,port))

        self.__socket = socket.socket(
                                        socket.AF_INET, 
                                        socket.SOCK_STREAM)

        self.__socket.bind((host, port))

        self.__logger.debug("Socket: Socket opened")

    def wait_for_connection(self,max_connections):

        self.__logger.debug("Socket: waiting for connection...")

        self.__socket.listen(max_connections)

        self.__logger.debug("Socket: connection detected")

        self.__connection, self.__address = self.__socket.accept()

        self.__logger.debug("Socket: connection accepted")

    def close(self):

        self.__env.logger.debug("Socket: Closing socket")

        self.__socket.close()


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class _FY_Com_Thread(object):

    def __init__(self,host,logger):

        self.__host   = host
        self.__logger = logger

        #initialise the thread object
        Thread.__init__(self)

        #create control events
        self._stop_event    = Event()
        self._stopped_event = Event()

    def stop_running(self):

        #reset the confirmed stop event just in case
        self._stopped_event.clear()

        #trigger the stop event
        self._stop_event.set()
        
        #wait to see if the thread stopped
        self._stopped_event.wait(1)

    def start_running(self):

        #clear the two control events
        self._stop_event.clear()
        self._stopped_event.clear()

        self.start()

    def run(self):

        self.__socket = _FY_Com_Socket(self.__logger)

        self.__socket.open(self.__host.socket.host,self.__host.socket.port)

        while not self._stop_event.wait(0.1):                           
            
            self.__socket.wait_for_connection(self.__host.socket.max_connections)

            _data = self.__socket.read(4096)

            if _data:
                
                print(data)

        #clear the stop event
        self._stop_event.clear()

        #trigger the confirmation event to tell all this thread has stopped      
        self._stopped_event.set()
           
        
"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Com(object):

    def __init__(self,env):

        self.__env          = env
        self.__host_threads = []

    def start(self):

        for _host in self.__env.config.hosts:

            _thread = _FY_Com_Thread(_host,self.__env.logger)
            _thread.start_running()

            self.__host_threads.append(_thread)

    def stop(self):

        for _thread in self.__host_threads:

            _thread.stop_running()





