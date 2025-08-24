from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSer


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSer

    def get(self, request):
        user = request.user
        ser = UserSer(user)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        ser = UserSer(data=request.data, instance=user)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)