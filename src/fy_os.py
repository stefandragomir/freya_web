import os
import shutil

from fy_err import FY_Err_Copy_File
from fy_err import FY_Err_Move_File
from fy_err import FY_Err_Delete_File
from fy_err import FY_Err_Copy_Dir
from fy_err import FY_Err_Move_Dir
from fy_err import FY_Err_Delete_Dir
from fy_err import FY_Err_Breakeup_Path

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Process(object):

    error = PGB_ERROR.ALL_OK
    _log   = None

    def __init__(self, cwd, user, logger)
        self.error     = PGB_ERROR.ALL_OK
        self._log      = log

    def get_env(self):

        _env = os.environ.copy()

        return _env

    def get_command(self,command,user):
        """
        Prepare command for execution
        """
        # on windows we can pass the comand as a single string because cmd.exe will interpret the string
        # on UNIX systems we have two choices we use shell=True(which we will never use) so we must specify each argument with shlex
        if os.name != 'nt':

            command = shlex.split(command)

            if user != '':
                #see ticket #131
                command = ["sudo", "-u", user] + command
                #command = command

        return command

    def check_reponse(self,std_err,user):
        """
        Check if response contains Linux errors
        """
        self.error = PGB_ERROR.ALL_OK

        if re.match("Sorry, user",std_err) != None:
            self.error = PGB_ERROR.ERROR_COULD_EXEC_CMD_USER
            if self._log != None:
                self._log.error(self.error,"The user %s does not have access to execute this command" % (user,))

        return self.error

    def call(self,command,cwd="",user='pgb'):

        self.error = PGB_ERROR.ALL_OK

        _std_out = ""
        _std_err = ""
        command = self.get_command(command,user)

        if self._log != None:
            self._log.debug("CMD CWD: %s" % (cwd,))
            self._log.debug("CMD    : %s" % (str(command),))

        try:
            _proc = Popen(
                            command,
                            bufsize=0,
                            executable=None, 
                            stdin=None, 
                            stdout=PIPE, 
                            stderr=PIPE, 
                            preexec_fn=None, 
                            close_fds=False, 
                            shell=False, 
                            cwd=cwd, 
                            env=self.get_env(),
                            universal_newlines=False, 
                            startupinfo=None, 
                            creationflags=0)
        except:
            self.error = PGB_ERROR.ERROR_COULD_NOT_EXECUTE_CMD
            if self._log != None:
                self._log.error(self.error,"Could not execute command [%s] at cwd [%s]" % (command,cwd))

        if PGB_ERROR.ALL_OK == self.error:
            _std_out, _std_err = _proc.communicate()
            self.error = self.check_reponse(_std_err,user)

        return self.error, _std_out, _std_err

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

         _cwd  = os.path.split(path)[0]
         _proc = FY_Process(cwd=_cwd,user=None,logger=self.__logger)

        _std_out, _std_err = _proc.call(cmd="chown %s %s" % (new_owner,path))

    def set_object_group(self,path,new_group):

        _error = PGB_ERROR.ALL_OK

        _cwd = os.path.split(path)[0]

        _error, _std_out, _std_err = self.__proc.call(
                                                        command="chgrp %s %s" % (new_group,path), 
                                                        cwd=_cwd, 
                                                        user=cmd_owner)

        return _error

    def set_object_mode(self,path,mode):

        _error = PGB_ERROR.ALL_OK

        _cwd = os.path.split(path)[0]

        _error, _std_out, _std_err = self.__proc.call(
                                                        command="chmod %s %s" % (mode,path),
                                                        cwd=_cwd,
                                                        user=cmd_owner)

        return _error

    def set_object_owner_r(self,path,new_owner):

        _error = PGB_ERROR.ALL_OK

        _cwd = os.path.split(path)[0]

        _error, _std_out, _std_err = self.__proc.call(
                                                        command="chown -R %s %s" % (new_owner,path), 
                                                        cwd=_cwd, 
                                                        user=cmd_owner)

        return _error

    def set_object_group_r(self,path,new_group):

        _error = PGB_ERROR.ALL_OK

        _cwd = os.path.split(path)[0]

        _error, _std_out, _std_err = self.__proc.call(
                                                        command="chgrp -R %s %s" % (new_group,path), 
                                                        cwd=_cwd, 
                                                        user=cmd_owner)

        return _error

    def set_object_mode_r(self,path,mode):

        _error = PGB_ERROR.ALL_OK

        _cwd = os.path.split(path)[0]

        _error, _std_out, _std_err = self.__proc.call(
                                                        command="chmod -R %s %s" % (mode,path),
                                                        cwd=_cwd,
                                                        user=cmd_owner)

        return _error

    def set_dir_ac(self,path,owner,group,mode):

        _error = PGB_ERROR.ALL_OK

        _comps = list(os.walk(path))


        for _path, _dirs, _files in reversed(_comps):

            #for all files
            for _file in _files:

                _file_path = os.path.join(_path,_file)

                if PGB_ERROR.ALL_OK == _error:

                    _error = self.set_object_mode(_file_path,cmd_owner,mode)

                    if PGB_ERROR.ALL_OK == _error:

                        _error = self.set_object_owner(_file_path,cmd_owner,owner)

                        if PGB_ERROR.ALL_OK == _error:

                            _error = self.set_object_group(_file_path,cmd_owner,group)

            #for all dirs
            for _dir in _dirs:

                _dir_path = os.path.join(_path,_dir)

                if PGB_ERROR.ALL_OK == _error:

                    _error = self.set_object_mode(_dir_path,cmd_owner,mode)

                    if PGB_ERROR.ALL_OK == _error:

                        _error = self.set_object_owner(_dir_path,cmd_owner,owner)

                        if PGB_ERROR.ALL_OK == _error:

                            _error = self.set_object_group(_dir_path,cmd_owner,group)

        return _error

    def set_dir_ac_r(self,path,owner,group,mode):

        _error = PGB_ERROR.ALL_OK


        _error = self.set_object_mode_r(path,cmd_owner,mode)

        if PGB_ERROR.ALL_OK == _error:

            _error = self.set_object_owner_r(path,cmd_owner,owner)

            if PGB_ERROR.ALL_OK == _error:

                _error = self.set_object_group_r(path,cmd_owner,group)


        return _error

    def set_file_ac(self,path,owner,group,mode):

        _error = PGB_ERROR.ALL_OK

        if PGB_ERROR.ALL_OK == _error:

            _error = self.set_object_mode(path,cmd_owner,mode)

            if PGB_ERROR.ALL_OK == _error:

                _error = self.set_object_owner(path,cmd_owner,owner)

                if PGB_ERROR.ALL_OK == _error:

                    _error = self.set_object_group(path,cmd_owner,group)

        return _error