
from django.contrib import admin
from django.urls import path,include
from dj_rest_auth import views
from usres import views as v


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('dj_rest_auth.registration.urls')),
    path('create-course/', v.create_course_mixin_view, name='create-course'),
    path('view-course/', v.view_course_mixin_view, name='view-course'),
    path('attend-course/<int:pk>/', v.attend_course_view, name='attend-course'),
    path('view-request/', v.view_request, name='view-request'),
    path('accept-request/<int:pk>', v.accept_course_view, name='accept-request'),
    
]
