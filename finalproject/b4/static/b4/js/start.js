// const camera = document.querySelector(".camera");
// const gallery = document.querySelector(".gallery");

const pop_up_bg = document.querySelector(".pop_up_bg");

const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
const image = document.getElementById('image');

const camera_btn = document.querySelector(".camera_btn");
const gallery_btn = document.querySelector(".gallery_btn");
const guideline = document.querySelector(".guideline");

document.getElementById('fileinput').addEventListener('change', function(evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            document.getElementById('image').src = fr.result;
        }
        fr.readAsDataURL(files[0]);
    }
});

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

function setChildValue(index1) {
    //메시지는 임의로 설정했습니다.
    if(camera_btn.innerText === '촬영'){
        alert("사진을 선택해주세요.");
    }
    else{
        document.querySelector('.main').classList.add('display-none');
        document.querySelector('.main2').classList.remove('display-none');
        setTimeout(typing, 1500);
        var imageSrc = document.getElementById('image').src;
        var binary = atob(imageSrc.split(',')[1]);
        var array = [];
        for (var i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }

        const formData = new FormData();
        formData.append('camera-image', new Blob([new Uint8Array(array)], { type: 'image/png' }));
        fetch('/start/', {
            method: 'POST',
            body: formData
        });
        setTimeout(function () {
            window.location.href = "/color";
        }, 15000);
        // window.location.href = `/${index1}`;
    } 
}



function camera() {
    if (camera_btn.innerText === '촬영') {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);
        const imageData = canvas.toDataURL('image/png');
        image.src = imageData;

        camera_btn.innerText = '재촬영';
        guideline.style.display =  "none";
        video.style.direction='none';

        image.style.display="block";

        
    }else if (camera_btn.innerText === '재촬영'||camera_btn.innerText === '카메라') {
        camera_btn.innerText = '촬영';
        guideline.style.display =  "block";
        video.style.direction='block';

        image.style.display="none";  

    }
}

function gallery() {
    camera_btn.innerText = '카메라';
    guideline.style.display =  "none";
    image.style.display="block";

}

// function popup_open() {
//     document.querySelector("#pop_up_bg").style.display = 'flex';

//     // window.location.href = `indexcopy.html?${index1}?${index2}`;
// }

// function popup_close() {
//     document.querySelector("#pop_up_bg").style.display = 'none';

//     // window.location.href = `indexcopy.html?${index1}?${index2}`;
// }


// $(document)


const text = document.querySelector(".str");
// text.innerHTML = 'asdfasdf'; 

// 글자 모음
const letters = ["촬영 시작합니다.", "앞에 봐주세요~", "얼굴 살짝만 왼쪽으로", "한 번 더 찍을게요."];

// 글자 입력 속도
const speed = 200;
let i = 0;

// 타이핑 효과
const typing = async () => {  
  const letter = letters[i].split("");
  
  while (letter.length) {
    await wait(speed);
    text.innerHTML += letter.shift(); 
  }
  
  // 잠시 대기
  await wait(800);
  
  // 지우는 효과
  remove();
}

// 글자 지우는 효과
const remove = async () => {
  const letter = letters[i].split("");
  
  while (letter.length) {
    await wait(speed);
    
    letter.pop();
    text.innerHTML = letter.join(""); 
  }
  
  // 다음 순서의 글자로 지정, 타이핑 함수 다시 실행
  i = !letters[i+1] ? 0 : i + 1;
  typing();
}

// 딜레이 기능 ( 마이크로초 )
function wait(ms) {
  return new Promise(res => setTimeout(res, ms))
}

// 초기 실행



