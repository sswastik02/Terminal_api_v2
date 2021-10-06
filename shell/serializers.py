from rest_framework import serializers
from shell.models import Shell

class ShellSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shell
        fields = ("id","name","response")