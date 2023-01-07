from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Photos

def test(request):
    return render(request,'camera_test.html')
# Create your views here.

def share_page(request, id):
    # photo = Photos.objects.all()
    # print(photo.converte_photo)
    photo = Photos.objects.filter(id = id)
    return render(request,'share_page.html',{'photo':photo})

def upload_photo(request):
    if request.method == 'POST':
        photo=Photos()
        photo.origin_photo = request.FILES["origin"]
        photo.converte_photo = request.FILES["converte"]
        photo.background_color = request.POST["color"]
        photo.background_photo = request.FILES["background"]
        photo.save()
        # fileupload = Photos(
        #     origin_photo = origin_photo,
        #     converte_photo = converte_photo,
        #     background_color = background_color,
        #     background_photo = background_photo
        # )
        # fileupload.save()
        return redirect('/share/'+str(photo.id))
    else:
        return render(request, 'upload_photo.html')

