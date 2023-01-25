import cv2
import os
import urllib


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


path_dir = 'media/origin_img/'
saving_dir = 'media/cutting_faces/'
files, file_names = make_file_list(path_dir)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Photos,CameraImage
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.conf import settings



import time

@csrf_exempt
def start_page(request):
    if request.method == 'POST':
        image = request.FILES.get('camera-image')
        CameraImage.objects.create(image=image)
        images = CameraImage.objects.all()
        time.sleep(10)

        a=1
        b=2
        print(a+b)
        #임시 작성 코드
        for i in images:
            img=Image.open(i.image)
            img.save('media/origin_img/img.png','PNG')
        return render(request,'bg_color.html')
   
    return render(request,'start_page.html')



def loading(request):
    # Cutting_face_save(cv2.imread(os.path.join(path_dir, files[0])), file_names[0], saving_dir)
    # time.sleep(10)
    return render(request,'loading.html')

def loading1(request):
    Cutting_face_save(cv2.imread(os.path.join(path_dir, files[0])), file_names[0], saving_dir)
    return render(request,'loading.html')

def bg_color(request):
    if request.method == 'POST':
        photo = Photos.objects.filter(id="1")
        color=request.POST.get('color')
        print(color)
        if color:
            photo.update(background_color=color)
        return redirect('/share/'+str(1))
    else:
        return render(request,'bg_color.html')

def share_page(request, id):
    photo = Photos.objects.filter(id = id)
    return render(request,'share_page.html',{'photo':photo})


def file_download(request, id):
    photo = get_object_or_404(Photos, id = id)
    url = photo.converte_photo.url[1:]
    file_path = urllib.parse.unquote(url)
    file_type = 'image/png'  
    binary_file = open(file_path, 'rb')
    response = HttpResponse(binary_file.read(), content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename=네모네모.png'
    return response



# def upload_photo(request):
#     if request.method == 'POST':
#         photo=Photos()
#         photo.origin_photo = request.FILES["origin"]
#         photo.converte_photo = request.FILES["converte"]
#         photo.background_color = request.POST["color"]
#         photo.background_photo = request.FILES["background"]
#         photo.save()
#         return redirect('/share/'+str(photo.id))
#     else:
#         return render(request, 'upload_photo.html')

# def update_photo(request, id):
#     photo = Photos.objects.filter(id = id)
#     photo.update(background_color='가')
#     return render(request,'share_page.html',{'photo':photo})

import os
import requests
import json


def face_recognition():
    client_id = settings.NAVER_API
    client_secret = settings.NAVER_SECRET
    # client_id = ""
    # client_secret = ""
    url = "https://openapi.naver.com/v1/vision/face" 
    files = {'image': open('media/background/t.jpg', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        face_lenth = '0'
        emotion = '0'
        json_object = json.loads(response.text)
        if json_object['info']['faceCount'] !=0:
            face_ratio = json_object['info']['size']['height']/json_object['info']['size']['width']
            if face_ratio > 1.3 and face_ratio <= 1.5:
                face_lenth = '1'
            elif face_ratio > 1.5:
                face_lenth = '2'
            emotion_r = json_object['faces'][0]['emotion']['value']
            if emotion_r in ['angry', 'disgust']:
                emotion = '2'
            elif emotion_r in ['fear', 'sad']:
                emotion = '3'
            elif emotion_r == 'surprise':
                emotion = '1'
            elif emotion_r == 'smile':
                emotion = '4'
            print (face_ratio, emotion_r)
            return face_lenth, emotion
    else:
        print("Error Code:" + rescode)
    return face_lenth, emotion

def change_color(image, face_color, hair_color):
    px = image.load()
    for i in range(0, 640):
        for j in range(0, 820):
            if px[i, j]==(255, 224, 189, 255):
                px[i, j] = face_color[0]
            elif px[i, j] == (255, 205, 148, 255):
                px[i, j] = face_color[1]
            elif px[i, j] == (118, 83, 57, 255):
                px[i, j] = hair_color
            elif px[i, j] == (76, 45, 23, 255):
                px[i, j] = (hair_color[0]-30, hair_color[1]-30, hair_color[2]-30)
            elif px[i, j] != (0, 0, 0, 0):
                px[i, j] = (hair_color[0]+30, hair_color[1]+30, hair_color[2]+30)


def create_character(request):
    face_lenth, emotion = '0', '0'
    # face_lenth, emotion = face_recognition() 
    result = {'face_lenth':face_lenth, 'hair_style':'short', 'front_hair_style':'short','face_color':[(255, 243, 219) ,((255, 232, 190))], "hair_color":(186,212,237), 'eye':'o','emotion':emotion}
    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/static/b4/img/character/'
    char_path ='face'+result['face_lenth']

    face = Image.open(dir+char_path+'/face'+result['face_lenth']+'_0.png')
    face_shadow = Image.open(dir+char_path+'/face'+result['face_lenth']+'_1.png')
    face.paste(face_shadow,(0,0),face_shadow)

    if result['hair_style'] in ['medium', 'long','longwave', 'mediumwave']:
        back_hair = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_2.png')
        if result['hair_style']=='longwave':
            back_hair_highlight=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_0.png')
            back_hair.paste(back_hair_highlight,(0,0),back_hair_highlight)
    elif result['hair_style']!='short' and result['hair_style']!='bald':
        back_hair = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_0.png')
        back_hair_shadow=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_2.png')
        back_hair.paste(back_hair_shadow,(0,0),back_hair_shadow)
        if result['hair_style']=='ponytail':
            accessory = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_3.png')
            back_hair.paste(accessory,(0,0),accessory)
        elif result['hair_style']=='braided':
            back_hair_highlight=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_1.png')
            back_hair.paste(back_hair_highlight,(0,0),back_hair_highlight)
    
    if result['hair_style']!='bald':
        front_hair=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_faceshadow.png')
        front_hair_main=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_0.png')
        front_hair_highlight=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_1.png')
        front_hair_shadow=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_2.png')
        front_hair.paste(front_hair_main,(0,0),front_hair_main)
        front_hair.paste(front_hair_highlight,(0,0),front_hair_highlight)
        front_hair.paste(front_hair_shadow,(0,0),front_hair_shadow)

    uniform=Image.open(dir+'uniform.png')
    face_emotion = Image.open(dir+char_path+'/emotion'+result['face_lenth']+'_'+result['eye']+'_'+result['emotion']+'.png')
    if result['hair_style']!='bald':
        face.paste(front_hair,(0,0),front_hair)
        if result['hair_style'] != 'short':
            back_hair.paste(face,(0,0),face)
            change_color(back_hair, result['face_color'], result['hair_color'])
            back_hair.paste(face_emotion,(0,0),face_emotion)
            back_hair.paste(uniform,(0,0),uniform)
            back_hair.save('media/test/new1.png','PNG')
        else:
            change_color(face, result['face_color'], result['hair_color'])
            face.paste(face_emotion,(0,0),face_emotion)
            face.paste(uniform,(0,0),uniform)
            face.save('media/test/new1.png','PNG')
    else:
        change_color(face, result['face_color'], result['hair_color'])
        face.paste(face_emotion,(0,0),face_emotion)
        face.paste(uniform,(0,0),uniform)
        face.save('media/test/new1.png','PNG')
    
    return render(request,'loading.html')


   