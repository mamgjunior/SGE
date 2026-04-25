from rest_framework.response import Response

from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from accounts.views.base import Base


class Signup(Base):
    def post(self, request) -> Response:
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        auth = Authentication()
        user = auth.signup(name=name, email=email, password=password)

        serializer = UserSerializer(user)
        return Response({"user": serializer.data})
