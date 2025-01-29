# urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('upgrade_user_to_admin/<str:email>/', views.upgrade_user_to_admin, name='upgrade_user_to_admin'),  # Email in URL
]

