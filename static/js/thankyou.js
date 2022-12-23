const orderId = document.querySelector(".orderId");
const homePage = document.querySelector(".homePage");
const searchOrder = document.querySelector(".searchOrder");
import {getStatus, goToHomePage} from "./auth.js";

// 確認登入狀態
getStatus(checkStatus)
function checkStatus(elem){
    if(elem.data === null || !elem.data.id ){
        window.location.href = "/";
    }
}

// 取得訂單 id
const url = location.href;
const id = url.split("/thankyou?number=")[1];
orderId.innerText = id;

// 回首頁
homePage.addEventListener("click", goToHomePage);

// 查詢訂單
searchOrder.addEventListener("click", ()=>{
    let url = "/api/order/" + id;
    fetch(url,{
        method : "GET",
    }).then(function(response){
        return response.json();
    }).then(function(datas){
        if (!datas.error && datas.data !== null){
            window.location.href = "/api/order/" + id;
        }
    })
    
})

