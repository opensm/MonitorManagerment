# Generated by Django 2.2 on 2019-04-27 03:04

from django.db import migrations


def forwards_func(apps, schema_editor):
    """
    :param apps:
    :param schema_editor:
    :return:
    """
    role = apps.get_model("rbac", "Role")
    permission = apps.get_model("rbac", "Permission")
    var_g1 = permission.objects.get(id=1)
    var_g2 = permission.objects.get(id=2)
    var_g3 = permission.objects.get(id=3)
    var_g4 = permission.objects.get(id=4)
    var_g5 = permission.objects.get(id=5)
    var_g6 = permission.objects.get(id=6)
    var_g7 = permission.objects.get(id=7)
    var_g8 = permission.objects.get(id=8)
    var_g9 = permission.objects.get(id=9)
    var_g10 = permission.objects.get(id=10)
    var_g11 = permission.objects.get(id=11)
    var_g12 = permission.objects.get(id=12)
    var_g13 = permission.objects.get(id=13)
    var_g14 = permission.objects.get(id=14)
    var_g15 = permission.objects.get(id=15)
    var_g16 = permission.objects.get(id=16)
    var_g17 = permission.objects.get(id=17)
    var_g18 = permission.objects.get(id=18)
    var_g19 = permission.objects.get(id=19)
    var_g20 = permission.objects.get(id=20)
    var_g21 = permission.objects.get(id=21)
    role_1 = role.objects.create(
        id=1, title="用户管理"
    )
    role_1.permission.add(var_g1, var_g2, var_g3, var_g4)
    role_2 = role.objects.create(
        id=2, title="菜单管理"
    )
    role_2.permission.add(var_g5, var_g6, var_g7, var_g8)
    role_3 = role.objects.create(
        id=3, title="权限组管理"
    )
    role_3.permission.add(var_g9, var_g10, var_g11, var_g12)
    role_4 = role.objects.create(
        id=4, title="权限管理"
    )
    role_4.permission.add(var_g13, var_g14, var_g15, var_g16)
    role_5 = role.objects.create(
        id=5, title="角色管理"
    )
    role_5.permission.add(var_g17, var_g18, var_g19, var_g20)
    role_6 = role.objects.create(
        id=6, title="自带权限"
    )
    role_6.permission.add(var_g21)


def reverse_func(apps, schema_editor):
    role = apps.get_model("rbac", "role")
    db_alias = schema_editor.connection.alias
    role.objects.using(db_alias).filter(permission=1, id=1).delete()
    role.objects.using(db_alias).filter(permission=2, id=1).delete()
    role.objects.using(db_alias).filter(permission=3, id=1).delete()
    role.objects.using(db_alias).filter(permission=4, id=1).delete()
    role.objects.using(db_alias).filter(permission=5, id=2).delete()
    role.objects.using(db_alias).filter(permission=6, id=2).delete()
    role.objects.using(db_alias).filter(permission=7, id=2).delete()
    role.objects.using(db_alias).filter(permission=8, id=2).delete()
    role.objects.using(db_alias).filter(permission=9, id=3).delete()
    role.objects.using(db_alias).filter(permission=10, id=3).delete()
    role.objects.using(db_alias).filter(permission=11, id=3).delete()
    role.objects.using(db_alias).filter(permission=12, id=3).delete()
    role.objects.using(db_alias).filter(permission=13, id=4).delete()
    role.objects.using(db_alias).filter(permission=14, id=4).delete()
    role.objects.using(db_alias).filter(permission=15, id=4).delete()
    role.objects.using(db_alias).filter(permission=16, id=4).delete()
    role.objects.using(db_alias).filter(permission=17, id=5).delete()
    role.objects.using(db_alias).filter(permission=18, id=5).delete()
    role.objects.using(db_alias).filter(permission=19, id=5).delete()
    role.objects.using(db_alias).filter(permission=20, id=5).delete()
    role.objects.using(db_alias).filter(permission=21, id=6).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('rbac', '0001_initial'),
        ('rbac', '0002_auto_20190520_0000'),
        ('rbac', '0003_auto_20190520_0001'),
        ('rbac', '0004_auto_20190520_0001'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
