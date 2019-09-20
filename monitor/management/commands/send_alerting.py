from django.core.management.base import BaseCommand, CommandError
from monitor.models import *
import simplejson as json
from monitor.qloud_api import VoiceSend
import logging


class FormatSendAlert(object):

    def get_alert_msg(self):
        """
        :return:
        """
        try:
            data_alert = AlertPrometheus.objects.values(
                "event_id",
                "labels",
                "annotations",
                "startsAt",
                "status"
            )
            logging.info(u"获取报警日志成功!")
            return data_alert
        except Exception as error:
            logging.error(u"获取报警日志异常:%s" % str(error))
            return {}

    def format_alert(self):
        """
        :return:
        """
        for data in self.get_alert_msg():

            labels = json.loads(str(data['labels']).replace("'", '"'))
            annotations = json.loads(str(data['annotations']).replace("'", '"'))

            try:
                rule_id = ContactRule.objects.get(job=labels['job'], severity=labels['severity'])
                alert_dict = {
                    "contact_rule": rule_id,
                    "alertname": labels['alertname'],
                    "instance": labels['instance'],
                    "job": labels['job'],
                    "project": labels['project'],
                    "severity": labels['severity'],
                    "description": annotations['description'],
                    "tag": labels,
                    "status": data['status'],
                    "startsAt": data["startsAt"]
                }
                AlertFormat.objects.get_or_create(**alert_dict)
                logging.info("格式化报警日志成功,%s" % str(alert_dict))
            except Exception as error:
                logging.error("格式化数据失败，将其存入失败列表中，%s,Error:%s" % (str(data), str(error)))
                continue

    def count_alert_message(self):
        """
        :return:
        """

        try:
            count_data = ContactUser.objects.values(
                "id",
                "contact_rule__rule_name",
                "contact_rule__alertformat__description",
                "contact_rule__alertformat__status"
            ).annotate(
                count=models.Count("contact_rule__alertformat__description")
            )
            return count_data
        except Exception as error:
            logging.error("分组报警失败,%s" % str(error))
            return {}

    def format_alert_message(self):
        """
        :return:
        """
        alert_type = {
            "firing": "报警中",
            "resolved": "报警已恢复"
        }
        for value in self.count_alert_message():
            try:
                user_object = ContactUser.objects.get(id=value['id'])
                data = {
                    "contact_user": user_object,
                    "status": 2
                }
                if len(AlertMessage.objects.filter(**data)) == 0:
                    data.update({"message": "%s:%s,%s" % (
                        value['contact_rule__rule_name'],
                        value['contact_rule__alertformat__description'],
                        alert_type[value['contact_rule__alertformat__status']]
                    )})
                    AlertMessage.objects.create(**data)
                else:
                    alert_data = AlertMessage.objects.get(**data)
                    alert_data.message = "%s,%s:%s,%s" % (
                        alert_data.message,
                        value['contact_rule__rule_name'],
                        value['contact_rule__alertformat__description'],
                        alert_type[value['contact_rule__alertformat__status']]
                    )
                    alert_data.save()
            except Exception as error:
                logging.error("汇总报警数据失败,%s" % str(error))

    def send_alerting(self):
        """
        :return:
        """
        try:
            for vs in AlertMessage.objects.values(
                    "id",
                    "contact_user__contact_address",
                    "contact_user__alertmessage__message"
            ).filter(status=2):
                v = VoiceSend()
                status = v.send_voice(
                    tellist=vs['contact_user__contact_address'],
                    massage=vs['contact_user__alertmessage__message']
                )
                alert = AlertMessage.objects.get(id=vs['id'])
                if not status:
                    alert.status = 3
                    continue
                alert.status = 1
                alert.save()
        except Exception as error:
            logging.error("发送报警失败%s" % str(error))


class Command(BaseCommand):

    def handle(self, *args, **options):
        f_ins = FormatSendAlert()
        f_ins.format_alert()
        f_ins.format_alert_message()
        f_ins.send_alerting()
        print("success")
