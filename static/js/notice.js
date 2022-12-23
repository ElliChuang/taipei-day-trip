const noticeWindowOuter = document.querySelector('.noticeWindowOuter');
const noticeWindow = document.querySelector('.noticeWindow');
const noticeTitle = document.querySelector('.noticeTitle');
const noticeMessage = document.querySelector('.noticeMessage');
const noticeEvent = document.querySelector('.noticeEvent');
export {showNoticeWindow, closeNoticeWindow};

function showNoticeWindow(elem1, elem2, elem3){
    noticeWindowOuter.style.display = "block";
    noticeWindow.style.display = "block";
    noticeTitle.innerText = elem1;
    noticeMessage.innerText = elem2;
    noticeEvent.addEventListener("click", elem3)
}

function closeNoticeWindow(){
    noticeWindowOuter.style.display = "none";
    noticeWindow.style.display = "none";
    noticeTitle.innerText = "";
    noticeMessage.innerText = "";
}