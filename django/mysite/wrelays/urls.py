
from django.urls import path

from . import views


app_name = 'wrelays'    #namespace for template urls

urlpatterns = [
    path('', views.index, name='index'),
    path('relays', views.index, name='index2'),
    path('<int:relay_id>/', views.detail, name='detail'),
    path('<int:relay_id>/on', views.on, name='on'),
    path('<int:relay_id>/off', views.off, name='off'),
    path('<int:relay_id>/toggle', views.toggle, name='toggle'),
    path('schedule', views.schedule, name='schedule'),
]