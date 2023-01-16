const camera = document.querySelector(".camera");
const gallery = document.querySelector(".gallery");
const pop_up_bg = document.querySelector(".pop_up_bg");

const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
      
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

//임의로 넣어둠.
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
    window.location.href = `/${index1}`;
    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}



// function setChildValue(index1) {
//     window.location.href = `/${index1}`;
//     // window.location.href = `indexcopy.html?${index1}?${index2}`;
// }

function popup_open() {
    document.querySelector("#pop_up_bg").style.display = 'flex';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}

function popup_close() {
    document.querySelector("#pop_up_bg").style.display = 'none';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}