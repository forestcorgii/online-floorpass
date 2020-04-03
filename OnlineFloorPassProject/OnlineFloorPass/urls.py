from django.urls import path, include
from . import views

app_name = 'floorpass'
urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),

    path('manager/', views.manager, name='manager'),
    path('manager/<int:ref_id>/', views.manager_edit, name='manager'),

    path('generate_id/', views.generate_floorpass_id, name='generate_id'),

    path('log/', views.log, name='log'),
    path('log_add/', views.log_add, name='log_add'),

    path('verify/<int:ref_id>/', views.verify, name='verify'),

]
