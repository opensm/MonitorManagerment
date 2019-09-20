#!/usr/bin/env python
# encoding:utf-8
import sys
from qcloudsms_py import SmsVoicePromptSender
from qcloudsms_py.httpclient import HTTPError


class VoiceSend:

    def __init__(self):
        self.__id = 
        self.__key = ""
        self.vp = SmsVoicePromptSender(self.__id, self.__key)

    def send_voice(self, tellist, massage):
        """
        :param tellist:
        :param massage:
        :return:
        """
        start_msg = u'系统警报:'
        end_msg = u'请尽快处理'
        try:
            status = self.vp.send(
                "86", tellist, 2, "%s%s,%s" % (start_msg, massage, end_msg), playtimes=2, ext="server alert!"
            )
            if int(status["result"]) != 0:
                raise Exception(u"语音接口异常导致报警无法发出,可能导致报警积压,请尽快处理,ErrNo:%d,Errmsg:%s" % (
                    status['result'], status['errmsg']))
            return True
        except HTTPError as e:
            return False
        except Exception as e:
            return False
