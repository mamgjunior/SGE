from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from companies.models import Enterprise, Employee
from accounts.models import User_Groups, Group_Permissions


class Base(APIView):
    def get_enterprise_user(self, user_id):
        enterprise = {"is_owner": False, "permissions": []}

        enterprise["is_owner"] = Enterprise.objects.filter(user_id=user_id).exists()
        if enterprise["is_owner"]:
            return enterprise

        employee = Employee.objects.filter(user_id=user_id).first()
        if not employee:
            raise APIException("Este usuário não é um funcionário")

        groups = User_Groups.objects.filter(user_id=user_id).all()
        for group in groups:
            permissions = Group_Permissions.objects.filter(group_id=group.pk).all()
            for permission in permissions:
                enterprise["permissions"].append(
                    {
                        "id": permission.permission.pk,
                        "label": permission.permission.name,
                        "codename": permission.permission.codename,
                    }
                )

        return enterprise
