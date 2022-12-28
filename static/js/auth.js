const outer = document.getElementById("outer");
const login = document.getElementById("login");
const signup = document.getElementById("signup");
const loginClosed = document.getElementById("loginClosed");
const signUpClosed = document.getElementById("signUpClosed");
const goLogin = document.getElementById("goLogin");
const goSignUp = document.getElementById("goSignUp");
const loginOfNav = document.getElementById("loginOfNav");
const logoutOFNav = document.getElementById("logoutOFNav");
const backToHomePage = document.getElementById("backToHomePage");
const goToBookingPage = document.getElementById("goToBookingPage");
const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");
const signUpName = document.getElementById("signUpName");
const signUpEmail = document.getElementById("signUpEmail");
const signUpPassword = document.getElementById("signUpPassword");
const memberSignUp = document.getElementById("memberSignUp");
const loginMessage = document.getElementById("loginMessage");
const signUpMessage = document.getElementById("signUpMessage");
const memberLogin = document.getElementById("memberLogin");
const loginPasswordShow = document.getElementById("loginPasswordShow");
const loginPasswordHidden = document.getElementById("loginPasswordHidden");
const signUpPasswordShow = document.getElementById("signUpPasswordShow");
const signUpPasswordHidden = document.getElementById("signUpPasswordHidden");
export {loginOfNav, logoutOFNav, showLogin, getStatus, goToHomePage};
import {showNoticeWindow, closeNoticeWindow} from "./notice.js";

// 關閉 登入／註冊 視窗
loginClosed.addEventListener("click", closeView);
signUpClosed.addEventListener("click", closeView);
function closeView(){
    outer.style.display = "none";
    signup.style.display = "none";
    login.style.display = "none";
}

// 顯示登入頁面
goLogin.addEventListener("click", showLogin);
loginOfNav.addEventListener("click", showLogin);
function showLogin(){
    outer.style.display = "block";
    signup.style.display = "none";
    login.style.display = "block";
    // 清除input值
    loginEmail.value = ""; 
    loginPassword.value = "";
    loginMessage.innerText = "";
}

// 顯示註冊頁面
goSignUp.addEventListener("click", ()=>{
    outer.style.display = "block";
    signup.style.display = "block";
    login.style.display = "none";
    // 清除input值
    signUpName.value = "";
    signUpEmail.value = "";
    signUpPassword.value = "";
    signUpMessage.innerText = "";
});


// 點擊 nav title 回首頁
backToHomePage.addEventListener("click", goToHomePage)
function goToHomePage(){
    window.location.href = "/";
}

// 點擊 nav 預定行程 跳轉 Booking 頁面
goToBookingPage.addEventListener("click", ()=>{
    if(loginOfNav.style.display === "none"){
        window.location.href = "/booking";
    }else if(logoutOFNav.style.display === "none"){
        showLogin();
    }
})


// 顯示密碼
signUpPasswordHidden.addEventListener("click", showPassword)
loginPasswordHidden.addEventListener("click", showPassword)
function showPassword(){
    signUpPasswordHidden.style.display = "none";
    signUpPasswordShow.style.display = "block";
    signUpPassword.setAttribute("type", "text");
    loginPasswordHidden.style.display = "none";
    loginPasswordShow.style.display = "block";
    loginPassword.setAttribute("type", "text");
}

// 隱藏密碼
signUpPasswordShow.addEventListener("click", hidePassword)
loginPasswordShow.addEventListener("click", hidePassword)
function hidePassword(){
    signUpPasswordShow.style.display = "none";
    signUpPasswordHidden.style.display = "block";
    signUpPassword.setAttribute("type", "password");
    loginPasswordShow.style.display = "none";
    loginPasswordHidden.style.display = "block";
    loginPassword.setAttribute("type", "password");
}


// 註冊會員
memberSignUp.addEventListener("click", ()=>{
    let url = "/api/user";
    let requestBody = {"name" : signUpName.value, "email" : signUpEmail.value, "password" : signUpPassword.value};
    fetch(url,{
        method : "POST",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
            return response.json();
    }).then(function(Data){
        if(Data.ok){
            signUpMessage.innerText = "註冊成功";
            closeView();
            showNoticeWindow("註冊成功", "請登入會員", closeNoticeWindow);     
        }else{
            signUpMessage.innerText = Data.data;     
        }
    })
})

// 取得會員狀態
function getStatus(callback){
    let url = "/api/user/auth";
    fetch(url,{
        method : "GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        callback(data);
    })
}

// 顯示登入／登出 of nav bar
getStatus(navOfLoginOrLogout);
function navOfLoginOrLogout(elem){
    if(elem.data !== null && elem.data.id){
        loginOfNav.style.display = "none";
        logoutOFNav.style.display = "block";
    }else{
        loginOfNav.style.display = "block";
        logoutOFNav.style.display = "none";
    }
}

// 重新載入頁面
function reLoadPage(){
    location.reload()
}

// 會員登入
memberLogin.addEventListener("click", ()=>{
    let url = "/api/user/auth";
    let requestBody = {"email" : loginEmail.value, "password" : loginPassword.value};
    fetch(url,{
        method : "PUT",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
        return response.json();
    }).then(function(Data){
        console.log("會員登入:", Data);
        if(Data.ok){
            closeView();
            showNoticeWindow("登入成功", "點選確定，繼續瀏覽景點", reLoadPage);
        }else{
            loginMessage.innerText = Data.data; 
        } 
    })     
})

// 會員登出
logoutOFNav.addEventListener("click", ()=>{
    let url = "/api/user/auth";
    fetch(url,{
        method : "DELETE",
    }).then(function(response){
        return response.json();
    }).then(function(Data){
        if(Data.ok){
            reLoadPage();
        }
    })
})
