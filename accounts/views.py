from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializer import SignupSerializer


@api_view(
    [
        "POST",
    ]
)
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
