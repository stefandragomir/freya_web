
from datetime  import datetime
from time      import gmtime
from time      import strftime

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Time():

    def __init__(self):

        pass
        
    @staticmethod
    def timestamp_1():

        return strftime("%d_%m_%Y_%H_%M_%S", gmtime()) 

    @staticmethod
    def timestamp_2():

        return datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")