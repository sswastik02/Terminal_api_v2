from django.db import models

# Create your models here.

class Shell(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user=models.TextField(editable=False,default="Anonymous")
    command = models.CharField(max_length=100)
    response = models.TextField(editable=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.command
