from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import User
from companies.models import Enterprise, Employee


class Authentication:
    def signin(self, email=None, password=None) -> User:
        exception_auth = AuthenticationFailed("Email ou Senha incorreto(s)")

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exception_auth
        if not check_password(password, user.password):
            raise exception_auth

        return user

    def signup(
        self, name, email, password, type_account="owner", company_id=False
    ) -> User:
        if not name or name == "":
            raise APIException("O nome não deve ser null")

        if not email or email == "":
            raise APIException("O e-mail não deve ser null")

        if not password or password == "":
            raise APIException("O password não deve ser null")

        if type_account == "employee" and not company_id:
            raise APIException("O id da empresa não deve ser null")

        if User.objects.filter(email=email).exists():
            raise APIException("Este e-mail já existe na plataforma")

        password_hashed = make_password(password)
        createed_user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == "employee" else 1,
        )

        if type_account == "owner":
            Enterprise.objects.create(name="Nome da empresa", user_id=createed_user.pk)

        if type_account == "employee":
            Employee.objects.create(
                enterprise_id=company_id,
                user_id=createed_user.pk,
            )

        return createed_user
