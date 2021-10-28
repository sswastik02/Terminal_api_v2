from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from shell.serializers import ShellSerializer
from shell.models import Shell

# Create your views here.

class ListShellAPIView(ListCreateAPIView):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer

class DetailShellAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
