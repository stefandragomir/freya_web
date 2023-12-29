
import socket

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Socket(object):

    def __init__(self,host,port,logger):

        self.logger     = logger
        self.socket     = None
        self.connection = None
        self.address    = None
        self.host       = host
        self.port       = port

    def open(self):

        self.logger.debug("FY_Socket: [{}]:[{}] open".format(self.host,self.port))

        self.socket = socket.socket(
                                        socket.AF_INET, 
                                        socket.SOCK_STREAM)

        self.socket.bind((self.host, self.port))

        self.logger.debug("FY_Socket: [{}]:[{}] opened".format(self.host,self.port))

    def connect(self):

        self.logger.debug("FY_Socket: [{}]:[{}] connect".format(self.host,self.port))

        self.socket = socket.socket(
                                        socket.AF_INET, 
                                        socket.SOCK_STREAM)

        self.socket.connect((self.host, self.port))

        self.logger.debug("FY_Socket: [{}]:[{}] connected".format(self.host,self.port))  

    def listen(self,max_conn):

        self.logger.debug("FY_Socket: [{}]:[{}] waiting for connection".format(self.host,self.port))

        self.socket.listen(max_conn)

        self.connection, self.address = self.socket.accept()

        self.logger.debug("FY_Socket: [{}]:[{}] connection accepted from [{}]".format(self.host,self.port,self.address))

    def write(self,data):

        self.logger.debug("FY_Socket: [{}]:[{}] write [{}]".format(self.host,self.port,data,))

        self.socket.sendall(data)

    def read(self,nob):
        
        _data = self.connection.recv(nob)

        self.logger.debug("FY_Socket: [{}]:[{}] read [{}]".format(self.host,self.port,_data,))

        return _data

    def close(self):

        self.logger.debug("FY_Socket: close socket")

        self.socket.close()
       