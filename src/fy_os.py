import os
import shutil
import shlex

from fy_err  import FY_Err_Copy_File
from fy_err  import FY_Err_Move_File
from fy_err  import FY_Err_Delete_File
from fy_err  import FY_Err_Copy_Dir
from fy_err  import FY_Err_Move_Dir
from fy_err  import FY_Err_Delete_Dir
from fy_err  import FY_Err_Breakeup_Path
from fy_err  import FY_Err_Call_Process
from fy_err  import FY_Err_Append_To_Txt_File
from fy_err  import FY_Err_Read_Txt_File
from fy_err  import FY_Err_Write_Txt_File
from fy_err  import FY_Err_Read_Binary_File
from fy_err  import FY_Err_Write_Binary_File
from fy_err  import FY_Err_Touch
from fy_err  import FY_Err_Create_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_IsWindows():

    _state = False

    if os.name == 'nt':

        _state = True

    return _state

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Process(object):

    _log   = None

    def __init__(self, cwd, user, logger):

        self.__cwd    = cwd
        self.__user   = user
        self.__logger = logger

    def __get_env(self):

        _env = os.environ.copy()

        return _env

    def __get_command(self,cmd):
        
        if FY_IsWindows():
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
            self.__logger.debug("CMD CWD: %s" % (self.__cwd,))
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
                            cwd=self.__cwd, 
                            env=self.__get_env(),
                            universal_newlines=False, 
                            startupinfo=None, 
                            creationflags=0)
        except:

            raise FY_Err_Call_Process

            if self.__logger != None:
                self.__logger.error("Could not execute command [%s] at cwd [%s]" % (cmd,self.__cwd))

        _std_out, _std_err = _proc.communicate()

        self.__check_reponse(_std_out,_std_err)

        return _std_out, _std_err

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Brakeup_Path(path):
    """ Receive a path and return a list of all subpaths in that path"""

    _components = [path]
    _remainder  = None

    try:
        while _remainder != '':

            _component,_remainder = os.path.split(path)

            if _remainder != '':
                _components.append(_component)
                path = _component
    except:
        raise FY_Err_Breakeup_Path

    return _components

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Copy_File(src,dest):

    src  = os.path.normpath(src)
    dest = os.path.normpath(dest)

    #get all file path components
    #because shutil copy cannot copy 
    #a file from a folder that does not exist
    _comps = FY_Brakeup_Path(dest)

       
    #remove the drive letter and the file name
    _comps = _comps[1:-1]

    for _comp in reversed(_comps):

        #if folder does not exist we create it
        if not os.path.exists(_comp):
            os.mkdir(_comp)

    try:
        shutil.copyfile(src, dest)
    except:
        raise FY_Err_Copy_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Move_File(src,dest):

    source = os.path.normpath(source)
    dest   = os.path.normpath(dest)
   
    try:
        shutil.move(src, dest)
    except:
        raise FY_Err_Move_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Delete_File(path):

    path = os.path.normpath(path)

    try:
        os.chmod(path ,stat.S_IWRITE)
        os.remove(path)

        if os.path.isfile(path):
            try:
                os.remove(path)
            except:
                raise FY_Err_Delete_File
        
    except:
        raise FY_Err_Delete_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Copy_Dir(src,dest):

    src    = os.path.normpath(src)
    dest   = os.path.normpath(dest)

    try:
        shutil.copytree(src,dest)
    except:
        raise FY_Err_Copy_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Move_Dir(src,dest):

    src  = os.path.normpath(src)
    dest = os.path.normpath(dest)

    try:
        shutil.move(src, dest)
    except:
        raise FY_Err_Move_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Create_Dir(path):

    path  = os.path.normpath(path)

    try:
        os.makedirs(path)
    except:
        raise FY_Err_Create_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Delete_Dir(path):

    path = os.path.normpath(path)

    try:
        shutil.rmtree(path)
    except:
        raise FY_Err_Delete_Dir

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_AccessRights(object):

    def __init__(self,logger):

        self.__logger  = logger

    def set_object_owner(self,path,new_owner):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chown %s %s" % (new_owner,path))

    def set_object_group(self,path,new_group):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chgrp %s %s" % (new_group,path))

    def set_object_mode(self,path,mode):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chmod %s %s" % (mode,path))

    def set_object_owner_r(self,path,new_owner):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chown -R %s %s" % (new_owner,path))

    def set_object_group_r(self,path,new_group):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chgrp -R %s %s" % (new_group,path))

    def set_object_mode_r(self,path,mode):

        if FY_IsWindows():
            pass
        else:
            _cwd  = os.path.split(path)[0]
            _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)
            _std_out, _std_err = _proc.call(cmd="chmod -R %s %s" % (mode,path))

    def set_dir_ac(self,path,owner,group,mode):

        _comps = list(os.walk(path))

        for _path, _dirs, _files in reversed(_comps):

            #for all files
            for _file in _files:

                _file_path = os.path.join(_path,_file)

                self.set_object_mode(_file_path,mode)

                self.set_object_owner(_file_path,owner)

                self.set_object_group(_file_path,group)

            #for all dirs
            for _dir in _dirs:

                _dir_path = os.path.join(_path,_dir)

                self.set_object_mode(_dir_path,mode)

                self.set_object_owner(_dir_path,owner)

                self.set_object_group(_dir_path,group)

    def set_dir_ac_r(self,path,owner,group,mode):

        self.set_object_mode_r(path,cmd_owner,mode)

        self.set_object_owner_r(path,cmd_owner,owner)

        self.set_object_group_r(path,cmd_owner,group)

    def set_file_ac(self,path,owner,group,mode):

        self.set_object_mode(path,cmd_owner,mode)

        self.set_object_owner(path,cmd_owner,owner)

        self.set_object_group(path,cmd_owner,group)

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Touch(path):

    try:
        with open(path,'w+') as _file:

            _file.write("")
    except:
        raise FY_Err_Touch

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Write_Txt_File(path,data):

    try:
        with open(path,'w+') as _file:

            _file.write(data)
    except:
        raise FY_Err_Write_Txt_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Write_Binary_File(path,data):

    try:
        with open(path,'wb') as _file:

            _file.write(data)
    except:
        raise FY_Err_Write_Binary_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Read_Txt_File(path):
    _data = ""

    try:
        with open(path,'r') as _file:

            _data = _file.read()
    except:
        raise FY_Err_Read_Txt_File

    return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Append_To_Txt_File(path,data):
    try:
        with open(path,'a') as _file:

            _file.write(data)
    except:
        raise FY_Err_Append_To_Txt_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
def FY_Read_Binary_File(path):

    _data = ""

    try:
        with open(path,'rb') as _file:

            _data = _file.read()
    except:
        raise FY_Err_Read_Binary_File

    return _data