from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializer import SignupSerializer, UserSerializer


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET", "POST"])
def logout(request):
    try:
        r_tkn = request.data["refresh_token"]
        token = RefreshToken(r_tkn)
        token.blacklist()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = UserSerializer(request.user)
    return Response(user.data)


class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUser(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
