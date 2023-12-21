import sys

from fy_os import FY_Dir
from fy_os import FY_File_Txt
from fy_os import FY_OS

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Logger(object):

    def __init__(self,console,path,level,max_size):

        self.console     = console
        self.path        = path.file_txt("log")
        self.level       = level
        self.max_size    = max_size
        self.archive     = self.path.dir()

        self.archive.join("archive")

        self.path.touch()

        if not self.archive.exists():

            self.archive.create()

    def __is_log_level(self,level):

        _log = False

        if self.level == "debug":
            _log = True
        else:
            if self.level == 'error':
                if level == 'info' or level == 'warning' or level == 'error':
                    _log = True
            else:
                if self.level == 'warning':
                    if level == 'info' or level == 'warning':
                        _log = True
                else:
                    if self.level == 'info':
                        if level == 'info':
                            _log = True
        return _log

    def __log(self,txt,level):

        if self.__is_log_level(level):

            _log_txt = "[{}] [{}]      -> {}".format(FY_OS.timestamp_2(),level.upper(),txt)

            _log_txt_console = " -> {}".format(txt,)

            if self.console:

                sys.stdout.write(_log_txt_console + "\n")

            self.__log_to_file(_log_txt + "\n")

    def __log_to_file(self,txt):

        if self.path.size() >= int(self.max_size):

            _archive_path = self.archive.file_zip("{}.zip", FY_OS.timestamp_1())

            _archive_path.write(self.path)

            self.path.delete()

        self.path.append(txt)

    def info(self,txt):

        self.__log(txt,'info')

    def warning(self,txt):

        self.__log(txt,'warning')

    def error(self,txt):

        self.__log(txt,'error')

    def debug(self,txt):

        self.__log(txt,'debug')
