const memberName = document.getElementById('memberName');
const main = document.querySelector('.main');
const group = document.getElementById('group');
const table = document.querySelector('.table');
const Orders = document.getElementById('Orders');
const Detail = document.getElementById('Detail');
const noOrderHistory = document.querySelector('.noOrderHistory');
const orderDetail = document.querySelector('.orderDetail');
const orderDetailId = document.querySelector('.orderDetailId');
const orderDetailTotalAmount = document.querySelector('.orderDetailTotalAmount');
import {getStatus} from "./auth.js";
import {showNoticeWindow, closeNoticeWindow} from "./notice.js";

getStatus(checkStatus)
function checkStatus(elem){
    if(elem.data !== null && elem.data.id){
        memberName.innerText = elem.data.name;
        getOrderInfor(checkOrder);
    }else{
        window.location.href = "/";
    }
}

function getOrderInfor(callback){
    let url = "/api/orders";
    fetch(url,{
        method : "GET",
    }).then(function(response){
        return response.json();
    }).then(function(datas){
        callback(datas);
    })
}

function checkOrder(datas){
    if(datas.data !== null && datas.data[0].order_dt){
        main.style.display = "block";
        noOrderHistory.style.display = "none";
        showOrder(datas);
    }else{
        main.style.display = "none";
        noOrderHistory.style.display = "block";
    }
}

function showOrder(datas){
    let dataLength = datas.data.length;
    for(let i = 0; i < dataLength; i +=1){
        let rowTr = document.createElement("tr");
        table.appendChild(rowTr);
        // date
        let dateTd = document.createElement("td");
        rowTr.appendChild(dateTd);
        dateTd.innerText = datas.data[i].order_dt;
        // orderId
        let orderIdTd = document.createElement("td");
        rowTr.appendChild(orderIdTd);
        orderIdTd.innerText = datas.data[i].order_id;
        // status
        let statusTd = document.createElement("td");
        rowTr.appendChild(statusTd);
        statusTd.innerText = datas.data[i].status;
        // price
        let priceTd = document.createElement("td");
        rowTr.appendChild(priceTd);
        priceTd.innerText = datas.data[i].price;
        // detail
        let detailTd = document.createElement("td");
        rowTr.appendChild(detailTd);
        let detailButton = document.createElement("button");
        detailTd.appendChild(detailButton);
        detailButton.className = "checkDetail";
        detailButton.innerText = "查詢";
        detailButton.id = datas.data[i].order_id;
    }
    // 點擊查詢顯示詳細頁面
    const checkButton = document.querySelectorAll(".checkDetail")
    checkButton.forEach(button => {
        button.addEventListener("click", detailPage)
    })  
}

function detailPage(elem){
    let url = "/api/order/" + elem.target.id;
    fetch(url,{
        method : "GET",
    }).then(function(response){
        return response.json();
    }).then(function(datas){
        if(datas.data !== null && datas.data.trip){
            group.style.display = "none";
            orderDetail.style.display = "block";
            Orders.classList.remove("currentPage");
            Detail.classList.add("currentPage");
            showDetail(datas);
        }else{
            showNoticeWindow("錯誤訊息", datas.data, closeNoticeWindow);
        }
    })
}

function showDetail(datas){
    remove();
    orderDetailId.innerText = `訂單編號：${datas.data.number}`;
    orderDetailTotalAmount.innerText = `訂單總額：新台幣${datas.data.total_amount}元`;
    let dataLength = datas.data.trip.length;
    for(let i = 0; i < dataLength; i +=1){
        // item section
        let sectionDiv = document.createElement("div");
        sectionDiv.className = "section";
        orderDetail.appendChild(sectionDiv);
        // img
        let pictureDiv = document.createElement("div");
        pictureDiv.className = "picture";
        let img = document.createElement("img");
        img.className = "cartItemImage";
        img.src = datas.data.trip[i].attraction.image;
        pictureDiv.appendChild(img);
        sectionDiv.appendChild(pictureDiv);
        // infor
        let inforDiv = document.createElement("div");
        sectionDiv.appendChild(inforDiv);
        inforDiv.className = "infor";
        // title
        let titleDiv = document.createElement("div");
        inforDiv.appendChild(titleDiv);
        titleDiv.innerText = `台北一日遊：${datas.data.trip[i].attraction.name}`;
        titleDiv.className = "title";
        // date
        let dateDiv = document.createElement("div");
        inforDiv.appendChild(dateDiv);
        dateDiv.innerText = `日期：${datas.data.trip[i].date}`;
        dateDiv.className = "message";
        // time
        let timeDiv = document.createElement("div");
        inforDiv.appendChild(timeDiv);
        timeDiv.className = "message";
        if(datas.data.trip[i].time === "morning"){
            timeDiv.innerText = "時間：早上９點至下午２點";
        }else if(datas.data.trip[i].time === "afternoon"){
            timeDiv.innerText = "時間：下午１點至下午６點";
        }
        // price
        let priceDiv = document.createElement("div");
        inforDiv.appendChild(priceDiv);
        priceDiv.innerText = `費用：新台幣 ${datas.data.trip[i].price} 元`;
        priceDiv.className = "message";
        // address
        let addressDiv = document.createElement("div");
        inforDiv.appendChild(addressDiv);
        addressDiv.innerText = `地點：${datas.data.trip[i].attraction.address}`;
        addressDiv.className = "message";
    }
}

Orders.addEventListener("click", () => {
    group.style.display = "block";
    orderDetail.style.display = "none";
    Detail.classList.remove("currentPage");
    Orders.classList.add("currentPage");
})

// 移除已建立的訂單明細 div
function remove(){
    const sectionDiv = document.querySelectorAll(".section");
    for (let i = 0; i < sectionDiv.length; i += 1){
        orderDetail.removeChild(sectionDiv[i])
    }   
}