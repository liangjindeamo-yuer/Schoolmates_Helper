from django.urls import path
from . import views

app_name = 'tasks_square'

urlpatterns = [
    path('', views.task_square, name='task_square'),
    path('check_hunt/<int:task_id>/', views.check_hunt, name='check_hunt'),
    path('hunt_task/<int:task_id>/', views.hunt_task, name='hunt_task'),
    path('reward_up/', views.reward_up, name='reward_up'),
    path('reward_down/', views.reward_down, name='reward_down'),
    path('<int:task_id>/task_detail', views.task_detail, name='task_detail'),
]
