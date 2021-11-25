from django.urls import path
from . import views
from .views import TaskList, TaskDetail

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    #path('task-list/', views.tasklist, name='api-tasklist'),
    #path('task-detail/<str:pk>/', views.taskdetail, name='api-taskdetail'),
    #path('task-create/', views.taskcreate, name='api-taskcreate'),
    #path('task-update/<str:pk>/', views.taskupdate, name='api-taskupdate'),
    #path('task-delete/<str:pk>/', views.taskdelete, name='api-taskdelete'),


    

     
     path('task-list/', TaskList.as_view(), name='api-tasklist'),
     path('task-detail/<str:pk>/', TaskDetail.as_view(), name='api-taskdetail'),

     path('users/', views.UserList.as_view()),
     path('users/<int:pk>/', views.UserDetail.as_view()),
     
]  
