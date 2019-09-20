from django.urls import path
from monitor import views

app_name = 'monitor'
urlpatterns = [
    # 监控信息管理
    path('permit/list.html', views.MonitorListView.as_view(), name='information_list'),
    path('permit/add.html', views.MonitorAddView.as_view(), name="information_add"),
    path('permit/del/<int:monitor_id>.html', views.MonitorDelView.as_view(), name="information_del"),
    path('permit/edit/<int:monitor_id>.html', views.MonitorEditView.as_view(), name="information_edit"),
    # 报警消息管理
    path('prometheus/alert.html', views.AlertPrometheusListView.as_view(), name="alert_prometheus"),
    # 发送消息管理
    path('alert/list.html', views.AlertPrometheusListView.as_view(), name="alert_list"),
    # 报警规则
    path('rule/list.html', views.ContactRuleListView.as_view(), name='rule_list'),
    path('rule/add.html', views.ContactRuleAddView.as_view(), name="rule_add"),
    path('rule/del/<int:rule_id>.html', views.ContactRuleDelView.as_view(), name="rule_del"),
    path('rule/edit/<int:rule_id>.html', views.ContactRuleEditView.as_view(), name="rule_edit"),
    # 报警联系人
    path('user/list.html', views.ContactUserListView.as_view(), name='user_list'),
    path('user/add.html', views.ContactUserAddView.as_view(), name="user_add"),
    path('user/del/<int:user_id>.html', views.ContactUserDelView.as_view(), name="user_del"),
    path('user/edit/<int:user_id>.html', views.ContactUserEditView.as_view(), name="user_edit"),
    # 报警联系人组
    path('group/list.html', views.ContactGroupListView.as_view(), name='group_list'),
    path('group/add.html', views.ContactGroupAddView.as_view(), name="group_add"),
    path('group/del/<int:group_id>.html', views.ContactGroupDelView.as_view(), name="group_del"),
    path('group/edit/<int:group_id>.html', views.ContactGroupEditView.as_view(), name="group_edit"),
]
