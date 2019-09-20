import uuid

from django.db import models

from rbac.models import UserInfo


# Create your models here.

class MonitorAccount(models.Model):
    monitor_choice = {
        ('ZABBIX', 'ZABBIX'),
        ('PROMETHEUS', '普罗米修斯'),
        ('CONSUL', 'Consul')
    }
    request_choice = {
        ('http', 'http'),
        ('https', 'https')
    }
    title = models.CharField(verbose_name='报警名称', max_length=64)
    secret_id = models.CharField(verbose_name='监控用户', max_length=64)
    secret_key = models.CharField(verbose_name='监控密码', max_length=64)
    host = models.GenericIPAddressField(verbose_name="监控IP")
    port = models.IntegerField(verbose_name="监控端口")
    monitor_type = models.CharField(verbose_name='监控类型', choices=monitor_choice, max_length=64)
    request_type = models.CharField(verbose_name="请求方式", choices=request_choice, max_length=6)
    create_user = models.CharField(verbose_name='监控用户', max_length=50)
    create_date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    class Meta:
        verbose_name_plural = "监控系统信息"


class AlertPrometheus(models.Model):
    alert_status = {
        ('firing', '报警中'),
        ('resolved', '已解决')
    }
    event_id = models.UUIDField(verbose_name="动作id", default=uuid.uuid3(uuid.NAMESPACE_DNS, "Alert"), unique=True)
    status = models.CharField(verbose_name='状态', max_length=64, default='firing', choices=alert_status)
    labels = models.TextField(verbose_name="资源信息", default=None, max_length=500)
    annotations = models.TextField(verbose_name="报警内容", default=None, max_length=500)
    startsAt = models.DateTimeField(verbose_name='开始报警时间')
    endsAt = models.DateTimeField(verbose_name='结束报警时间')
    generatorURL = models.URLField(verbose_name="产生报警URL", max_length=300)
    record_time = models.DateTimeField(verbose_name='记录报警时间', auto_now_add=True)

    class Meta:
        index_together = ["event_id"]
        verbose_name_plural = "普罗米修斯报警汇总"


class AlertFormat(models.Model):
    status_choice = {
        ("firing", "报警中"),
        ("resolved", "已解决"),
    }
    alertname = models.CharField(verbose_name="报警项", max_length=20, default=None)
    contact_rule = models.ForeignKey(verbose_name="报警规则", to="ContactRule", on_delete=False, default=None)
    status = models.CharField(verbose_name="发送状态", choices=status_choice, max_length=10, default="firing")
    job = models.CharField(verbose_name="主机组", max_length=20, default=None)
    instance = models.CharField(verbose_name="数据源", max_length=20, default=None)
    project = models.CharField(verbose_name="数据源", max_length=20, default=None)
    severity = models.CharField(verbose_name="报警等级", max_length=20, default=None)
    tag = models.TextField(verbose_name="报警备注", max_length=2000, default="")
    description = models.TextField(verbose_name="报警描述", max_length=5000, default=None)
    startsAt = models.DateTimeField(verbose_name="变更时间")

    class Meta:
        verbose_name_plural = "报警汇总消息"
        index_together = ['job', 'severity']


class AlertMessage(models.Model):
    status_choice = {
        (1, "已发送"),
        (2, "未发送"),
        (3, "发送失败")
    }
    status = models.IntegerField(verbose_name="发送状态", choices=status_choice)
    contact_user = models.ForeignKey(verbose_name="接收人", on_delete=False, to="ContactUser", default=None)
    message = models.TextField(verbose_name="发送消息内容", max_length=2000, default="")
    startsAt = models.DateTimeField(verbose_name="变更时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = "报警消息发送状态"


class ContactUser(models.Model):
    choice = {
        ("Wechat", "微信"),
        ("Voice", "电话"),
        ("Sms", "短信"),
        ("Email", "邮件")
    }
    contact_user = models.ForeignKey(verbose_name="用户ID", to=UserInfo, on_delete=False, default=None)
    contact_address = models.CharField(verbose_name="接收地址", max_length=200, default=None)
    contact_group = models.ForeignKey(verbose_name="发送规则组", to="ContactGroup", default=None, on_delete=False)
    contact_level = models.IntegerField(verbose_name="发送优先级(数字)", default=0)
    contact_type = models.CharField(verbose_name="接收类型", choices=choice, max_length=10, default="Voice")
    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = "发送联系人"
        unique_together = ['contact_user', 'contact_type']


class ContactGroup(models.Model):
    contact_choice = {
        ("VoiceMessage", "语音"),
        ("SmsMessage", "短信"),
        ("EmailMessage", "邮件"),
        ("WechatMessage", "微信")
    }
    group_name = models.CharField(verbose_name="联系组名", max_length=50, default=None)
    contact_type = models.CharField(verbose_name="消息方法", choices=contact_choice, default=None, max_length=20)
    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    def __str__(self):
        return "%s--%s" % (self.group_name, self.contact_type)


class ContactRule(models.Model):
    rule_choice = {
        ("Level1", "严重"),
        ("Level2", "一般"),
        ("Level3", "普通"),
    }
    rule_name = models.CharField(verbose_name="规则名称", max_length=40, default=None)
    regex_rule = models.CharField(verbose_name="匹配规则", max_length=60, default=None)
    contact_group = models.ForeignKey(verbose_name="发送规则组", to=ContactGroup, default=None, on_delete=False)
    severity = models.CharField(verbose_name="报警等级", max_length=20, choices=rule_choice, default=None)
    create_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    def __str__(self):
        return self.rule_name

    class Meta:
        verbose_name_plural = "发送规则"
        unique_together = ['regex_rule', 'severity', 'contact_group']
