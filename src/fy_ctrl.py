
from fy_socket import FY_Socket


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_CtrlServer():

    def __init__(self,port,shutdown,logger):

        self.logger   = logger
        self.shutdown = shutdown
        self.conn     = FY_Socket(
                                    "127.0.0.1",
                                    port,
                                    logger)

    def start(self):

        _data = ""

        self.logger.debug("FY_CtrlServer: start port [{}]".format(self.conn.port))

        self.conn.open()

        while _data != "shutdown":

            self.conn.listen(max_conn=1)

            _data = self.conn.read(nob=1024)

            _data = _data.decode("utf-8")

            self.logger.debug("FY_CtrlServer: received [{}]".format(_data))

            if _data == "shutdown":

                self.shutdown()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_CtrlClient():

    def __init__(self,port,logger):

        self.logger = logger

        self.conn  = FY_Socket(
                                "127.0.0.1",
                                port,
                                logger)

    def connect(self):

        self.logger.debug("FY_CtrlClient: connect port [{}]".format(self.conn.port))

        self.conn.connect()

    def shutdown(self):

        self.logger.debug("FY_CtrlClient: shutdown")

        self.conn.write(bytes("shutdown",'utf-8'))



