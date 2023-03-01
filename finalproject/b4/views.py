import os
import urllib
import os
import requests
import json
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Photos
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageColor
from django.conf import settings
from django.core.files import File
import time
import torch
import torchvision
from torchvision import transforms
import torch.nn as nn

def save_photo(image, uuid):
    """start.js로 부터 받은 정보를 db에 저장

    Args:
        image (blob): 캡쳐이미지 blob 데이터
        uuid (str): 사용자의 uuid 값

    Returns:
        int: 사용자의 id 값
    """
    photo = Photos()
    photo.origin_photo = image
    photo.uuid = uuid
    photo.save()
    return photo.id

def save_photo_media(photo_id, path):
    """blob파일을 이미지로 변환하여 저장

    Args:
        photo_id (int): 사용자의 id값
        path (str): 이미지가 저장되는 경로
    """
    photo = Photos.objects.get(id=photo_id)
    photo_file = File(photo.origin_photo.file)
    with open(path, 'wb') as f:
        for chunk in photo_file.chunks():
            f.write(chunk)


@csrf_exempt
def start_page(request: HttpResponse) -> HttpResponse:

    """ 시작 페이지

    Args:
        request (HttpResponse)

    Returns:
        HttpResponse
    
    url: start/
    """

    if request.method == 'POST':
        start = time.time()
        image = request.FILES.get('camera-image')
        uuid = request.POST.get('uuid-test')
        id = save_photo(image, uuid)
        save_photo_media(id,'media/origin_img/img.png')

        # 결과 기본 설정 
        result = {'face_lenth':'0', 'hair_style': 'short', 'front_hair_style':'short',
                  'face_color':[(255, 243, 219) ,((255, 232, 190))], "hair_color":(186,212,237), 
                  'eye':'x','emotion':'0'}
        
        # 원본 이미지 주소
        img_path = 'media/origin_img/img.png'

         # api를 통해 얻은 결과
        face_box=(0,0,0,0)
        result['face_lenth'], result['emotion'], result['hair_color'], result['face_color'], face_box, exist = face_recognition(img_path) 
        if exist == 1:
            image = Image.open(img_path).crop(face_box).convert('RGB')
            image.save('media/origin_img/img.png')

            # 헤어스타일 모델 적용 결과
            result['hair_style'] = hair_style(image)
            print(result['hair_style'])
            
            # 안경 모델 적용 결과
            result['eye'] = glasses_style(image)
            print(result['eye'])
            
            # 앞머리 모델 적용 결과
            result['front_hair_style'] = front_hair_style(image)
            print(result['front_hair_style'])
        
        # 캐릭터 생성
        create_character(result, id)
        end = time.time()
        print(f"{end - start:.5f} sec")
   
    return render(request,'start_page.html')


def bg_color(request: HttpResponse, uuid :str) -> HttpResponse:

    """ 배경색 변경 페이지. 

    Args:
        request (HttpResponse)
        uuid (str): 사용자의 uuid 값

    Returns:
        HttpResponse

    url: color/
    """
    
    photo = Photos.objects.filter(uuid = uuid)
    id=photo[0].id
    character_url=photo[0].converted_photo.url
    print(uuid)
    print(character_url[1:])
    print(id)

    # 배경색 선택
    if request.method == 'POST':
        color=request.POST.get('color')
        
        print(color)
        if color:
            photo.update(background_color=color)
        else: 
            color = '#ffffff'
        # 이미지 저장
        add_bg_color(photo[0],character_url, color, id)
        return redirect('/share/'+str(id))
    else:
        return render(request,'bg_color.html',{'photo':photo})


def share_page(request: HttpResponse, id :int) -> HttpResponse:

    """ 결과/공유 페이지. 

    Args:
        request (HttpResponse)
        id (int): 사용자의 id 값

    Returns:
        HttpResponse

    url: share/<int:id>
    """

    photo = Photos.objects.filter(id = id)
    return render(request,'share_page.html',{'photo':photo})


def file_download(request: HttpResponse, id: int) -> HttpResponse:

    """ 최종 결과 이미지를 기기에 저장하는 함수

    Args:
        request (HttpResponse)
        id (int): 사용자의 id 값

    Returns:
        HttpResponse
    """

    photo = get_object_or_404(Photos, id = id)
    url = photo.background_photo.url[1:]
    file_path = urllib.parse.unquote(url)
    
    if os.path.exists(file_path):
        file_type = 'image/png'  
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type=file_type)
        response['Content-Disposition'] = 'attachment; filename=네모네모.png'
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")


def change_color(image: Image, face_color: list, hair_color: tuple) -> None:

    """ 생성된 캐릭터의 머리, 피부 색을 변환하는 함수

    Args:
        image (Image): 생성된 캐릭터 이미지
        face_color (list): 피부과 그림자의 rgb 값을 담은 리스트, [(피부색), (그림자색)] = [(r, g, b), (r, g, b)]
        hair_color (tuple): 머리색의 rgb 값, (r, g, b)
    """

    px = image.load()
    for i in range(0, 640):
        for j in range(0, 820):
            if px[i, j]==(255, 224, 189, 255): # 피부색 변경
                px[i, j] = face_color[0]
            elif px[i, j] == (255, 205, 148, 255): # 피부 그림자색 변경
                px[i, j] = face_color[1]
            elif px[i, j] == (118, 83, 57, 255): # 머리색 변경
                px[i, j] = hair_color
            elif px[i, j] == (76, 45, 23, 255) or px[i, j] == (69, 49, 34, 255): # 머리 그림자색 변경
                px[i, j] = (hair_color[0]-30, hair_color[1]-30, hair_color[2]-30)
            elif px[i, j] != (0, 0, 0, 0) and px[i, j] != (0, 0, 0, 255): # 머리 하이라이트 색 변경
                px[i, j] = (hair_color[0]+30, hair_color[1]+30, hair_color[2]+30)


def add_bg_color(photo: Photos, character_url: str, color_hex: str, id: int) -> None:

    """ 선택된 배경색을 합친 이미지 저장
    Args:
        photo (Photos): 해당 Photos
        character_url (str): character이미지의 url
        color_hex (str): 선택한 배경 색상 (hex 형태)
        id (int): 사용자의 id 값
    """

    color = ImageColor.getcolor(color_hex, "RGB")
    character=Image.open(character_url[1:])
    data = np.zeros([820, 640, 3], dtype=np.uint8)
    data[:,:] = color
    image = Image.fromarray(data, 'RGB') # data를 이미지 객체로 변환한 뒤 화면에 표시한다.
    image.paste(character,(0,0),character)
    image.save('media/test/add_bg'+str(id)+'.png','PNG')
    photo.background_photo = File(open('media/test/add_bg'+str(id)+'.png', 'rb'))
    photo.save()
    os.remove('media/test/add_bg'+str(id)+'.png')


def create_character(result: dict, id: int) -> None:

    """ 나온 결과들을 바탕으로 캐릭터 이미지를 생성하는 함수

    Args:
        result (dict): 나온 결과들({'face_lenth': 얼굴 비율, 'hair_style':머리 스타일, 'front_hair_style':앞머리 모양,
                  'face_color':피부색, "hair_color":머리색, 'eye':안경 유무,'emotion': 표정})
        id (int): 사용자 id 값
    """
    
    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/static/b4/img/character/'
    char_path ='face'+result['face_lenth']

    face = Image.open(dir+char_path+'/face'+result['face_lenth']+'_0.png') # 얼굴 이미지 불러오기
    face_shadow = Image.open(dir+char_path+'/face'+result['face_lenth']+'_1.png') # 얼굴 그림자 이미지 불러오기
    face.paste(face_shadow,(0,0),face_shadow) # 얼굴 이미지에 얼굴 그림자 이미지 복사

    if result['hair_style']=='shortwave':
        result['front_hair_style']='shortwave'

    # 해어 추가(뒷머리가 있는 경우만)
    if result['hair_style'] in ['medium', 'long','longwave', 'mediumwave']:
        back_hair = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_2.png')
        if result['hair_style']=='longwave': # 장발 웨이브에 경우 헤어 하이라이트 추가
            back_hair_highlight=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_0.png')
            back_hair.paste(back_hair_highlight,(0,0),back_hair_highlight)
    elif result['hair_style']!='short' and result['hair_style']!='bald':
        back_hair = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_0.png')
        back_hair_shadow=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_2.png')
        back_hair.paste(back_hair_shadow,(0,0),back_hair_shadow)
        if result['hair_style']=='ponytail': # 포니테일의 경우 머리끈 추가
            accessory = Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_3.png')
            back_hair.paste(accessory,(0,0),accessory)
        elif result['hair_style']=='braided': # 땋은 양갈래의 경우 헤어 하이라이트 추가
            back_hair_highlight=Image.open(dir+char_path+'/'+result['hair_style']+result['face_lenth']+'_1.png')
            back_hair.paste(back_hair_highlight,(0,0),back_hair_highlight)
    
    # 앞머리 추가(대머리 제외)
    if result['hair_style']!='bald':
        front_hair=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_faceshadow.png')
        front_hair_main=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_0.png')
        front_hair_highlight=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_1.png')
        front_hair_shadow=Image.open(dir+char_path+'/'+result['front_hair_style']+result['face_lenth']+'_2.png')
        front_hair.paste(front_hair_main,(0,0),front_hair_main)
        front_hair.paste(front_hair_highlight,(0,0),front_hair_highlight)
        front_hair.paste(front_hair_shadow,(0,0),front_hair_shadow)

    # 교복, 표정 이미지 불러오기
    uniform=Image.open(dir+'uniform.png')
    face_emotion = Image.open(dir+char_path+'/emotion'+result['face_lenth']+'_'+result['eye']+'_'+result['emotion']+'.png')

    # 얼굴, 교복, 머리, 표정 합치고 저장
    photo = Photos.objects.filter(id = id).first()
    print(photo)
    if result['hair_style']!='bald':
        face.paste(front_hair,(0,0),front_hair)
        if result['hair_style'] != 'short' and result['hair_style'] != 'shortwave': # 뒷머리가 있는 경우
            back_hair.paste(face,(0,0),face)
            change_color(back_hair, result['face_color'], result['hair_color'])
            back_hair.paste(face_emotion,(0,0),face_emotion)
            back_hair.paste(uniform,(0,0),uniform)
            back_hair.save('media/test/character'+str(id)+'.png','PNG')
            
        else: # 뒷머리가 없는 경우
            change_color(face, result['face_color'], result['hair_color'])
            face.paste(face_emotion,(0,0),face_emotion)
            face.paste(uniform,(0,0),uniform)
            face.save('media/test/character'+str(id)+'.png','PNG')
            
    else: # 대머리
        change_color(face, result['face_color'], result['hair_color'])
        face.paste(face_emotion,(0,0),face_emotion)
        face.paste(uniform,(0,0),uniform)
        face.save('media/test/character'+str(id)+'.png','PNG')

    photo.converted_photo = File(open('media/test/character'+str(id)+'.png', 'rb'))
    photo.save()
    os.remove('media/test/character'+str(id)+'.png')


def color_picker(img_path: str, x: int, y: int) -> tuple:

    """ 원본 이미지에서 색상을 추출할 부분(x,y을 중심으로 -3~3범위의 픽셀)의 rgb 값의 평균을 반환하는 함수 

    Args:
        img_path (str): 원본 이미지 주소
        x (int): 입력된 x좌표
        y (int): 입력된 y좌표

    Returns:
        tuple: (r, g, b)
    """

    image = Image.open(img_path)
    px = image.load()
    a = [-3, -2, -1, 0, 1, 2, 3]
    n=0
    R,G,B= 0, 0, 0
    for i in a:
        xx=x+i
        if xx>=0 and xx<image.size[0]:
            for j in a:
                yy=y+j
                if yy>=0 and yy<image.size[1]:
                    n+=1
                    R+=px[xx, yy][0]
                    G+=px[xx, yy][1]
                    B+=px[xx, yy][2]
    if n==0: n=1
    return (R//n+1, G//n+1, B//n+1)


def face_color_picker(rgb: tuple) -> list:

    """ 추출된 얼굴의 평균 rgb 값을 미리 지정해 놓은 9가지 피부 그림자 rgb 값과 비교하여 
    가장 가까운 피부과 피부 그림자의 rgb 값을 튜플 형태로 반환하는 함수

    Args:
        rgb (tuple): (r, g, b)

    Returns:
        list: [(피부색), (그림자색)] = [(r, g, b), (r, g, b)]
    """

    color = [[(255, 243, 219), (255, 232, 190)], [(254, 230, 218), (252, 215, 199)], [(255, 238, 220), (254, 224, 188)],
            [(255, 224, 189),(255, 204, 148)], [(255, 208, 188), (231, 175, 150)], [(255, 209, 157), (234, 186, 132)],
            [(233, 185, 149), (215, 159, 120)], [(165, 114, 87) ,(140, 89, 62)], [(175, 127, 89), (150, 102, 66)]]
    idx=0
    err=765
    for i in range(9):
        a = abs(rgb[0]-color[i][1][0])+abs(rgb[1]-color[i][1][1])+abs(rgb[2]-color[i][1][2])
        if err>a:
            err=a
            idx=i
    return color[idx]


def face_recognition(img_path: str) -> tuple:

    """ 네이버 face recognition api를 활용하여 얼굴의 위치, 길이, 표정를 찾고 
    이를 활용하여 얼굴의 비율, 피부색, 머리색, 표정을 반환하는 함수

    Args:
        img_path (str): 원본 이미지의 주소

    Returns:
        tuple: (face_lenth, emotion, hair_color, face_color)
            face_lenth (str): 얼굴의 세로/가로 비율 (0, 1, 2)
            emotion (str): 표정 (0, 1, 2, 3, 4)
            hair_color (tuple): 머리색, color_picker()의 반환값 ((r, g, b))
            face_color (list): 피부색, face_color_picker()의 반환값 ([(피부색), (그림자색)] = [(r, g, b), (r, g, b)])
            face_box (tuple): crop실시할 x,y값 범위
            exist(int): 이미지에 존재하는 인원 수
    """

    # api 실행
    client_id = settings.NAVER_API
    client_secret = settings.NAVER_SECRET
    url = "https://openapi.naver.com/v1/vision/face" 
    files = {'image': open(img_path, 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code

    # 초기 설정
    face_lenth = '0'
    emotion = '0'
    hair_color = (0,0,0)
    face_color = [(255, 243, 219) ,((255, 232, 190))]
    face_box=(0,0,0,0)
    exist = 0
    if(rescode==200):
        json_object = json.loads(response.text)
        if json_object['info']['faceCount'] !=0:
            exist = 1
            # 얼굴 비율
            face_ratio = json_object['faces'][0]['roi']['height']/json_object['faces'][0]['roi']['width']
            if face_ratio > 1.2 and face_ratio <= 1.4:
                face_lenth = '1'
            elif face_ratio > 1.4:
                face_lenth = '2'

            # 표정
            emotion_r = json_object['faces'][0]['emotion']['value']
            if emotion_r in ['angry', 'disgust']:
                emotion = '2'
            elif emotion_r in ['fear', 'sad']:
                emotion = '3'
            elif emotion_r == 'surprise':
                emotion = '1'
            elif emotion_r == 'smile':
                emotion = '4'
            print (face_ratio, emotion_r, json_object)

            # 머리색
            x,y = json_object['faces'][0]['roi']['x'],json_object['faces'][0]['roi']['y']
            hair_color = color_picker(img_path, x, y)

            # 피부색
            x_f,y_f = json_object['faces'][0]['roi']['x']+json_object['faces'][0]['roi']['width']//2,json_object['faces'][0]['roi']['y']+json_object['faces'][0]['roi']['height']//2
            rgb = color_picker(img_path, x_f, y_f)
            face_color = face_color_picker(rgb)

            # crop
            x_ltop=json_object['faces'][0]['roi']['x']
            y_ltop=json_object['faces'][0]['roi']['y']

           
            #액자 미리 구성
            x_frame=[i*24 for i in range(1,51)]
            y_frame=[i*32 for i in range(1,51)]
            
            #프레임 초기화
            frame=(0,0)

            """ 
            이미지 크기가 프레임 크기보다 작다면 반복문을 탈출하고 이미지 크기에 맞는 프레임 정의
            """
            for f in zip(x_frame,y_frame): 
                if (f[0]>json_object['faces'][0]['roi']['width'] and f[1]>json_object['faces'][0]['roi']['height']):
                    frame=f
                    break

            
            x,y=(x_ltop+json_object['faces'][0]['roi']['width']//2),(y_ltop+json_object['faces'][0]['roi']['height']//2)
            
            face_box=(x-frame[0],y-frame[1],x+frame[0],y+frame[1])

            return face_lenth, emotion, hair_color, face_color, face_box, exist
    else:
        print("Error Code:" + str(rescode))
        return face_lenth, emotion, hair_color, face_color, face_box, exist
    return face_lenth, emotion, hair_color, face_color, face_box, exist


def hair_style(image):
    """머리 스타일 분류

    Args:
        image (Image): 입력 이미지

    Returns:
        str: 헤어스타일 분류 결과(bald, braided, bun, long, longwave, medium, mediumwave, pigtails, ponytail, short, shortwave)
    """
    model = torchvision.models.efficientnet_b0(weights=None)
    model.classifier = nn.Linear(in_features=1280, out_features=11)
    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/static/b4/models/hairstyle_efficientnet.pth'
    model.load_state_dict(torch.load(dir, map_location = 'cpu'))

    preprocess = transforms.Compose([
        transforms.Resize((210, 280)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze_(0)

    model.eval()

    output = model(image_tensor)
    _, pred = torch.max(output, 1)

    labels = ['bald','braided','bun','long','longwave','medium','mediumwave','pigtails','ponytail','short','shortwave']

    return labels[pred]


def front_hair_style(image: Image) -> str:

    """ 앞머리 스타일 분류

    Args:
        image (Image): 입력 이미지

    Returns:
        str: 헤어스타일 분류 결과(short, shortall, shortfront, shorthalf)
    """

    model = torchvision.models.mobilenet_v2(weights=None)
    dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/static/b4/models/fronthair_mobilenetv2_0.pth'
    model.load_state_dict(torch.load(dir, map_location = 'cpu'))

    preprocess = transforms.Compose([
        transforms.Resize((210, 280)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze_(0)

    model.eval()

    output = model(image_tensor)
    _, pred = torch.max(output, 1)

    labels = ['short', 'shortall', 'shortfront', 'shorthalf']

    return labels[pred]


def glasses_style(img):

  """
  안경 착용 유무 반환하는 함수
  img: 이미지
  """
  
  # 안경 분류
  glasses_dict = {0:"o", 1:"x"}

  # device 설정 (cuda:0 혹은 cpu)
  # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

  # model load
  dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/static/b4/models/glasses_mobilenetv2-pretrained.pth'
  glasses_model = torchvision.models.mobilenet_v2(weights=None)
  fc = nn.Sequential(
      nn.Linear(1280, 512),
      nn.ReLU(), 
      nn.Linear(512, 128),
      nn.ReLU(), 
      nn.Linear(128, 32), 
      nn.ReLU(), 
      nn.Linear(32, 2)
  )
  glasses_model.classifier = fc
  glasses_model.load_state_dict(torch.load(dir, map_location = 'cpu'))
  # glasses_model.to(device)

  # 이미지 전처리
  preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
  image_tensor = preprocess(img)
  image_tensor = image_tensor.unsqueeze_(0)

  # prediction
  glasses_model.eval()
  output = glasses_model(image_tensor)
  _, pred = output.max(dim = 1)

  return glasses_dict[pred.item()]
