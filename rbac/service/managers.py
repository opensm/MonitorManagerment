from django.contrib.auth.base_user import BaseUserManager


# from ..models import Department


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        if not username:
            raise ValueError('The email is required!')
        email = self.normalize_email(username)
        # department = Department.objects.get(id=extra_fields['department'])
        user = self.model(username=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)

    def __str__(self):
        """
        :return:
        """
        return self.username
