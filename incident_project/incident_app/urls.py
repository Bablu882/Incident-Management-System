from django.urls import path 
from .views import *

urlpatterns=[
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('incident/post-get-put/',CreateIncidentAPI.as_view(),name='incident'),
    path('incident-search/',SearchIncidentAPI.as_view(),name='incident-name')
    
]