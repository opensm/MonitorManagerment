from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .serializer import *


# +++++++++++++++++++++++++++++++++++++监控信息管理++++++++++++++++++++++++++++++++++
# 添加监控信息
class MonitorAddView(View):
    template_name = 'monitor/monitor_edit.html'
    view_message = "添加监控信息"

    @method_decorator(login_required)
    def get(self, request):
        monitor_register = MonitorForm()
        return render(
            request,
            self.template_name,
            {
                'monitor_register': monitor_register,
                'view_message': self.view_message
            }
        )

    @method_decorator(login_required)
    def post(self, request):
        monitor_register = MonitorForm(request.POST)
        if not monitor_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'monitor_register': monitor_register,
                    'view_message': self.view_message
                })
        try:
            monitor_register.save()
            return redirect('monitor:information_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    'monitor_register': monitor_register,
                    "error": error,
                    'view_message': self.view_message
                })


# 监控信息列表
class MonitorListView(View):
    template_name = "monitor/monitor.html"
    view_message = "监控信息列表"

    @method_decorator(login_required)
    def post(self, request):
        monitor_data = MonitorAccount.objects.order_by('create_date')
        return render(request, self.template_name, {
            "monitor_data": monitor_data,
            "view_message": self.view_message
        })

    @method_decorator(login_required)
    def get(self, request):
        monitor_data = MonitorAccount.objects.order_by('create_date')
        return render(request, self.template_name, {
            "monitor_data": monitor_data,
            "view_message": self.view_message
        })


# 编辑监控信息信息
class MonitorEditView(View):
    template_name = 'monitor/monitor_edit.html'
    view_message = "修改监控信息"

    @method_decorator(login_required)
    def post(self, request, monitor_id):
        monitor_data = get_object_or_404(MonitorAccount, pk=monitor_id)
        monitor_register = MonitorForm(request.POST, instance=monitor_data)
        if not monitor_register.is_valid():
            return render(
                request,
                self.template_name, {
                    "monitor_register": monitor_register,
                    "view_message": self.view_message
                })
        try:
            monitor_register.save()
            return redirect('monitor:information_list')
        except Exception as error:
            return render(
                request,
                self.template_name, {
                    "monitor_register": monitor_register,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, monitor_id):
        monitor_data = get_object_or_404(MonitorAccount, pk=monitor_id)
        monitor_register = MonitorForm(instance=monitor_data)
        return render(
            request,
            self.template_name, {
                "monitor_register": monitor_register,
                "view_message": self.view_message
            })


# 删除监控信息
class MonitorDelView(View):
    template_name = 'monitor/monitor.html'
    view_message = "监控信息列表"

    @method_decorator(login_required)
    def post(self, request, monitor_id):
        try:
            MonitorAccount.objects.get(pk=monitor_id).delete()
            return redirect('monitor:information_list')
        except Exception as error:
            monitor_data = MonitorAccount.objects.order_by('id')
            return render(
                request,
                self.template_name, {
                    "monitor_data": monitor_data,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, monitor_id):
        try:
            MonitorAccount.objects.get(pk=monitor_id).delete()
            return redirect('monitor:information_list')
        except Exception as error:
            monitor_data = MonitorAccount.objects.order_by('id')
            return render(
                request,
                self.template_name, {
                    "monitor_data": monitor_data,
                    "view_message": self.view_message,
                    "error": error
                })


# +++++++++++++++++++++++++++++++++++++++++++++++++报警信息删除和添加 +++++++++++++++++++++++++++++++++++++++++++
# def consul_list(monitor_type=None):
#     """
#     :return:
#     """
#     data = MonitorAccount.objects.filter(monitor_type=monitor_type)
#     for s in data:
#         print(monitor_type, s.monitor_type)
#         if s.monitor_type != monitor_type:
#             continue
#         print(111111111111111)
#         secret_id = s.secret_id
#         secret_key = s.secret_key
#         try:
#             c = consul.Consul(host=s.host, port=s.port, scheme=s.request_type)
#             for x in c.catalog.service('a8-mixed-gs')[1]:
#                 print(x)
#         except Exception as error:
#             print(error)


# 监控信息列表
class AlertPrometheusListView(View):
    template_name = "monitor/alert_prometheus.html"
    view_message = "报警列表"

    @method_decorator(login_required)
    def post(self, request):
        alert_data = AlertPrometheus.objects.order_by('startsAt')
        return render(
            request,
            self.template_name, {
                "alert_data": alert_data,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        alert_data = AlertPrometheus.objects.order_by('startsAt')
        return render(request, self.template_name, {
            "alert_data": alert_data,
            "view_message": self.view_message
        })


# 监控信息列表
class AlertMessage(View):
    template_name = "monitor/alert_message.html"
    view_message = "报警列表"

    @method_decorator(login_required)
    def post(self, request):
        alert_data = AlertMessage.objects.order_by('id')
        return render(
            request,
            self.template_name, {
                "alert_data": alert_data,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        alert_data = AlertMessage.objects.order_by('id')
        return render(request, self.template_name, {
            "alert_data": alert_data,
            "view_message": self.view_message
        })


# 删除监控信息
class AlertPrometheusDelView(View):
    template_name = 'monitor/alert_prometheus.html'
    view_message = "监控信息列表"

    @method_decorator(login_required)
    def post(self, request, event_id):
        try:
            AlertPrometheus.objects.get(event_id=event_id).delete()
            return redirect('monitor:alert_prometheus')
        except Exception as error:
            alert_register = AlertPrometheus.objects.order_by('id')
            return render(
                request,
                self.template_name, {
                    "AlertPrometheus_data": alert_register,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, event_id):
        try:
            AlertPrometheus.objects.get(event_id=event_id).delete()
            return redirect('monitor:alert_prometheus')
        except Exception as error:
            alert_register = AlertPrometheus.objects.order_by('id')
            return render(
                request,
                self.template_name, {
                    "AlertPrometheus_data": alert_register,
                    "view_message": self.view_message,
                    "error": error
                })


# ++++++++++++++++++++++++++++++++++++++++++++++++ 报警规则管理 ++++++++++++++++++++++++++++++++++++++
# 添加报警规则
class ContactRuleAddView(View):
    template_name = 'monitor/contact_rule_edit.html'
    view_message = "添加报警规则"

    @method_decorator(login_required)
    def get(self, request):
        contact_register = ContactRuleForm()
        return render(
            request,
            self.template_name,
            {
                'contact_register': contact_register,
                'view_message': self.view_message
            }
        )

    @method_decorator(login_required)
    def post(self, request):
        contact_register = ContactRuleForm(request.POST)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    'view_message': self.view_message
                }
            )
        try:
            contact_register.save()
            return redirect('monitor:rule_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    "error": error,
                    'view_message': self.view_message
                }
            )


# 报警规则列表
class ContactRuleListView(View):
    template_name = "monitor/contact_rule.html"
    view_message = "报警规则列表"

    @method_decorator(login_required)
    def post(self, request):
        contact_data = ContactRule.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        contact_data = ContactRule.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })


# 编辑报警规则
class ContactRuleEditView(View):
    template_name = 'monitor/contact_rule_edit.html'
    view_message = "修改报警规则"

    @method_decorator(login_required)
    def post(self, request, rule_id):
        contact_data = get_object_or_404(ContactRule, pk=rule_id)
        contact_register = ContactRuleForm(request.POST, instance=contact_data)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message
                })
        try:
            contact_register.save()
            return redirect('monitor:rule_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, rule_id):
        contact_data = get_object_or_404(ContactRule, pk=rule_id)
        contact_register = ContactRuleForm(instance=contact_data)
        return render(
            request,
            self.template_name,
            {
                "contact_register": contact_register,
                "view_message": self.view_message
            })


# 删除报警规则
class ContactRuleDelView(View):
    template_name = 'monitor/contact_rule.html'
    view_message = "报警规则列表"

    @method_decorator(login_required)
    def post(self, request, rule_id):
        try:
            ContactRule.objects.get(pk=rule_id).delete()
            return redirect('monitor:rule_list')
        except Exception as error:
            contact_data = ContactRule.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, rule_id):
        try:
            ContactRule.objects.get(pk=rule_id).delete()
            return redirect('monitor:rule_list')
        except Exception as error:
            contact_data = ContactRule.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++报警联系人配置++++++++++++++++++++++++++++++++++++++++++++++++
class ContactUserAddView(View):
    template_name = 'monitor/contact_user_edit.html'
    view_message = "添加报警联系人"

    @method_decorator(login_required)
    def get(self, request):
        contact_register = ContactUserForm()
        return render(
            request,
            self.template_name,
            {
                'contact_register': contact_register,
                'view_message': self.view_message
            }
        )

    @method_decorator(login_required)
    def post(self, request):
        contact_register = ContactUserForm(request.POST)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    'view_message': self.view_message
                }
            )
        try:
            contact_register.save()
            return redirect('monitor:user_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    "error": error,
                    'view_message': self.view_message
                }
            )


# 报警规则列表
class ContactUserListView(View):
    template_name = "monitor/contact_user.html"
    view_message = "报警规则联系人"

    @method_decorator(login_required)
    def post(self, request):
        contact_data = ContactUser.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        contact_data = ContactUser.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })


# 编辑报警规则
class ContactUserEditView(View):
    template_name = 'monitor/contact_user_edit.html'
    view_message = "修改报警联系人"

    @method_decorator(login_required)
    def post(self, request, user_id):
        contact_data = get_object_or_404(ContactUser, pk=user_id)
        contact_register = ContactUserForm(request.POST, instance=contact_data)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message
                })
        try:
            contact_register.save()
            return redirect('monitor:user_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, user_id):
        contact_data = get_object_or_404(ContactUser, pk=user_id)
        contact_register = ContactUserForm(instance=contact_data)
        return render(
            request,
            self.template_name,
            {
                "contact_register": contact_register,
                "view_message": self.view_message
            })


# 删除报警规则
class ContactUserDelView(View):
    template_name = 'monitor/contact_user.html'
    view_message = "报警规则联系人"

    @method_decorator(login_required)
    def post(self, request, user_id):
        try:
            ContactUser.objects.get(pk=user_id).delete()
            return redirect('monitor:user_list')
        except Exception as error:
            contact_data = ContactUser.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, user_id):
        try:
            ContactUser.objects.get(pk=user_id).delete()
            return redirect('monitor:user_list')
        except Exception as error:
            contact_data = ContactUser.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++报警联系人组配置++++++++++++++++++++++++++++++++++++++++++++++++
class ContactGroupAddView(View):
    template_name = 'monitor/contact_group_edit.html'
    view_message = "添加报警联系人组"

    @method_decorator(login_required)
    def get(self, request):
        contact_register = ContactGroupForm()
        return render(
            request,
            self.template_name,
            {
                'contact_register': contact_register,
                'view_message': self.view_message
            }
        )

    @method_decorator(login_required)
    def post(self, request):
        contact_register = ContactGroupForm(request.POST)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    'view_message': self.view_message
                }
            )
        try:
            contact_register.save()
            return redirect('monitor:group_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    'contact_register': contact_register,
                    "error": error,
                    'view_message': self.view_message
                }
            )


# 报警联系人组列表
class ContactGroupListView(View):
    template_name = "monitor/contact_group.html"
    view_message = "报警联系人组联系人组"

    @method_decorator(login_required)
    def post(self, request):
        contact_data = ContactGroup.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })

    @method_decorator(login_required)
    def get(self, request):
        contact_data = ContactGroup.objects.order_by('create_time')
        return render(
            request,
            self.template_name,
            {
                "contact_data": contact_data,
                "view_message": self.view_message
            })


# 编辑报警联系人组
class ContactGroupEditView(View):
    template_name = 'monitor/contact_group_edit.html'
    view_message = "修改报警联系人组"

    @method_decorator(login_required)
    def post(self, request, group_id):
        contact_data = get_object_or_404(ContactGroup, pk=group_id)
        contact_register = ContactGroupForm(request.POST, instance=contact_data)
        if not contact_register.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message
                })
        try:
            contact_register.save()
            return redirect('monitor:group_list')
        except Exception as error:
            return render(
                request,
                self.template_name,
                {
                    "contact_register": contact_register,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, group_id):
        contact_data = get_object_or_404(ContactGroup, pk=group_id)
        contact_register = ContactGroupForm(instance=contact_data)
        return render(
            request,
            self.template_name,
            {
                "contact_register": contact_register,
                "view_message": self.view_message
            })


# 删除报警联系人组
class ContactGroupDelView(View):
    template_name = 'monitor/contact_group.html'
    view_message = "报警联系人组联系人组"

    @method_decorator(login_required)
    def post(self, request, group_id):
        try:
            ContactGroup.objects.get(pk=group_id).delete()
            return redirect('monitor:group_list')
        except Exception as error:
            contact_data = ContactGroup.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })

    @method_decorator(login_required)
    def get(self, request, group_id):
        try:
            ContactGroup.objects.get(pk=group_id).delete()
            return redirect('monitor:group_list')
        except Exception as error:
            contact_data = ContactGroup.objects.order_by('id')
            return render(
                request,
                self.template_name,
                {
                    "contact_data": contact_data,
                    "view_message": self.view_message,
                    "error": error
                })
