from django.db import models

class Photos(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(default='',max_length=100,null=True)
    # models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origin_photo = models.ImageField(upload_to="origin",null=True)
    converted_photo = models.ImageField(upload_to="converted",null=True)
    background_color = models.CharField(default='#ffffff',max_length=10,null=True)
    background_photo = models.ImageField(upload_to="background",null=True)

class CameraImage(models.Model):
    image = models.ImageField(upload_to="origin_blob")
    timestamp = models.DateTimeField(auto_now_add=True)