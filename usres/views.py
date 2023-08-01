
from rest_framework.views import APIView
from django.http import HttpResponse
from .permissions import IsTeacherPermission, IsStudentPermission
from rest_framework.views import APIView
from rest_framework import mixins,generics
from .models import Course, Request, Student, Teacher, CustomUser
from .serializers import CourseSerializer,AttendCourseSerializer,AcceptRequestSerializer
    


class CreateCourseView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    permission_classes = [IsTeacherPermission] # Custom permission class used
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs): #HTTP -> get
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        model_class = Course
        serializer.is_valid(raise_exception=True)
        courseobj = serializer.save()
        return HttpResponse(courseobj,courseobj.id)
    

create_course_mixin_view = CreateCourseView.as_view()


class ViewCourseView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    # Custom permission class used
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs): #HTTP -> get
        return self.list(request, *args, **kwargs)


view_course_mixin_view = ViewCourseView.as_view()

class SingleCourseView(   
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    permission_classes = [IsStudentPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'
    selected_course = 0
    def get(self, request, *args, **kwargs): #HTTP -> get
        global selected_course
        pk = kwargs.get("pk")
        selected_course = Course.objects.get(id=pk)
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

 
one_course_view = SingleCourseView.as_view()


""""
class AttendCourseView(   
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    permission_classes = [IsStudentPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get

        global selected_course
        pk = kwargs.get("pk")
        selected_course = Course.objects.get(id=pk)
        print(selected_course.course_type,selected_course.capacity)

        if selected_course.course_type == 'Public':
            selected_course.capacity = selected_course.capacity - 1
            selected_course.save(update_fields=["capacity"]) 
            print(selected_course.capacity, "after reduction")
            return HttpResponse("Public class was attended, capacity is,", selected_course.capacity)
        
        elif selected_course.course_type =='Private' :
            print("This is Private class for now", request.user)
            selected_student = Student.objects.get(user=request.user)

            Request.objects.create(sender_student = selected_student, reciver_teacher=selected_course.user , r_selected_course = selected_course)

            req = Request.objects.get(sender_student = selected_student, r_selected_course = selected_course)

            if req :
                return HttpResponse("request is already created")
            
            else :
                print("request has not been created")
                Request.objects.create(sender_student = selected_student, reciver_teacher=selected_course.user , r_selected_course = selected_course)
                return HttpResponse("Created request object")

            return HttpResponse("request")

 
"""  

class AttendCourseView(   
    APIView
    ):

    permission_classes = [IsStudentPermission]

    def post(self, request, *args, **kwargs): #HTTP -> get
        serializer = AttendCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = request.data.get('id')
        selected_course = Course.objects.get(id=course_id)
        print(selected_course.course_type,selected_course.capacity)

        if selected_course.course_type == 'Public':
            selected_course.capacity = selected_course.capacity - 1
            selected_course.save(update_fields=["capacity"]) 
            print(selected_course.capacity, "after reduction")
            return HttpResponse("Public class was attended, capacity is,", selected_course.capacity)
        
        elif selected_course.course_type =='Private' :
            print("This is Private class for now", request.user)
            selected_student = Student.objects.get(user=request.user)

            Request.objects.create(sender_student = selected_student, reciver_teacher=selected_course.user , r_selected_course = selected_course)
        
            req = Request.objects.get(sender_student = selected_student, r_selected_course = selected_course)

            if req :
                return HttpResponse("request is already created")
            
            else :
                print("request has not been created")
                Request.objects.create(sender_student = selected_student, reciver_teacher=selected_course.user , r_selected_course = selected_course)
                return HttpResponse("Created request object")

        


attend_course_view = AttendCourseView.as_view()


class ViewRequest(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    permission_classes = [IsTeacherPermission] # Custom permission class used
    queryset = Request.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs): #HTTP -> get
        user_name = CustomUser.objects.get(username= request.user.username)
        user_name_id = user_name.id

        sender_students = Request.objects.values_list('sender_student', flat=True).distinct()
        requests_with_related = Request.objects.filter(sender_student__in=sender_students,reciver_teacher = user_name_id).prefetch_related('reciver_teacher', 'r_selected_course')

        
        for request in requests_with_related:
            print("Student is", request.sender_student)
            print("Teacher is", request.reciver_teacher)
            print("Course is", request.r_selected_course)
            print("Request Number  is", request.id)
            print('**********************************')

        return HttpResponse("View Request")


view_request = ViewRequest.as_view()



#delete course class

class AcceptCourseView(   
    APIView
    ):

    def post(self, request, *args, **kwargs): #HTTP -> get

        serializer = AcceptRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_id = request.data.get('id')
        selected_request = Request.objects.get(id=request_id)       
        selected_course = Course.objects.get(subject = selected_request.r_selected_course)
    
        selected_course.capacity = selected_course.capacity - 1
        selected_course.save(update_fields=["capacity"]) 
        print(selected_course.capacity, "after reduction")

        return HttpResponse("Accepted the View")

 
accept_course_view = AcceptCourseView.as_view()


 
