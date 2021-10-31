from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from shell.serializers import ShellSerializer
from shell.models import Shell

# Create your views here.

class ListShellAPIView(ListCreateAPIView):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
    def list(self,request,*args,**kwargs):
        queryset = Shell.objects.filter(user=self.request.user) if request.user.is_authenticated else Shell.objects.none()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

class DetailShellAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer
