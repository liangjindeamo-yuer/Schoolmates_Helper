from django.urls import path
from . import views

app_name = 'tasks_square'

urlpatterns = [
    path('', views.task_square, name='task_square'),
    path('sort/<int:type_id>/<slug:order>',views.task_square_sort,name='task_square_sort'),
    path('check_hunt/<int:task_id>/', views.check_hunt, name='check_hunt'),
    path('hunt_task/<int:task_id>/', views.hunt_task, name='hunt_task'),
    path('<int:task_id>/task_detail', views.task_detail, name='task_detail'),
    # swf 2020年4月25日 新增
    path('<int:publisher_id>/publisher_detail/',views.publisher_detail,name='publisher_detail'),
]
