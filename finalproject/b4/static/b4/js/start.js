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
        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('camera-image', blob);
            fetch('/start/', {
                method: 'POST',
                body: formData
              });
            });
        window.location.href = `/${index1}`;
    }
    // window.location.href = `indexcopy.html?${index1}?${index2}`;
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

function popup_open() {
    document.querySelector("#pop_up_bg").style.display = 'flex';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}

function popup_close() {
    document.querySelector("#pop_up_bg").style.display = 'none';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}