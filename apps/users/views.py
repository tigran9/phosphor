from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserRegistrationSerializer, UserSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user_last_name': user.last_name,
            'user_first_name': user.first_name,
            'email': user.email
        })


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save_user(request.data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():

            path = "http://127.0.0.1:8000/"
            send_mail(
                'Subject here',
                'Follow link to reset your password {0}{1}'.format(path, request.data.password_reset_key),
                'tigran94.stdev@gmail.com',
                [self.request.data['email']],
                fail_silently=False,
            )
            return Response(ForgotPasswordSerializer(user).data, status=status.HTTP_201_CREATED)


class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def get_serializer(self):
        return self.serializer_class()
