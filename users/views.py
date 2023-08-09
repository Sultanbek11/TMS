from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Users, UserProfile
from .serializers import (
    UsersProfileSerializer,
    UserRegisterSerializer,
    VerifySerializer,
    ChangePasswordSerializer,
    LoginSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAdminUser, IsAuthenticatedOrReadOnly)


class Verify_EmailAPIView(generics.RetrieveAPIView):
    serializer_class = VerifySerializer
    queryset = Users.objects.filter(is_active=False)
    lookup_field = 'verify_code'

    def retrieve(self, request, *args, **kwargs):
        instance: Users = self.get_object()
        serializer = self.get_serializer(instance)
        instance.verify_account()
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Users
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
