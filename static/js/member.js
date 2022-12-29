const userName = document.querySelector('[name=userName]');
const userEmail = document.querySelector('[name=userEmail]');
const userOldPassword = document.querySelector('[name=userOldPassword]');
const userNewPassword = document.querySelector('[name=userNewPassword]');
const reUserNewPassword = document.querySelector('[name=reUserNewPassword]');
const inforButton = document.getElementById("inforButton");
const passwordButton = document.getElementById("passwordButton");
const memberName = document.getElementById("memberName");
import {getStatus} from "./auth.js";
import {showNoticeWindow, closeNoticeWindow} from "./notice.js";

getStatus(checkStatus)
function checkStatus(elem){
    if(elem.data !== null && elem.data.id){
        memberName.innerText = elem.data.name;
        userName.value = elem.data.name;
    }else{
        window.location.href = "/";
    }
}

// 重新載入頁面
function reLoadPage(){
    location.reload()
}

inforButton.addEventListener("click", personalInfor)
async function personalInfor(){
    if (!userName.validity.valid ){
        showNoticeWindow("錯誤訊息", "請輸入修正後會員姓名", closeNoticeWindow);
    }else if(!userEmail.validity.valid){
        showNoticeWindow("錯誤訊息", "請輸入信箱，或信箱格式有誤", closeNoticeWindow);
    }else{
        let url = "/api/member";
        let requestBody = {"name" : userName.value, "email" : userEmail.value}
        const res = await fetch(url,{
                                    method : "PATCH",
                                    headers : {"content-type" : "application/json"},
                                    body : JSON.stringify(requestBody),
                                }
                            );
        const data = await res.json();
        console.log(data);
        if (data.ok){
            showNoticeWindow("修改成功", "點選確定，關閉訊息", reLoadPage);
        }else{
            showNoticeWindow("錯誤訊息", "資料填寫有誤，或格式為符", closeNoticeWindow);
        }
        
    }
        
}    

passwordButton.addEventListener("click", modifyPassword)
async function modifyPassword(){
    if (userOldPassword.validity.valid && userNewPassword.validity.valid && reUserNewPassword.validity.valid){
        let url = "/api/member";
        let requestBody = {"password" : userOldPassword.value, "newPassword" : userNewPassword.value, "checkPassword" : reUserNewPassword.value}
        const res = await fetch(url,{
                                    method : "PATCH",
                                    headers : {"content-type" : "application/json"},
                                    body : JSON.stringify(requestBody),
                                }
                            );
        const data = await res.json();
        console.log(data);
        if (data.ok){
            showNoticeWindow("修改成功", "下次登入，請以新密碼登入。", reLoadPage);
        }else {
            showNoticeWindow("錯誤訊息", data.data, closeNoticeWindow);
        }
    }else{
        showNoticeWindow("錯誤訊息", "請輸入密碼，或密碼格式有誤", closeNoticeWindow);
    }


        
      
}   



