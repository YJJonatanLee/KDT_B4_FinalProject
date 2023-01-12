import base64
import cv2
import numpy as np
import os

def make_file_list(path_dir):
    file_list = os.listdir(path_dir)
    file_name_list = []
    for i in range(len(file_list)):
        file_name_list.append(file_list[i].replace(".jpg",""))
    return file_list, file_name_list

def Cutting_face_save(image, name, saving_dir):
    face_cascade = cv2.CascadeClassifier('media/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cropped = image[y-40 : y+h+40, x-40: x+w+40]
        resize = cv2.resize(cropped, (180,180))
        cv2.imwrite(os.path.join(saving_dir, f"{name}.jpg"), resize)


path_dir = 'media/origin/'
saving_dir = 'media/cutting_faces/'
files, file_names = make_file_list(path_dir)


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Photos,Test


def test(request):
    return render(request,'camera_view.html')


def loading(request):
    Cutting_face_save(cv2.imread(os.path.join(path_dir, files[0])), file_names[0], saving_dir)
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






    