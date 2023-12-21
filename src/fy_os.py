import os
import shutil
import shlex

from datetime               import datetime
from time                   import gmtime
from time                   import strftime
from fy_err                 import FY_Err_Type
from copy                   import deepcopy


"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_OS():

    def __init__(self):

        pass

    def is_windows(self):

        return os.name == 'nt'

    def cwd(self):

        return FY_Dir(os.path.abspath(os.getcwd()))

    def pid(self):

        return os.getpid()

    def timestamp(self):

        return strftime("%d_%m_%Y_%H_%M_%S", gmtime()) 

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Process():

    _log   = None

    def __init__(self, cwd, user, logger):

        self.__cwd    = cwd
        self.__user   = user
        self.__logger = logger

    def __get_env(self):

        _env = os.environ.copy()

        return _env

    def __get_command(self,cmd):
        
        if FY_OS().is_windows():
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

            raise FY_Err_Call_Process

            if self.__logger != None:
                self.__logger.error("Could not execute command [%s] at cwd [%s]" % (cmd,self.__cwd.path))

        _std_out, _std_err = _proc.communicate()

        self.__check_reponse(_std_out,_std_err)

        return _std_out, _std_err

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Path():

    def __init__(self,path):

        self.path = os.path.abspath(path.strip())

    def exists(self):

        return os.path.exists(self.path)

    def is_empty(self):

        return self.path == ''

    def breakup():

        _path       = self.path
        _components = [self]
        _remainder  = FY_Path("")

        try:
            while _remainder != '':

                _component,_remainder = os.path.split(_path)

                if _remainder != '':
                    _components.append(FY_Path(_component))
                    _path = _component
        except:
            raise FY_Err_Breakeup_Path

        return _components

    def join(self,*components):

        self.path = os.path.join(self.path,*components)

    def split(self):

        self.path = os.path.split(self.path)[0]

    def root(self):

        return FY_Path(os.path.split(self.path)[0])

    def file(self):

        return os.path.split(self.path)[1]

    def is_file(self):

        return os.path.isfile(self.path)

    def is_dir(self):

        return os.path.isfile(self.path)

    def duplicate(self):

        return deepcopy(self)

    def __print(self):

        _txt = "PATH: [{}]".format(self.path)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Dir(FY_Path):

    def __init__(self,path):

        FY_Path.__init__(self,path)

    def create(self):

        if not self.exists():

            try:
                os.makedirs(self.path)
            except:
                raise FY_Err_Create_Dir

    def copy(self,dest):

        if isinstance(dest,FY_Dir):

            try:
                shutil.copytree(self.path, dest.path)
            except:
                raise FY_Err_Copy_Dir
        else:
            raise FY_Err_Type("Destination path should be of type FY_Dir")

    def move(self,dest):

        if isinstance(dest,FY_Dir):

            try:
                shutil.move(self.path, dest.path)
            except:
                raise FY_Err_Move_Dir

        else:
            raise FY_Err_Type("Destination path should be of type FY_Dir")

    def delete(self):

        try:
            shutil.rmtree(path)
        except:
            raise FY_Err_Delete_Dir

    def file(self,name):

        return  FY_File(self.path).join(name)

    def add(self,name):

        _path = FY_Dir(self.path)

        _path.join(name)

        return _path

    def __print(self):

        _txt = "DIR: [{}]".format(self.path)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_File(FY_Path):

    def __init__(self,path):

        FY_Path.__init__(self,path)

    def copy(self,dest):

        if isinstance(dest,FY_File):

            _comps = dest.breakup()

            _comps = _comps[1:-1]

            for _comp in reversed(_comps):

                if not _comp.exists:

                    os.mkdir(_comp)

            try:
                shutil.copyfile(self.path, dest.path)
            except:
                raise FY_Err_Copy_File

        else:
            raise FY_Err_Type("Destination path should be of type FY_File")

    def move(self,dest):

        if isinstance(dest,FY_File):       
            try:
                shutil.move(src, dest)
            except:
                raise FY_Err_Move_File
        else:
            raise FY_Err_Type("Destination path should be of type FY_File")

    def delete(self):

        try:
            os.chmod(self.path ,stat.S_IWRITE)
            os.remove(self.path)

            if os.path.isfile(path):
                try:
                    os.remove(path)
                except:
                    raise FY_Err_Delete_File
            
        except:
            raise FY_Err_Delete_File

    def touch(self):

        if not self.exists():

            try:
                with open(path,'w+') as _file:

                    _file.write("")
            except:
                raise FY_Err_Touch

    def write_txt(self,data):

        try:
            with open(self.path,'w+') as _file:

                _file.write(data)
        except:
            raise FY_Err_Write_Txt_File

    def write_bin(self,data):

        try:
            with open(path,'wb') as _file:

                _file.write(data)
        except:
            raise FY_Err_Write_Binary_File

    def read_txt(self):

        _data = ""

        try:
            with open(self.path,'r') as _file:

                _data = _file.read()
        except:
            raise FY_Err_Read_Txt_File

        return _data

    def append_txt(self,data):

        try:
            with open(self.path,'a') as _file:

                _file.write(data)
        except:
            raise FY_Err_Append_To_Txt_File

    def read_bin(self):

        _data = ""

        try:
            with open(self.path,'rb') as _file:

                _data = _file.read()
        except:
            raise FY_Err_Read_Binary_File

        return _data

    def dir(self):

        return self.root()

    def size(self):

        return os.path.getsize(self.path)

    def ext(self):

        return os.path.splitext(self.path)[1]

    def __print(self):

        _txt = "FILE: [{}]".format(self.path)

        return _txt

    def __str__(self):

        return self.__print()

    def __repr__(self):

        return self.__print()

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Err_Copy_File(Exception):
    pass

class FY_Err_Move_File(Exception):
    pass

class FY_Err_Delete_File(Exception):
    pass

class FY_Err_Copy_Dir(Exception):
    pass 

class FY_Err_Move_Dir(Exception):
    pass

class FY_Err_Delete_Dir(Exception):
    pass

class FY_Err_Breakeup_Path(Exception):
    pass

class FY_Err_Read_Txt_File(Exception):
    pass

class FY_Err_Write_Txt_File(Exception):
    pass

class FY_Err_Read_Binary_File(Exception):
    pass

class FY_Err_Write_Binary_File(Exception):
    pass

class FY_Err_Append_To_Txt_File(Exception):
    pass

class FY_Err_Touch(Exception):
    pass

class FY_Err_Create_Dir(Exception):
    pass

class FY_Err_Call_Process(Exception):
    pass