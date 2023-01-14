

// var string = ["촬영 시작합니다.", "앞에 봐주세요~", "얼굴 살짝만 왼쪽으로", "한 번 더 찍을게요."];

const $text = document.querySelector(".text");

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
    $text.innerHTML += letter.shift(); 
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
    $text.innerHTML = letter.join(""); 
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
setTimeout(typing, 1500);
// // var str = string.split("");
// var el = document.querySelector('.str').innerHTML;
// // (function animate() {
// // str.length > 0 ? el.innerHTML += str.shift() : clearTimeout(running); 
// // // var running = setTimeout(animate, 90);
// // // })();

// // // (function animate(s) {
// // //     el.innerHTML += s; 
// // // })();
// // string.forEach(s=>{
// //     console.log(s.split(""));
// //     s.split("").forEach(i=>{
// //         setTimeout(() => el += i, 500);
// //         // animate(i)
// //         // timeInterval = setInterval(animate, 1000);
// //     })
// //     // console.log(s.split("").shift());
// //     // el.innerHTML += s.split("").shift();
    
// //     // el='';
// // })
// var string = ["촬영 시작합니다.", "앞에 봐주세요~", "얼굴 살짝만 왼쪽으로", "한 번 더 찍을게요."];
// let str =''
// var el = document.querySelector('.str');
// let running;

// sleep(3000).then(() => console.log("after"));

// // (function animate() {
    


// // })();
// // string.forEach(s=>{
// //     running = setTimeout(animate, 90);
// //     str = s.split("");
// //     console.log(str)
    
// // })
// animate2()
// function animate2() {
//     string.forEach(s=>{
        
//         str = s.split("");
//         console.log(str)
//         // console.log(str)
//         running = setTimeout(animate, 90);
        
//     })
//     str.length > 0 ? el.innerHTML += str.shift() : clearTimeout(running); 
// }
// function animate() {
//     str.length > 0 ? el.innerHTML += str.shift() : clearTimeout(running); 
// }
// // var str = string.split("");
