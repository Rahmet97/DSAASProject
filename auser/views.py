from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, response, views
from rest_framework.generics import CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt import exceptions, authentication, tokens

from auser.serializers import (
    RegisterCustomSerializer, InviteUserEmailSerializer, UserCustomDetailsSerializer,
    LoginSerializer
)
from auser.models import Worker, InviteUserEmail, RecommendUserEmail
from auser.u_permissions import InviteUserEmailPermission
from auser.u_utils import check_token

User = get_user_model()


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
            return response.Response({"message": "Invitation link is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"message": "you are successfully registered"},
                                 status=status.HTTP_201_CREATED, headers=headers)

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
class UserFirstLoginView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user.is_first_login:
            user = get_object_or_404(User, id=request.user.id)
            user.is_first_login = False
            user.save()
            return response.Response(data={"message": "successfully changed"}, status=status.HTTP_200_OK)
        return response.Response(data={"message": "unsuccessfully changed"}, status=status.HTTP_400_BAD_REQUEST)


class TestView(TemplateView):
    template_name = 'user/invite_email_reg.html'


# @api_view(['post'])
# @authentication_classes([])
# @permission_classes([])
# def login(request):
#     try:
#         email = request.data.get('email')
#         password = request.data.get('password')
#         us = User.objects.get(email=email)
#         if check_password(password, us.password):
#             token = RefreshToken.for_user(us)
#             tk = {
#                 "refresh": str(token),
#                 "access": str(token.access_token)
#             }
#             data = {
#                 "success": True,
#                 "token": tk
#             }
#         else:
#             data = {
#                 "success": False,
#                 "message": "Email yoki parol xato!!!"
#             }
#             return Response(data, status=405)
#     except Exception as e:
#         data = {
#             "success": False,
#             "message": f"{e}"
#         }
#         return Response(data, status=405)
#     return Response(data, status=200)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny, ]

    # parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Login tizimga kirish")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password!')

        token = tokens.RefreshToken.for_user(user)
        tk = {
            "access": str(token.access_token),
            "refresh": str(token),
        }
        return response.Response(data=tk, status=status.HTTP_200_OK)


class UserView(GenericAPIView):
    serializer_class = UserCustomDetailsSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Foydalanuvchi haqidagi malumotlar")
    def get(self, request):
        user = get_object_or_404(User, email=request.user.email, pk=request.user.pk)
        serializer = self.get_serializer(user)
        return response.Response(data=serializer.data)

    @swagger_auto_schema(operation_summary="Foydalanuvchi ma`lumotlarini yangilash")
    def put(self, request, *args, **kwargs):
        """
        Foydalanuvchi ma`lumotlarini yangilash
        """
        user, data = request.user, request.data
        serializer = self.get_serializer(user, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
