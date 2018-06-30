import sys
import zipfile
import os

from datetime               import datetime
from time                   import gmtime
from time                   import strftime
from fy_err  				import FY_Err_Send_Email
from smtplib                import SMTP         as SMTP
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from fy_os                  import FY_Touch
from fy_os                  import FY_Append_To_Txt_File
from fy_os                  import FY_Delete_File

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
class FY_Notifications(object):

    COMMASPACE = ', '

    def __init__(self,host,port,logger=None):

        self.__logger   = logger
        self.__host     = host
        self.__port     = port

    def send(self,sender,receivers,cc,bcc,subject,message):
     
        receivers = list(set(receivers))

        try:
            
            _msg = MIMEMultipart('alternative')
            _msg.attach(MIMEText(message, 'html'))
            
            _msg['Subject'] = subject
            _msg['From']    = sender
            _msg['To']      = self.COMMASPACE.join(receivers)
            
            _smtp = SMTP(self.__host, self.__port)
            
            _smtp.sendmail(sender, receivers, _msg.as_string())
            _smtp.quit()

        except:

        	raise FY_Err_Send_Email

            if self.__logger != None:

                self.__logger.error("Could not send email to %s" % (str(receivers),))

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class FY_Logger(object):
    """
    Logger levels:
     - info
     - warning
     - error
     - debug
    """

    def __init__(self, name="", console=True, path, level='info'):

        self.__console     = console
        self.__path        = path
        self.__level       = level
        self.__name        = name

        _file_name = "freya_%s.log" % (name,)

        self.__path  = os.path.join(self.__path,_file_name)

        if not os.path.exists(self.__path):
            FY_Touch(self.__path)

    def __log(self,txt,level):

        _date    = datetime.now().strftime("%I:%M:%S %p %d-%B-%Y")

        _log_txt = "[%s] [%s]      -> %s" % (_date,level.upper(),txt)

        if self.__console:
            sys.stdout.write(_log_txt + "\n")

        self.__log_to_file(_log_txt + "\n")

    def __log_to_file(self,txt):

        #in case the log file is to big we will archive it
        if self._is_log_to_big():
            self._archive_log()

        FY_Append_To_Txt_File(self.__path,txt)

    def _is_log_to_big(self):
        _is_big = False

        #check if file is larger then 50MB
        if os.path.getsize(self.__path) >= 34000000:
            _is_big = True

        return _is_big

    def _archive_log(self):
        
        _archive_path = os.path.join(os.path.split(self.__path)[0],"freya_log_archive")

        if not os.path.exists(_archive_path):
            os.makedirs(_archive_path)

        _name = "freya_log_%s" % (self.__name,)

        _archive_path = os.path.join(_archive_path,strftime(_name + "_%d_%m_%Y_%H_%M_%S.zip", gmtime()))

        _arch = zipfile.ZipFile(_archive_path, mode='w')

        _arch.write(
                    self.__path,
                    os.path.basename(self.__path), 
                    compress_type=zipfile.ZIP_DEFLATED)

        _arch.close()

        FY_Delete_File(self.__path)

    def info(self,txt):

        self.__log(txt,'info')

    def warning(self,txt):

        self.__log(txt,'warning')

    def error(self,txt):

        self.__log(txt,'error')

    def debug(self,txt):

        self.__log(txt,'debug')
