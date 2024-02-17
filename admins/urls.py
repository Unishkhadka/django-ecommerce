from django.urls import path
from .views import *

urlpatterns = [
    path("admin-dashboard/", dashboard, name="dashboard"),
    ]