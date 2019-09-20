import re
from django.template import Library
from django.conf import settings
import time

register = Library()

"""
{% menu request %}
"""


@register.inclusion_tag('menu.html')
def menu(request):
    current_url = request.path
    # 获取session中菜单信息，自动生成二级菜单【默认选中，默认展开】
    permission_menu_list = request.session.get(settings.PERMISSION_MENU_SESSION_KEY)
    per_dict = {item['id']: item for item in permission_menu_list if item['pid'] is None}
    # print(per_dict)
    # 以下是白名单URL的处理
    for item in permission_menu_list:
        reg = settings.REX_FORMAT % (item['url'])
        # 判断当前URL是否未白名单URL,是的话直接设定为可用url
        if not re.match(reg, current_url):
            continue
        # 匹配成功
        # item['pid'] 不为None 直接将ID对应的 active 设为真，否则 item 设为假
        if item['pid'] is not None:
            item['active'] = True

    """
    {
        1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True}, 
        5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'}
        10: {'id': 10, 'title': 'xx列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'}
    }

    {
        1:{
            'menu__name': '菜单1',
            'active': True,
            'children':[
                {'id': 1, 'title': '用户列表', 'url': '/users/','active': True}
                {'id': 5, 'title': '主机列表', 'url': '/users/'}
            ]
        },
        2:{
             'menu__name': '菜单1',
              'children':[
                {'id': 10, 'title': 'xx列表', 'url': '/hosts/'}
            ]

        }
    }
    """
    menu_result_tmp = dict()
    menu_result = dict()
    for item in per_dict.values():
        data = {
            'menu__id': item['menu_id'],
            'menu__name': item['menu__name'],
            'active': item.get('active', False)
        }
        if item['menu__types'] not in menu_result_tmp.keys():
            menu_result_tmp.setdefault(item['menu__types'], []).append(data)
            continue
        if data in menu_result_tmp[item['menu__types']]:
            continue
        menu_result_tmp.setdefault(item['menu__types'], []).append(data)
    for key, value in menu_result_tmp.items():
        for v in value:
            data_list = [{
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'active': item.get('active', False)
            } for item in per_dict.values() if item['menu_id'] == v['menu__id']]
            v['children'] = data_list
            menu_result.setdefault(key, []).append(v)

    return {'menu_result': menu_result}


@register.filter
def get_index(x):
    css_list = ['focus', 'primary', 'success', 'warning', 'danger', 'metal', 'brand']
    return css_list[int(x) % 7]
