from rest_framework import serializers
from shell.models import Shell
import subprocess
import os

class ShellSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shell
        fields = ("id","user","command","response","cwd")

    def formatdotdot(self,dir):
        while("/.." in dir):
            dotdot = dir.index('/..')
            if(dotdot == 0):
                dir = '/'
                break
            slashbeforedotdot=-1
            for i in range(dotdot-1,-1,-1):
                if(dir[i] != "/"):
                    continue
                else:
                    slashbeforedotdot=i
                    break
            dir = dir[:slashbeforedotdot] + dir[dotdot + 3:]
            if(dir == ''):
                dir = '/'
                break
        return dir
    def getcwd(self,obj):
        last_cwds = Shell.objects.all().filter(user=obj.user).exclude(id=obj.id)[::-1]
        if(len(last_cwds) > 0):
            return last_cwds[0].cwd
        return "/" + obj.user
            
    def create(self,validated_data):
        obj = Shell.objects.create(**validated_data)


        if(not self.context['request'].user.is_authenticated):
            obj.response = "Invalid User Credentials"
            obj.save()
            return obj

        
        obj.user = self.context['request'].user.username
        if(not os.path.isdir("UserShells")):
            subprocess.run("mkdir UserShells",shell=True)
            

        
        obj.cwd = self.getcwd(obj)
        if(not os.path.isdir("UserShells/"+obj.user)):
            subprocess.run("mkdir UserShells/"+obj.user,shell=True)
        
        obj.command = obj.command.strip()
        if(obj.command == "whoami"):
            obj.response = obj.user
            obj.save()
            return obj

        if("cd" in obj.command and obj.command.index("cd") == 0):
            obj.response = ""
            dir = obj.command[3:]
            while(dir[-1] == "/"):
                dir = dir[:-1]
            if(".." in dir and dir.index("..") == 0 and obj.cwd == "/" + obj.user):
                obj.response = "Do not use .."
                obj.save()
                return obj
            
            if(dir[0] != '/'):
                dir = obj.cwd + "/" + dir
            
            dir = self.formatdotdot(dir)
            if("/"+obj.user not in dir or ("/" + obj.user in dir and dir.index("/"+obj.user) != 0)):
                obj.response = "Permission Denied"
                obj.save()
                return obj
            
            if(not os.path.isdir("UserShells"+ dir)):
                obj.response = dir + " :No such directory"
                obj.save()
                return obj
            
            obj.cwd=dir
            obj.save()
            return obj

        
        if(len(Shell.objects.all().filter(user=obj.user).exclude(id=obj.id)[::-1]) > 0):
            print(Shell.objects.all().filter(user=obj.user).exclude(id=obj.id)[::-1][0].cwd)
        
        process = subprocess.run(obj.command,shell=True,text=True,capture_output=True,cwd="UserShells"+obj.cwd)
        obj.response = process.stdout if process.stderr == '' else process.stderr
        obj.response = obj.response.replace(os.getcwd() + "/UserShells","")
        obj.save() # this step is necessary to save the obj or during get it will not store correctly
        return obj