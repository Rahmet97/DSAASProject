from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from auser.models import UserRole, InviteUserEmail

UserModel = get_user_model()


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'type']


class InviteUserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteUserEmail
        fields = ['email']


class RegisterCustomSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "email", "phone_number", "type", "password1", "password2"]

    def validate_email(self, email):
        if UserModel.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _('A user is already registered with this e-mail address.'), )
        return email

    # def validate_password1(self, password):
    #     return get_adapter().clean_password(password)

    def validate(self, data):
        if UserModel.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError(
                _('A user is already registered with this phone number.'), )

        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'type': self.validated_data.get('type', ''),
        }

    def save(self, **kwargs):
        cleaned_data = self.get_cleaned_data()
        password1 = cleaned_data.pop("password1")
        user = UserModel(**cleaned_data)
        if "password1" not in cleaned_data:
            try:
                user.set_password(raw_password=password1)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


# User Details Serializer
class UserCustomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        extra_fields = []

        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'phone_number'):
            extra_fields.append('phone_number')
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'type'):
            extra_fields.append('type')

        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)
