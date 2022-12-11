import slack_sdk
import traceback

from configobj import ConfigObj

from neal_python_library.const import CfgSectionsConst, CfgFieldsConst
from neal_python_library.utils import Convertor

class Slack:
    def __init__(self, token, channel):
        self._token = token
        self._channel = channel
        
        self._slack_client = slack_sdk.WebClient(token = self._token) if token else None

    def post_msg(self, msg: str):
        if self._slack_client:
            self._slack_client.chat_postMessage(channel = self._channel, text = msg)


class SlackReporter:
    def __init__(self, cfg: ConfigObj):

        # Init parameters
        self._cfg = cfg

        self._slack_cfg = self._cfg[CfgSectionsConst.SLACK]

        try:
            self._slack_token = self._slack_cfg[CfgFieldsConst.TOKEN]
        except:
            self._slack_token = None

        try:
            self._slack_channel = self._slack_cfg[CfgFieldsConst.CHANNEL]
        except:
            self._slack_channel = None

        self._members_id = Convertor.load_strs_list_cfg(self._slack_cfg, CfgFieldsConst.MEMBER_ID)

        # Init Slack obj
        self._slack = Slack(self._slack_token, self._slack_channel)

    def report(self, subject = None, text = None, mention = True):
        try:
            # Generate formatted msg with members id
            format_members_id = ['<@{}>'.format(member_id) for member_id in self._members_id]
            msg_members_id = ' '.join(format_members_id)

            msgs_list = [subject, text]

            if mention:
                msgs_list.append(msg_members_id)
            
            msgs = '\n'.join(msgs_list)

            # Chat post message
            self._slack.post_msg(msgs)
        
        except:
            print('Slack reporter error: {}'.format(traceback.format_exc()))