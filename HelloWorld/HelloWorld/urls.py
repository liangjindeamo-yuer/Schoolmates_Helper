from django.conf.urls import url
from django.contrib import admin
from App import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register',views.register),
    url(r'^acp',views.acp),
    url(r'^finish',views.finish),
    url(r'^un_acp',views.un_acp),
    url(r'^release',views.release),
    url(r'^f_mission/',views.f_mission),
    url(r'^d_mission/',views.d_mission),
    url(r'^comment',views.comment),
    url(r'^reason',views.reason),
    url(r'^d_unacpm/',views.d_unacpm),
    url(r'^m_detail/',views.m_detail),
    url(r'^m_change',views.m_change)

]