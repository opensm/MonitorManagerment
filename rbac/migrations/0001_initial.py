# Generated by Django 2.2 on 2019-07-09 11:45

from django.db import migrations, models
import rbac.service.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='菜单名称')),
                ('types', models.CharField(choices=[('system', '系统菜单'), ('current', '当前用户'), ('general', '一般菜单')], default='select', max_length=50, verbose_name='菜单种类')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='权限名称')),
                ('code', models.CharField(choices=[('delete', '删除'), ('insert', '添加'), ('select', '查看'), ('update', '修改')], default='select', max_length=50, verbose_name='读写情况')),
                ('url', models.CharField(max_length=255, verbose_name='含正则的URL')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色名称')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('permission', models.ManyToManyField(to='rbac.Permission', verbose_name='拥有权限')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('menu', models.ForeignKey(on_delete=False, to='rbac.Menu', verbose_name='所属菜单')),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='group',
            field=models.ForeignKey(on_delete=False, to='rbac.PermissionGroup', verbose_name='所属权限组'),
        ),
        migrations.AddField(
            model_name='permission',
            name='group_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=False, related_name='权限', to='rbac.Permission', verbose_name='组内菜单'),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.EmailField(default='', max_length=50, unique=True, verbose_name='邮件')),
                ('first_name', models.CharField(blank=True, default='', max_length=50, verbose_name='姓')),
                ('last_name', models.CharField(default='', max_length=50, verbose_name='名')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('img', models.ImageField(default='/avatar/100_1.jpg', upload_to='static/img/users/', verbose_name='头像')),
                ('is_active', models.BooleanField(default=True, verbose_name='有效')),
                ('is_staff', models.BooleanField(default=True, verbose_name='员工')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('department', models.ForeignKey(blank=True, on_delete=False, to='rbac.Department', verbose_name='部门')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='具有的所有角色')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'User',
            },
            managers=[
                ('object', rbac.service.managers.UserManager()),
            ],
        ),
    ]
