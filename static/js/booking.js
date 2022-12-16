const order = document.querySelector(".order");
const confirmAmount = document.querySelector(".confirmAmount");
const memberName = document.getElementById("memberName");
const name = document.querySelector('[name=name]')
const email = document.querySelector('[name=email]')
const contactForm = document.querySelector('.contactForm')
const paymentForm = document.querySelector('.paymentForm')
const confirmForm = document.querySelector('.confirmForm')
const noOrder = document.querySelector('.noOrder')
const hr = document.querySelectorAll('hr')
const homePage = document.getElementById("homePage");

import {getStatus} from "./auth.js";

getStatus(checkStatus)
function checkStatus(elem){
    if(elem.data !== null && elem.data.id){
        memberName.innerText = elem.data.name;
        name.value = elem.data.name;
        email.value = elem.data.email;
    }else{
        window.location.href = "/";
    }
}

function getOrderInfor(callback){
    let url = "/api/booking";
    fetch(url,{
        method : "GET",
    }).then(function(response){
            return response.json();
    }).then(function(datas){
        callback(datas);
    })
}
getOrderInfor(checkOrder);

function checkOrder(datas){
    if(datas.data === null){
        contactForm.style.display = "none";
        paymentForm.style.display = "none";
        confirmForm.style.display = "none";
        noOrder.style.display = "block";
        hr.forEach((elem)=> elem.style.display = "none")
    }else{
        contactForm.style.display = "block";
        paymentForm.style.display = "block";
        confirmForm.style.display = "block";
        noOrder.style.display = "none";
        hr.forEach((elem)=> elem.style.display = "block")
        showCart(datas);
    }
}


function showCart(datas){
    let amount = 0 
    let dataLength = datas.data.length;
    for(let i = 0; i < dataLength; i +=1){
        // item section
        let sectionDiv = document.createElement("div");
        sectionDiv.className = "section";
        order.appendChild(sectionDiv);
        // img
        let pictureDiv = document.createElement("div");
        pictureDiv.className = "picture";
        let img = document.createElement("img");
        let imgId = document.createElement("span");
        img.className = "cartItemImage";
        img.src = datas.data[i].attraction.image;
        imgId.textContent = datas.data[i].attraction.id;
        imgId.className = "cartItemId";
        pictureDiv.appendChild(imgId);
        pictureDiv.appendChild(img);
        sectionDiv.appendChild(pictureDiv);
        // infor
        let inforDiv = document.createElement("div");
        sectionDiv.appendChild(inforDiv);
        inforDiv.className = "infor";
        // title
        let titleDiv = document.createElement("div");
        inforDiv.appendChild(titleDiv);
        titleDiv.innerText = `台北一日遊：${datas.data[i].attraction.name}`;
        titleDiv.className = "title";
        // date
        let dateDiv = document.createElement("div");
        inforDiv.appendChild(dateDiv);
        dateDiv.innerText = `日期：${datas.data[i].date}`;
        dateDiv.className = "message";
        // time
        let timeDiv = document.createElement("div");
        inforDiv.appendChild(timeDiv);
        timeDiv.className = "message";
        if(datas.data[i].time === "morning"){
            timeDiv.innerText = "時間：早上９點至下午２點";
        }else if(datas.data[i].time === "afternoon"){
            timeDiv.innerText = "時間：下午１點至下午６點";
        }
        // price
        let priceDiv = document.createElement("div");
        inforDiv.appendChild(priceDiv);
        priceDiv.innerText = `費用：新台幣 ${datas.data[i].price} 元`;
        priceDiv.className = "message";
        // address
        let addressDiv = document.createElement("div");
        inforDiv.appendChild(addressDiv);
        addressDiv.innerText = `地點：${datas.data[i].attraction.address}`;
        addressDiv.className = "message";
        // delete
        let deleteDiv = document.createElement("div");
        deleteDiv.className = "deleteImage";
        let ID = document.createElement("div");
        ID.className = "attractionID";
        ID.textContent = datas.data[i].attraction.id;
        inforDiv.appendChild(deleteDiv);
        inforDiv.appendChild(ID);
        // update amount    
        amount += datas.data[i].price;
    }
    // 計算總價
    confirmAmount.innerText = `總價：新台幣 ${amount} 元`
    // 點擊垃圾桶刪除商品
    const attractionID = document.querySelectorAll(".attractionID")
    attractionID.forEach(id => {
        id.addEventListener("click", deleteCart)
    })
    // 點擊景點圖片連結景點介紹頁面
    const itemId = document.querySelectorAll(".cartItemId")
    itemId.forEach(id => {
        id.addEventListener("click", (elem)=>{
            window.location.href = "/attraction/" + elem.target.textContent;})
    })
}

// 回首頁
homePage.addEventListener("click", ()=>{
    window.location.href = "/";
})

function deleteCart(elem){
    let attractionId = elem.target.textContent;
    let requestBody= {"attractionId" : attractionId}
    console.log(requestBody);
    let url = "/api/booking";
    fetch(url,{
        method : "DELETE",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
        return response.json();
    }).then(function(Data){
        if(Data.ok){
            location.reload();
        }
    })
}