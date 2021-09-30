from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import OwnProfilePermission
from .serializers import SignupSerializer, UserSerializer


@decorators.api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors)


@decorators.api_view(["GET", "POST"])
def logout(request):
    try:
        r_tkn = request.data["refresh_token"]
        token = RefreshToken(r_tkn)
        token.blacklist()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_object(self, queryset=None):
    #     return self.request.user
