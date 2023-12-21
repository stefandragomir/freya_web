import sys
import zipfile
import os

from fy_os import FY_Dir
from fy_os import FY_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Logger(object):

    def __init__(self,console,path,level,max_size):

        self.console     = console
        self.path        = path
        self.level       = level
        self.max_size    = max_size
        self.archive     = self.path.dir().join("archive")

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

            _date    = datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")

            _log_txt = "[%s] [%s]      -> %s" % (_date,level.upper(),txt)

            _log_txt_console = " -> %s" % (txt,)

            if self.__console:

                sys.stdout.write(_log_txt_console + "\n")

            self.__log_to_file(_log_txt + "\n")

    def __log_to_file(self,txt):

        if self.path.size() >= int(self.max_size):

            self.__archive_log()

        self.path.append_txt(txt)

    def __archive_log(self):

        _archive_path = self.archive.file("{}.zip", FY_OS().timestamp())

        _arch = zipfile.ZipFile(_archive_path.path, mode='w')

        _arch.write(
                    self.path.path,
                    self.path.dir.path, 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

        self.path.delete()

    def info(self,txt):

        self.__log(txt,'info')

    def warning(self,txt):

        self.__log(txt,'warning')

    def error(self,txt):

        self.__log(txt,'error')

    def debug(self,txt):

        self.__log(txt,'debug')
