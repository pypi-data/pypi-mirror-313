from django.urls import path
from umkt_service_utils.views import *

urlpatterns = [
    path('group', group_list),
    path('group/<str:name>', group_detil),

    path('user', user_group_list),
    path('user/<str:username>', user_group_detil),
]
