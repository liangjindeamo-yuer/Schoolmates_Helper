from django.contrib import admin
from .models import Task

# 管理者：admin 密码：untitled20

class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information',   {'fields':['ddltime']}),
    ]
    list_display = ('task_name', 'ddltime')


admin.site.register(Task, TaskAdmin)
# Register your models here.
