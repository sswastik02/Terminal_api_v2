from rest_framework import serializers
from shell.models import Shell
import subprocess
import os

class ShellSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shell
        fields = ("id","user","command","response","cwd")

    def formatdotdot(seld,dir):
        while("/./" in dir):
            dir=dir.replace("/./","/")
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
        dir=dir.replace("/.","")
        if(dir == ''):
            dir = '/'
        return dir

    def argformat(self,command):
        command = command.split(' ')
        dirs = []
        args = []
        for i in command:
            if "-" in i and i.index('-') == 0:
                args.append(i)
            else:
                dirs.append(i)
            
        return dirs,args
    # def mvchecks(self,obj):
    #     obj.response = ""
    #     obj.command = obj.command[3:]
    #     dirs,args = self.argformat(obj.command)
    #     if(len(dirs) <= 1):
    #         obj.response = "mv: missing file operands " 
    #         obj.save()
    #         return obj
    #     for dir in dirs:
    #         while(dir[-1] == "/"):
    #             dir = dir[:-1]
    #         if(dir[0]!='/'):
    #             dir = obj.cwd + "/" + dir
    #         dir = self.formatdotdot(dir)
    #         if("/"+obj.user not in dir or ("/" + obj.user in dir and dir.index("/"+obj.user) != 0)):
    #             obj.response = "Permission Denied"
    #             obj.save()
    #             return obj
    #         if(not os.path.isdir("UserShells"+ dir) and not os.path.isfile("UserShells"+ dir)):
    #             obj.response = dir + " :No such directory or file"
    #             obj.save()
    #             return obj
    #     obj.command = "mv "+ args.join(" ") + " " + dirs.join(' ')
    #     process = subprocess.run(obj.command,shell=True,text=True,capture_output=True,cwd="UserShells"+obj.cwd)
    #     obj.response = process.stdout if process.stderr == '' else process.stderr
    #     obj.response = obj.response.replace(os.getcwd() + "/UserShells","")
    #     obj.save() # this step is necessary to save the obj or during get it will not store correctly
    #     return obj
        
        
        
            
        
    def cdchecks(self,obj):
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

        if("cd" in obj.command and obj.command.index("cd ") == 0):
            return self.cdchecks(obj)
        if("mv" in obj.command and obj.command.index("mv ") == 0):
            return self.mvchecks(obj)
        process = subprocess.run(obj.command,shell=True,text=True,capture_output=True,cwd="UserShells"+obj.cwd)
        obj.response = process.stdout if process.stderr == '' else process.stderr
        obj.response = obj.response.replace(os.getcwd() + "/UserShells","")
        obj.save() # this step is necessary to save the obj or during get it will not store correctly
        return obj