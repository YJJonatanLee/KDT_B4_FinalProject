import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Photos

def test(request):
    return render(request,'camera_view.html')
# Create your views here.


def loading(request):
    return render(request,'loading.html')

def bg_color(request):
    return render(request,'bg_color.html')


def share_page(request, id):
    # photo = Photos.objects.all()
    # print(photo.converte_photo)
    photo = Photos.objects.filter(id = id)
    return render(request,'share_page.html',{'photo':photo})

def start_page(request):
    return render(request,'start_page.html')

def upload_photo(request):
    if request.method == 'POST':
        photo=Photos()
        photo.origin_photo = request.FILES["origin"]
        photo.converte_photo = request.FILES["converte"]
        photo.background_color = request.POST["color"]
        photo.background_photo = request.FILES["background"]
        photo.save()
        return redirect('/share/'+str(photo.id))
    else:
        return render(request, 'upload_photo.html')

def update_photo(request, id):
    photo = Photos.objects.filter(id = id)
    photo.update(background_color='가')
    return render(request,'share_page.html',{'photo':photo})

def django_html_webcam_image_upload(request):
    if request.method == 'POST':
        img_base64 = request.POST['imgBase64']
        img_data = img_base64.split(',')[1] # remove the metadata

        # save the image in the "static/b4/img" folder
        with open('static/b4/img/image.png', 'wb') as fh:
            fh.write(base64.b64decode(img_data))
        return HttpResponse('Image uploaded successfully!')