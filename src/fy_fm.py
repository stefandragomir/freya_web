'''
Freya File Management
'''

import os
import shutil
import shlex
import json
import stat
import zipfile

from fy_err     import FY_Err_Type
from fy_err     import FY_Not_Implemented
from copy       import deepcopy

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
            raise FY_Err_Breakeup_Path(self.path)

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
                raise FY_Err_Create_Dir(self.path)

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
            raise FY_Err_Delete_Dir(self.path)

    def file(self,name):

        _file = FY_File(self.path)
        _file.join(name)

        return  _file

    def file_txt(self,name):

        _file = FY_File_Txt(self.path)
        _file.join(name)

        return  _file

    def file_bin(self,name):

        _file = FY_File_Bin(self.path)
        _file.join(name)

        return  _file

    def file_json(self,name):

        _file = FY_File_Json(self.path)
        _file.join(name)

        return  _file

    def file_zip(self,name):

        _file = FY_File_Zip(self.path)
        _file.join(name)

        return  _file

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
                _txt = "source: {} destination: {}".format(self.path,dest)
                raise FY_Err_Copy_File(_txt)

        else:
            raise FY_Err_Type("Destination path should be of type FY_File")

    def move(self,dest):

        if isinstance(dest,FY_File):       
            try:
                shutil.move(src, dest)
            except:
                _txt = "source: {} destination: {}".format(self.path,dest)
                raise FY_Err_Move_File(_txt)
        else:
            raise FY_Err_Type("Destination path should be of type FY_File")

    def delete(self):

        try:
            os.chmod(self.path ,stat.S_IWRITE)
            os.remove(self.path)

            if os.path.isfile(self.path):
                try:
                    os.remove(self.path)
                except:
                    raise FY_Err_Delete_File(self.path)
            
        except:
            raise FY_Err_Delete_File(self.path)

    def touch(self):

        if not self.exists():

            try:
                with open(self.path,'w+') as _file:

                    _file.write("")
            except:
                raise FY_Err_Touch(self.path)

    def dir(self):

        return FY_Dir(self.root().path)

    def size(self):

        return os.path.getsize(self.path)

    def ext(self):

        return os.path.splitext(self.path)[1]

    def write(self,data):

        raise FY_Not_Implemented

    def read(self):

        raise FY_Not_Implemented

    def append(self,data):

        raise FY_Not_Implemented

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
class FY_File_Txt(FY_File):

    def __init__(self,path):

        FY_File.__init__(self,path)

    def write(self,data):

        try:
            with open(self.path,'w+') as _file:

                _file.write(str(data))
        except:
            raise FY_Err_Write_Txt_File

    def read(self):

        _data = ""

        try:
            with open(self.path,'r') as _file:

                _data = _file.read()
        except:
            raise FY_Err_Read_Txt_File

        return _data

    def append(self,data):

        try:
            with open(self.path,'a') as _file:

                _file.write(data)
        except:
            raise FY_Err_Append_To_Txt_File

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_File_Bin(FY_File):

    def __init__(self,path):

        FY_File.__init__(self,path)

    def write_bin(self,data):

        try:
            with open(path,'wb') as _file:

                _file.write(data)
        except:
            raise FY_Err_Write_Binary_File

    def read_bin(self):

        _data = ""

        try:
            with open(self.path,'rb') as _file:

                _data = _file.read()
        except:
            raise FY_Err_Read_Binary_File

        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_File_Json(FY_File):

    def __init__(self,path):

        FY_File.__init__(self,path)

    def write(self,data):
 
        with open(self.path, "w") as _file:

            _file.write(json.dumps(data, indent=4))

    def read(self):

        _data = {}

        with open(self.path,'r') as _file:

            _data = json.load(_file)

        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_File_Zip(FY_File):

    def __init__(self,path):

        FY_File.__init__(self,path)

    def write(self,path):

        _arch = zipfile.ZipFile(self.path, mode='w')

        _arch.write(
                    path.path,
                    self.dir(), 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

    def read(self):

        raise FY_Not_Implemented

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