from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import status, permissions, response, views
from rest_framework.generics import ListCreateAPIView,CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt import exceptions, authentication, tokens

from auser.serializers import (
    RegisterCustomSerializer, InviteUserEmailSerializer, UserCustomDetailsSerializer,
    LoginSerializer, OnlineUsersSerializer, DashboardPartSerializer
)
from auser.models import Worker, InviteUserEmail, RecommendUserEmail, UserRole
from auser.u_permissions import InviteUserEmailPermission
from auser.u_utils import check_token
from task_app.models import Task

User = get_user_model()


# Invite User Email View
class InviteUserEmailView(ListCreateAPIView):
    serializer_class = InviteUserEmailSerializer
    permission_classes = [InviteUserEmailPermission]
    authentication_classes = [authentication.JWTAuthentication]

    def perform_create(self, serializer):
        req_user = self.request.user
        if Worker.objects.filter(employee=req_user).exists():  # request user is employee
            boss = req_user.employee_related.get().whose_employee
        else:  # request user is boss
            boss = req_user
        serializer.save(whose_employee_worker=boss)

    def get(self, request, *args, **kwargs):
        queryset = InviteUserEmail.objects.filter(is_active=False)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

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
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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

@method_decorator(csrf_exempt, name='dispatch')
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


# Get Online Users View
class GetOnlineUsersView(views.APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="online users count and lists")
    def get(self, request):
        online_users_count = 0
        order_by = request.query_params.get('order', None)
        print(order_by)

        if Worker.objects.filter(employee=request.user).exists():  # request user is employee
            boss = request.user.employee_related.get().whose_employee
        else:  # request user is boss
            boss = request.user

        if boss.is_online:
            online_users_count += 1

        # obj = Worker.objects.filter(whose_employee=boss)
        obj = User.objects.filter(employee_related__whose_employee=boss)

        if order_by:
            obj = obj.order_by(order_by)

        for x in obj:
            # if x.employee.is_online:
            if x.is_online:
                online_users_count += 1

        if obj:
            # serializers = GetOnlineUsersSerializer(obj, many=True)
            serializers = OnlineUsersSerializer(obj, many=True)
            data = {
                "online_users": serializers.data,
                "online_users_count": online_users_count
            }
            return response.Response(data=data, status=status.HTTP_200_OK)
        return response.Response(data={"message": "HTTP 204 NO CONTENT"}, status=status.HTTP_204_NO_CONTENT)


class DashboardPartTwoView(GenericAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DashboardPartSerializer

    def get(self, request):

        if Worker.objects.filter(employee=request.user).exists():  # request user is employee
            boss = request.user.employee_related.get().whose_employee
        else:  # request user is boss
            boss = request.user

        users = User.objects.filter(employee_related__whose_employee=boss)
        tasks = Task.objects.filter(created_from__employee_related__whose_employee=boss)

        roles = [i.type for i in UserRole.objects.all()]
        context = {i: 0 for i in roles}
        for user in users:
            if user.type.type in roles:
                context[user.type.type] += 1
        serializers = self.get_serializer(tasks, many=True)
        data = {
            "employee_roles": context,
            "employee_total": users.count(),
            "project_tracked": {
                "projects_total": tasks.count(),
                "project_tracked": serializers.data,
            }
        }
        return response.Response(data, status=200)
