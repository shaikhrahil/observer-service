from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsOwnerStrict
from .serializers import ChangePasswordSerializer, SignupSerializer, UserSerializer


@decorators.api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated, IsOwnerStrict])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(request.user)
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["GET", "POST"])
@decorators.permission_classes([permissions.IsAuthenticated, IsOwnerStrict])
def logout(request):
    try:
        r_tkn = request.data["refresh_token"]
        token = RefreshToken(r_tkn)
        token.blacklist()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerStrict]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_object(self, queryset=None):
    #     return self.request.user
