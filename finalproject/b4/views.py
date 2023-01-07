from django.shortcuts import render
from django.http import HttpResponse
from .models import Photos

def test(request):
    return render(request,'camera_test.html')
# Create your views here.

def share_page(request, id):

    photo = Photos.objects.all()
    # print(photo.converte_photo)
    photo = Photos.objects.filter(id = id)
    # print(len(photo))
    # photo=1
    # print(photo.converte_photo)
    return render(request,'share_page.html',{'photo':photo})