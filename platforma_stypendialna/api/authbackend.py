from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Student   


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            student = Student.objects.get(nazwa_uzytkownika=username)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None