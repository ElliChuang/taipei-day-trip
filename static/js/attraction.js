const morningPrice = document.querySelector(".morningPrice");
const afternoonPrice = document.querySelector(".afternoonPrice");
const nameDiv = document.querySelector(".name");
const categoryAndMrtDiv = document.querySelector(".categoryAndMrt");
const descriptionP = document.querySelector(".description");
const addressP = document.querySelector(".address");
const transportP= document.querySelector(".transport");
const photoDiv = document.querySelector(".photo");
const dotsDiv = document.querySelector(".dots");
const prev = document.querySelector(".prev");
const next = document.querySelector(".next");
const morning = document.getElementById("morning");
const afternoon = document.getElementById("afternoon");

// 取得景點 id
let url = location.href;
let attractionId = url.split("attraction/")[1];

// 設定滑動圖片index
let slideIndex = 1;

getData(showData)

function getData(callback) {    
    console.log("fetch some JSON data");
    fetch(`/api/attraction/${attractionId}`)
        .then((response) => {
            if(response.ok){
                return response.json();
            }else{
                throw new Error(`An error occurred:${response.status}`);
            }
        })
        .then((datas) => {
            callback(datas);
        })
        .catch((error) => console.log(error))
    }


function showData(datas){
    // name
    let name = document.createTextNode(datas.data['name']);
    let textName = name.cloneNode(true);
    nameDiv.appendChild(textName);
    // category at MRT 
    let categoryAndMrt = document.createTextNode(datas.data['mrt'] + " at " + datas.data['category']);
    let textCategoryAndMrt = categoryAndMrt.cloneNode(true);
    categoryAndMrtDiv.appendChild(textCategoryAndMrt);
    // description
    let description = document.createTextNode(datas.data['description']);
    let textDescription = description.cloneNode(true);
    descriptionP.appendChild(textDescription);
    // address
    let address = document.createTextNode(datas.data['address']);
    let textAddress = address.cloneNode(true);
    addressP.appendChild(textAddress);
    // transport
    let transport = document.createTextNode(datas.data['transport']);
    let textTransport = transport.cloneNode(true);
    transportP.appendChild(textTransport);
    // img
    let imgLength = datas.data['images'].length;
    for(i = 0; i < imgLength; i += 1){
        let img = document.createElement("img");
        img.className = "img";
        img.src = datas.data['images'][i];
        photoDiv.appendChild(img);
        let dot = document.createElement("span");
        dot.className = "dot";
        dot.setAttribute("onclick", `currentSlide(${i})`);
        dotsDiv.appendChild(dot);
    }
    showSlides(slideIndex);
}


// guide fee
morning.addEventListener("click", ()=>{
    morningPrice.style.display = "block";
    afternoonPrice.style.display = "none";
})

afternoon.addEventListener("click", ()=>{
    morningPrice.style.display = "none";
    afternoonPrice.style.display = "block";
})

// dot control
function currentSlide(n){
    slideIndex = n + 1;
    showSlides(slideIndex);
}

// plus or minus slide
prev.addEventListener("click", plusSlides)
next.addEventListener("click", plusSlides)
function plusSlides(elem){
    if(elem.target.className === "next") {
        slideIndex += 1;
    }else{
        slideIndex += -1;
    }
    showSlides(slideIndex);
}

function showSlides(n) {
    let img = document.querySelectorAll(".img");
    let dot = document.querySelectorAll("span");
    if (n > img.length){slideIndex = 1}
    if (n < 1){slideIndex = img.length}
    for (i = 0; i < img.length; i++) {
      img[i].style.display = "none";
      dot[i].className = "dot";
    }
    img[slideIndex-1].style.display = "block";
    dot[slideIndex-1].className = "dotSlides";
  }