from django.contrib.auth.base_user import BaseUserManager
from django.db import IntegrityError


class UserManager(BaseUserManager):
    user_in_migrations = True

    def create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        """
        создание и сохранение пользователя через почту или номер телефона
        """

        if not username:
            if not email and not phone: 
                raise ValueError("The given email/phone must be set")
            
        if email:
            email = self.normalize_email(email)

            if not username:
                username = email
            
            user = self.model(
                email=email,
                username=username,
                **extra_fields
            )

        if phone:
            if not username:
                username = phone
            
            user = self.model(
                username=username,
                phone=phone,
                **extra_fields
            )

        if extra_fields.get("is_superuser"):
            user = self.model(
                username=username,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(
            username=username,
            password=password, 
            **extra_fields
        )

        
