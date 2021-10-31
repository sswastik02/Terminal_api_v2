from django.urls import path,include
from shell.views import *
urlpatterns = [
    path("",ListShellAPIView.as_view(),name="List_Post_Commands"),
    path("<int:pk>/",DetailShellAPIView.as_view(),name="Update_Command"),
    path('rest-auth/',include('rest_auth.urls')),
    path('rest-auth/registration/',include('rest_auth.registration.urls'))
]
# an auto id is generated for each entry so pk here is that id
