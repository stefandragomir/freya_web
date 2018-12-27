"""
--start
--stop
--restart
--createenv
"""
import sys
from argparse                           import ArgumentParser

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Arguments(object):

    def __init__(self):

        self.__arg_parser = ArgumentParser()

        self.__add_arguments()

    def __add_arguments(self):        
        """Define all arguments for the PGB admin"""

        self.__arg_parser.add_argument('-st'      , '--start',      action='store_true',  help='start the freya web server with the env the CWD' )  
        self.__arg_parser.add_argument('-sp'      , '--stop',       action='store_true',  help='stop the freya webs server with the env the CWD' )  
        self.__arg_parser.add_argument('-rs'      , '--restart',    action='store_true',  help='restart the freya webs server with the env the CWD' ) 
 
    def get_arguments(self):
        """Parse command line arguments"""

        if len(sys.argv) == 1:
        
            self.__arg_parser.print_help()

            sys.exit(1)

        return self.__arg_parser.parse_args()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""