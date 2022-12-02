let morningPrice = document.querySelector(".morningPrice");
let afternoonPrice = document.querySelector(".afternoonPrice");
let nameDiv = document.querySelector(".name");
let categoryAndMrtDiv = document.querySelector(".categoryAndMrt");
let descriptionP = document.querySelector(".description");
let addressP = document.querySelector(".address");
let transportP= document.querySelector(".transport");
let photoDiv = document.querySelector(".photo");
let dotsDiv = document.querySelector(".dots");

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
function morning(){
    morningPrice.style.display = "block";
    afternoonPrice.style.display = "none";
}
function afternoon(){
    morningPrice.style.display = "none";
    afternoonPrice.style.display = "block";
}

// dot control
function currentSlide(n){
    slideIndex = n + 1;
    showSlides(slideIndex);
}

// plus or minus slide
function plusSlides(n){
    slideIndex += n;
    showSlides(slideIndex);
}

function showSlides(n) {
    let img = document.querySelectorAll(".img");
    let dot = document.querySelectorAll("span");
    console.log(dot)
    if (n > img.length){slideIndex = 1}
    if (n < 1){slideIndex = img.length}
    for (i = 0; i < img.length; i++) {
      img[i].style.display = "none";
      dot[i].className = "dot";
    }
    img[slideIndex-1].style.display = "block";
    dot[slideIndex-1].className = "dotSlides";
  }