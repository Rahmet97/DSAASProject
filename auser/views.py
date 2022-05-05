from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from auser.serializers import RegisterCustomSerializer, InviteUserEmailSerializer
from auser.models import Worker, InviteUserEmail, RecommendUserEmail

#---------------------------------------------------------------------------------------

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCustomDetailsSerializer #UsersSerializer, UserSerializer, NewsSerializer

#---------------------------------------------------------------------------------------

User = get_user_model()


class InviteUserEmailPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_company_admin
        )


# Invite User Email View
class InviteUserEmailView(CreateAPIView):
    serializer_class = InviteUserEmailSerializer
    permission_classes = [InviteUserEmailPermission]

    def perform_create(self, serializer):
        req_user = self.request.user
        if Worker.objects.filter(employee=req_user).exists():
            boss = req_user.employee.whose_employee
        else:
            boss = req_user
        serializer.save(whose_employee_worker=boss)


# Auth register view
def check_token(user, token):
    if (user.token is None) or (token is None):
        return False
    if user.token == token:
        return True
    return False


# Register view
class RegisterView(CreateAPIView):
    serializer_class = RegisterCustomSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
            is_invite_by_our_admin = force_str(urlsafe_base64_decode(kwargs['iiboa']))
            if is_invite_by_our_admin == 'True':
                invite_user = RecommendUserEmail.objects.get(pk=uid)
            else:
                invite_user = InviteUserEmail.objects.get(pk=uid)
        except():
            invite_user = None

        if invite_user is not None and check_token(invite_user, kwargs['token']) and invite_user.is_active:
            return self.create(request, *args, **kwargs)

        else:
            return Response({"message": "Invitation link is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "you are successfully registered"}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        employee = serializer.save()

        uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
        is_invite_by_our_admin = force_str(urlsafe_base64_decode(self.kwargs['iiboa']))

        if is_invite_by_our_admin == 'True':
            invite_user = RecommendUserEmail.objects.get(pk=uid)
            invite_user.is_active = False
            invite_user.save()
        else:
            invite_user = InviteUserEmail.objects.get(pk=uid)
            boss_user = invite_user.whose_employee_worker
            Worker.objects.create(whose_employee=boss_user, employee=employee)
            invite_user.is_active = False
            invite_user.save()


# User First Login view
class UserFirstLoginView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user.is_first_login:
            user = get_object_or_404(User, id=request.user.id)
            user.is_first_login = False
            user.save()
            return Response(data={"message": "successfully changed"}, status=status.HTTP_200_OK)
        return Response(data={"message": "unsuccessfully changed"}, status=status.HTTP_400_BAD_REQUEST)


class TestView(TemplateView):
    template_name = 'user/invite_email_reg.html'


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        us = User.objects.get(email=email)
        if check_password(password, us.password):
            token = RefreshToken.for_user(us)
            tk = {
                "refresh": str(token),
                "access": str(token.access_token)
            }
            data = {
                "success": True,
                "token": tk
            }
        else:
            data = {
                "success": False,
                "message": "Email yoki parol xato!!!"
            }
            return Response(data, status=405)
    except Exception as e:
        data = {
            "success": False,
            "message": f"{e}"
        }
        return Response(data, status=405)
    return Response(data, status=200)


@api_view(['get'])
@authentication_classes([JWTAuthentication])
def get_user(request):
    user = UserCustomDetailsSerializer(request.user)
    return Response(user.data)
