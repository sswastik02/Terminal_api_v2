from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from shell.serializers import ShellSerializer
from shell.models import Shell

# Create your views here.

class ListShellAPIView(ListAPIView):
    "To list all requests "
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer

class CreateShellAPIView(CreateAPIView):
    "To list all requests "
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
class UpdateShellAPIView(UpdateAPIView):
    "To list all requests "
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
class DestroyShellAPIView(DestroyAPIView):
    "To list all requests "
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
