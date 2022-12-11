import os
import slack_sdk
import logging
import traceback

from typing import Union
from configobj import ConfigObj
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from ttcommon.dataaccess.cfg_const import CfgCommonSection, CfgFields
from ttcommon.utils.utils import CommonUtils


class SlackHandler(logging.Handler):
    def __init__(self, cfg):
        super(SlackHandler, self).__init__()

        # Init parameters
        self._cfg = cfg
        self._subject = self._cfg[CfgCommonSection.GENERAL][CfgFields.COMPONENT_ID]

        self._slack_cfg = self._cfg[CfgCommonSection.REPORT][CfgCommonSection.SLACK]

        try:
            self._slack_token = self._slack_cfg[CfgFields.TOKEN]
        except:
            self._slack_token = None

        try:
            self._slack_channel = self._slack_cfg[CfgFields.CHANNEL]
        except:
            self._slack_channel = None

        self._members_id = CommonUtils.load_strs_list_cfg(self._slack_cfg, CfgFields.MEMBER_ID)
        
        # Init Slack obj
        self._slack = Slack(self._slack_token, self._slack_channel)

    def emit(self, record) -> None:
        try:
            # Generate formatted msg with members id
            msg = self.format(record)
            
            format_members_id = ['<@{}>'.format(member_id) for member_id in self._members_id]
            msg_members_id = ' '.join(format_members_id)

            msg = '{}\n```{}```\n{}'.format(self._subject, msg, msg_members_id)

            # Chat post message
            self._slack.post_msg(msg)
        
        except:
            print('Slack handler error : {}'.format(traceback.format_exc()))      
    
    
# ==================== Logger ====================
class Logger:
    @staticmethod
    def getLogger(log_file_name: str, cfg: Union[ConfigObj, str], 
            time_rotate: bool = False, time_rotate_when = 'D', rotate: bool = False, stream: bool = True, pipe = None, 
            slack: bool = False, slack_level = logging.ERROR
        ) -> logging.Logger:
        """
        Get the logger object from logging modules

        Args:
            log_file_name (str): [The name of the log file].
            cfg (ConfigObj | str): [cfg file or the path of the cfg file].
            pipe (StreamIO, Optional): [ExtraHandler to pass through],

        Returns:
            [logging_obj]: [the logger object for logging things].
        """
        
        # Init parameters
        if isinstance(cfg, str):
            cfg = ConfigObj(cfg, interpolation = False)

        log_path = cfg[CfgCommonSection.LOG][CfgFields.LOG_PATH]
        log_suffix = cfg[CfgCommonSection.LOG][CfgFields.LOG_SUFFIX]
        
        try:
            log_format = cfg[CfgCommonSection.LOG][CfgFields.LOG_FORMAT]
        except:
            log_format = '[%(levelname)s][%(asctime)s]\n[%(funcName)s] %(message)s'

        try:
            log_level = getattr(logging, cfg[CfgCommonSection.LOG][CfgFields.LOG_LEVEL])
        except:
            log_level = logging.INFO
        
        try:
            log_stream = int(cfg[CfgCommonSection.LOG][CfgFields.LOG_STREAM_HANDLER])
        except:
            log_stream = 0

        # Turn on streamHandler only if logStreamHandler and param stream are both 1, 
        stream = log_stream and stream
        
        try:
            datetime_format = cfg[CfgCommonSection.GENERAL][CfgFields.DATETIME_FORMAT]
        except:
            datetime_format = '%Y-%m-%d %H:%M:%S'
        
        try:
            day_datetime_format = cfg[CfgCommonSection.GENERAL][CfgFields.DAY_DATETIME_FORMAT]
        except:
            day_datetime_format = '%Y-%m-%d'

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # Convert
        log_full_path = os.path.join(log_path, log_file_name + log_suffix)
        formatter = logging.Formatter(log_format, datetime_format)
        
        # Logger setup
        logger = logging.getLogger(log_full_path)
        
        if logger.hasHandlers():
            return logger
        
        logger.setLevel(log_level)

        # Time rotating file handler
        if time_rotate:
            time_rotate_file_handler = TimedRotatingFileHandler(log_full_path, when = time_rotate_when, interval = 1)
            time_rotate_file_handler.suffix = day_datetime_format
            time_rotate_file_handler.setFormatter(formatter)
            logger.addHandler(time_rotate_file_handler)
        
        # Rotating file handler
        if rotate:
            rotate_file_handler = RotatingFileHandler(log_full_path, maxBytes = (1048576 * 10), backupCount = 5)
            rotate_file_handler.setFormatter(formatter)
            logger.addHandler(rotate_file_handler)

        # Stream handler
        if stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        
        # Stream pipe handler
        if pipe:
            pipe_handler = logging.StreamHandler(pipe)
            pipe_handler.setFormatter(formatter)
            logger.addHandler(pipe_handler)

        # Slack handler
        if slack:
            slack_handler = SlackHandler(cfg)
            slack_handler.setFormatter(formatter)
            slack_handler.setLevel(slack_level)
            logger.addHandler(slack_handler)
        
        return logger
