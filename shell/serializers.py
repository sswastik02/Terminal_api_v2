from rest_framework import serializers
from shell.models import Shell
import subprocess

class ShellSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shell
        fields = ("id","command","response")
    def create(self,validated_data):
        obj = Shell.objects.create(**validated_data)
        process = subprocess.run(obj.command,shell=True,text=True,capture_output=True)
        obj.response = process.stdout if process.stderr == '' else process.stderr
        obj.save() # this step is necessary to save the obj or during get it will not store correctly
        return obj