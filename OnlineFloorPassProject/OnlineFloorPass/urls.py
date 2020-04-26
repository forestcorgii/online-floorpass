from django.urls import path, include, re_path
from . import views
from . import api

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'floorpass'

urlpatterns = format_suffix_patterns([
    re_path('^filter/$', api.api_root),
    path('', api.api_root),

    # path('', api.FloorPassList.as_view(), name='floorpass-list'),
    path('<int:pk>/', api.FloorPassDetail.as_view(), name='floorpass-detail'),

    path('log/', api.LogList.as_view(), name='log-list'),
    path('log/<int:pk>/', api.LogDetail.as_view(), name='log-detail'),

    path('user/', api.UserList.as_view(), name='user-list'),
    path('user/<int:pk>/', api.UserDetail.as_view(), name='user-detail'),
])

# urlpatterns = [
#     path('api/', api.FloorPassList.as_view(), name='floorpass-list'),
#     path('api/detail', api.ReferenceID),
#     path('api/detail/<id>', api.ReferenceID),

#     path('test_form', views.get_name, name='index'),

#     path('', views.index, name='index'),

#     path('login/', views.login, name='login'),

#     path('manager/', views.manager, name='manager'),
#     path('manager/<int:ref_id>/', views.manager_edit, name='manager'),

#     path('generate_id/', views.generate_floorpass_id, name='generate_id'),

#     path('log/', views.log, name='log'),
#     path('log_add/', views.log_add, name='log_add'),

#     path('verify/<int:ref_id>/', views.verify, name='verify'),

# ]
