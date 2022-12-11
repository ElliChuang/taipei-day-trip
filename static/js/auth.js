let outer = document.getElementById("outer");
let login = document.getElementById("login");
let signup = document.getElementById("signup");
let item2 = document.getElementById("item2");
let item3 = document.getElementById("item3");
let loginEmail = document.getElementById("loginEmail");
let loginPassword = document.getElementById("loginPassword");
let signUpName = document.getElementById("signUpName");
let signUpEmail = document.getElementById("signUpEmail");
let signUpPassword = document.getElementById("signUpPassword");
let loginMessage = document.getElementById("loginMessage");
let signUpMessage = document.getElementById("signUpMessage");


// 呼叫 登入／註冊 視窗
function closeView(){
    outer.style.display = "none";
    signup.style.display = "none";
    login.style.display = "none";
}

function goLogin(){
    outer.style.display = "block";
    signup.style.display = "none";
    login.style.display = "block";
    // 清除input值
    loginEmail.value = ""; 
    loginPassword.value = "";
    loginMessage.innerText = "";
}

function goSignUp(){
    outer.style.display = "block";
    signup.style.display = "block";
    login.style.display = "none";
    // 清除input值
    signUpName.value = "";
    signUpEmail.value = "";
    signUpPassword.value = "";
    signUpMessage.innerText = "";
}

// 點擊nav title 回首頁
function backToHomePage(){
    window.location.href = "/";
}

// 註冊會員
function signUp(){
    let url = "/api/user";
    let requestBody = {"name" : signUpName.value, "email" : signUpEmail.value, "password" : signUpPassword.value};
    fetch(url,{
        method : "POST",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
            return response.json();
    }).then(function(Data){
        console.log("註冊會員：", Data)
        if(Data.ok){
            signUpMessage.innerText = "註冊成功";     
        }else{
            signUpMessage.innerText = Data.data;     
        }
    })
}

// 取得會員狀態
function getStatus(){
    let url = "/api/user/auth";
    fetch(url,{
        method : "GET",
    }).then(function(response){
            return response.json();
    }).then(function(Data){
        console.log("會員狀態:", Data)
        if(Data.data !== null && Data.data.id ){
            item2.style.display = "none";
            item3.style.display = "block";
        }else{
            item2.style.display = "block";
            item3.style.display = "none";
        }
    })
}
getStatus();


// 會員登入
function memberLogin(){
    let url = "/api/user/auth";
    let requestBody = {"email" : loginEmail.value, "password" : loginPassword.value};
    console.log(requestBody)
    fetch(url,{
        method : "PUT",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
            return response.json();
    }).then(function(Data){
        console.log("會員登入:", Data);
        if(Data.ok){
            location.reload();
        }else{
            loginMessage.innerText = Data.data; 
        } 
    })          
}

// 會員登出
function memberLogout(){
    let url = "/api/user/auth";
    fetch(url,{
        method : "DELETE",
    }).then(function(response){
        return response.json();
    }).then(function(Data){
        console.log("會員登出:", Data);
        if(Data.ok){
            location.reload();
        }
    })
}