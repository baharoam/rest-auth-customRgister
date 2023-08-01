from rest_framework import serializers

from .models import CustomUser, Teacher, Student, Course, Request
from allauth.account.forms import SignupForm
from allauth.account import app_settings as allauth_account_settings
from allauth.utils import email_address_exists, get_username_max_length
from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.utils import setup_user_email
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomSerializer(RegisterSerializer):
    
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED,
    )
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    ROLE_CHOICES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
         )

    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='Student')

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'role': self.validated_data.get('role', ''),
        }
    
    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.role = self.cleaned_data.get('role', 'Student')
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.save()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        print(user.role)
        if user.role == 'Teacher':
                Teacher.objects.create(user=user)
                print("object T created")
        elif user.role == 'Student':
                Student.objects.create(user=user)
                print("object S created")
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        print("token", token.key)
        return user



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('subject','user', 'course_type' ,'capacity', 'start_date')


class RegisterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        #fields = ('subject','user', 'course_type' ,'capacity', 'start_date')

class AttendCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id',)

class AcceptRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id',)