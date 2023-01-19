// const camera = document.querySelector(".camera");
// const gallery = document.querySelector(".gallery");
const pop_up_bg = document.querySelector(".pop_up_bg");

const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

const camera_btn = document.querySelector(".camera_btn");
const gallery_btn = document.querySelector(".gallery_btn");
const guideline = document.querySelector(".guideline");
      
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});
      
function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('camera-image', blob);
        fetch('/test/', {
            method: 'POST',
            body: formData
        });
    });
}

function setChildValue(index1) {

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('camera-image', blob);
        fetch('/start/', {
            method: 'POST',
            body: formData
          });
        });
    window.location.href = `/${index1}`;
    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}



function camera() {
    if (camera_btn.innerText === '촬영') {
        camera_btn.innerText = '재촬영'
        guideline.style.display =  "none";
    }else if (camera_btn.innerText === '재촬영' | camera_btn.innerText === '카메라') {
        camera_btn.innerText = '촬영';
        guideline.style.display =  "block";
    }
}

function gallery() {
    camera_btn.innerText = '카메라';
    guideline.style.display =  "none";
}

function popup_open() {
    document.querySelector("#pop_up_bg").style.display = 'flex';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}

function popup_close() {
    document.querySelector("#pop_up_bg").style.display = 'none';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}