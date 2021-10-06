from django.urls import path
from shell.views import *
urlpatterns = [
    path("",ListShellAPIView.as_view(),name="List_Commands"),
    path("create/",CreateShellAPIView.as_view(),name="Create_Command"),
    path("update/<int:pk>/",UpdateShellAPIView.as_view(),name="Update_Command"),
    path("delete/<int:pk>/",DestroyShellAPIView.as_view(), name="Destroy_Commands"),
]
# an auto id is generated for each entry so pk here is that id
