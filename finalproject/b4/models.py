from django.db import models

class Photos(models.Model):
    id = models.AutoField(primary_key=True)
    # models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origin_photo = models.ImageField(upload_to="origin",null=True)
    converte_photo = models.ImageField(upload_to="converte")
    background_color = models.CharField(default='',max_length=10)
    background_photo = models.ImageField(upload_to="background")

class CameraImage(models.Model):
    image = models.ImageField(upload_to="origin")
    timestamp = models.DateTimeField(auto_now_add=True)