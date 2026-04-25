from rest_framework.response import Response

from accounts.serializers import UserSerializer
from accounts.views.base import Base
from rest_framework.permissions import IsAuthenticated


class GerUser(Base):
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        user = request.user
        enterprise = self.get_enterprise_user(user)
        serializer = UserSerializer(user)
        return Response({"user": serializer.data, "enterprise": enterprise})
