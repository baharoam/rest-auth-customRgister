
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

    

class CustomUser(AbstractUser):
  ROLE_CHOICES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )

  password1 = models.CharField(_("password1"), max_length=128, default="13802001B#")
  password2 = models.CharField(_("password2"), max_length=128, default="13802001B#")
  role = models.CharField(max_length=10, choices=ROLE_CHOICES,default="Teacher")
  phone_number = models.IntegerField(null=True)
  #profilePic
  def __str__(self) -> str:
     return self.username

  




class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.CharField(max_length=100,null=True)
    def __str__(self) :
     return self.user.username


class Teacher(models.Model):
    TEACHER_DEGREE_CHOICES = (
        ("Bachelor", "Bachelor"),
        ("Master", "Master"),
        ("PHD", "PHD"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    instuitional_email = models.EmailField(unique=True,null=True)
    field_of_study = models.CharField(max_length=100,null=True)
    degree = models.CharField(max_length=9,
                  choices=TEACHER_DEGREE_CHOICES,
                  default="PHD",null=True)
    
    def __str__(self) :
     return self.user.username


class Course(models.Model):
   COURSE_TYPE = (
      ("Public", "Public"),
      ("Private", "Private")
   )
   user = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
   subject = models.CharField(max_length=70,null=True)
   course_type = models.CharField(max_length=10, choices=COURSE_TYPE, default=1)
   start_date = models.DateField()
   capacity = models.IntegerField(null=True)

   def __str__(self) :
     return self.subject


class Request(models.Model):
   ACEEPTANCE_COURSE = (
      ("True", "True"),
      ("False", "False")
   )
   sender_student = models.ForeignKey(Student, on_delete=models.CASCADE)
   reciver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
   r_selected_course = models.OneToOneField(Course, on_delete=models.CASCADE)
   acceptance = models.CharField(max_length=20, choices=ACEEPTANCE_COURSE,null=True)

#Imagine this is my 