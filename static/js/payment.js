const confirmButton = document.querySelector('.confirmButton');
import {showNoticeWindow, closeNoticeWindow} from "./notice.js"
import {name, email, phone, amount, trip} from "./booking.js"
import {goToHomePage} from "./auth.js"

// 設定參數
const appID = 126869;
const appKey = "app_5QdSI00at1u9WRcyl0RFSAnRuMTZR2tTiErn42VK9oeXRO3rER8RVv7drDtc";
const serverType = "sandbox";
TPDirect.setupSDK(appID, appKey, serverType)

// 設定card樣式
const fields = {
    number: {
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: '#card-expiration-date',
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'black'
        },
        'input.ccv': {
            'font-weight' : '500',
            'font-size' : '16px'
        },
        'input.expiration-date': {
            'font-weight' : '500',
            'font-size' : '16px'
        },
        'input.card-number': {
            'font-weight' : '500',
            'font-size' : '16px'
        },
        ':focus': {
            'color': 'black'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
    },
})

// 取得卡片輸入狀態
TPDirect.card.onUpdate(function (update) {
    if (update.canGetPrime) {
      confirmButton.removeAttribute('disabled')
    } else {
      confirmButton.setAttribute('disabled', true)
    }
})

let primeOfRequestBody = {"prime" : ""};
confirmButton.addEventListener("click", () => {
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    // 卡片號碼錯誤
    if (tappayStatus.status.number !== 0) {
        showNoticeWindow("錯誤訊息", "卡片號碼有誤", closeNoticeWindow);
        return
    }
    // 過期時間錯誤
    if (tappayStatus.status.expiry !== 0) {
        showNoticeWindow("錯誤訊息", "過期時間有誤", closeNoticeWindow);
        return
    }
    // 驗證碼錯誤
    if (tappayStatus.status.ccv !== 0) {
        showNoticeWindow("錯誤訊息", "驗證密碼有誤", closeNoticeWindow);
        return
    }
    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            showNoticeWindow("錯誤訊息", result.msg, closeNoticeWindow);
            return
        }
        let prime = result.card.prime;
        primeOfRequestBody.prime = prime;
        sumbitPrime();
    })
})


function sumbitPrime(){
    let url = "/api/orders";
    let requestBody = {
        "prime" : primeOfRequestBody.prime,
        "order" : {
            "amount" : amount.price, 
            "trip" : trip,
            "contact" : {
                "name" : name.value,
                "email" : email.value,
                "phone" : phone.value,
            }
        },
    };
    fetch(url,{
        method : "POST",
        headers : {"content-type" : "application/json"},
        body : JSON.stringify(requestBody)
    }).then(function(response){
            return response.json();
    }).then(function(datas){
        if (datas.error){
            showNoticeWindow("錯誤訊息", datas.data, closeNoticeWindow);
        }else if (datas.data.payment.message === "付款成功"){
            const number = datas.data.number;
            window.location.href = "/thankyou?number=" + number;
        }else if (datas.data.payment.message === "付款失敗"){
            showNoticeWindow("交易失敗", "信用卡付款失敗，請重新下單", goToHomePage);
        }
    })
}

