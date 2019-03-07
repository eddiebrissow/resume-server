from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/$', views.ResumeList.as_view(), name='resume-list'),
    path('api/v1/resumes/<str:user>/<str:name>', views.ResumeDownload.as_view(), name='resume-download'),
    path('api/v1/resumes/<int:pk>/', views.ResumeDetail.as_view(), name='resume-update'),
    path('api/v1/users/', views.UserList.as_view(), name='resume-update'),

]