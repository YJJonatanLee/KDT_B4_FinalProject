const camera = document.querySelector(".camera");
const gallery = document.querySelector(".gallery");

const pop_up_bg = document.querySelector(".pop_up_bg");



function setChildValue(index1) {
    window.location.href = `/${index1}`;
    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}

function popup_open() {
    document.querySelector("#pop_up_bg").style.display = 'flex';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}

function popup_close() {
    document.querySelector("#pop_up_bg").style.display = 'none';

    // window.location.href = `indexcopy.html?${index1}?${index2}`;
}