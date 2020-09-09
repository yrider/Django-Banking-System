from django.contrib.auth.models import BaseUserManager
from django.contrib import auth

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a user with a given email, first_name, last_name ans password.
        """
        if not email:
            raise ValueError("Users must provide an email address")
        if not password:
            raise ValueError("Users must provide a password")
        if not first_name and not last_name:
            raise ValueError("Users must provide their first and last names")
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',  False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, password=None, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')

        return self._create_user(email, first_name, last_name, password, **extra_fields)
    
    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'Multiple backend authoentications have been configured therefore '
                    'you must provide the backend argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                f'backend must be dotted import path string {backend}'
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers = include_superusers,
                obj=obj
            )
        return self.none()
