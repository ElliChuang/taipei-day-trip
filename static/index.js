// let page = 0
// let url = "http://127.0.0.1:3000/api/attractions?page="+ page
// fetch(url).then(function(response){
//     return response.json();
// }).then(function(datas){
//     getData(datas)
// })



// 設定 Infinite Scrolling 條件
let options = {
    root: null,
    rootMargins: "0px",
    threshold: 0.5
};

// 製作鈴鐺：建立一個 intersection observer，帶入設定條件＋要執行的函式
const observer = new IntersectionObserver(Intersect, options);

// 設定觀察對象
observer.observe(document.querySelector(".footer"));  

// 符合設定條件下，目標進入或離開 viewport 時觸發此函式
let isLoading = false;
function Intersect(entries) {
    console.log(entries);
    entries.forEach(entry =>{
        if (!entry.isIntersecting && page === null) {
            observer.unobserve(entry.target);
            console.log("closed");
        }else if(entry.isIntersecting && isLoading === false){
            console.warn("something is intersecting with the viewport");
            getData();
            console.log(`載入第${page+1}頁`);

        }
    })
}

let keyword = "";
let page = 0;
function getData() {
    let main = document.querySelector(".main")
    console.log("fetch some JSON data");
    isLoading = true;
    console.log("isLoading:", isLoading)
    fetch(`http://127.0.0.1:3000/api/attractions?page=${page}&keyword=${keyword}`)
        .then((response) => {
            if(response.ok){
                return response.json();
            }else{
                throw Error('status response was not ok.');
            }
            })
        .then(datas => {
            let dataLength = datas.data.length;
            for(i = 0; i < dataLength; i += 1){ 
                let teamDiv = document.createElement("div");
                teamDiv.className = "team";
                let photoDiv = document.createElement("div");
                photoDiv.className = "photo";
                let titleDiv = document.createElement("div");
                titleDiv.className = "title";
                let subtitleDiv = document.createElement("div");
                subtitleDiv.className = "subtitle";
                let mrtDiv = document.createElement("div");
                mrtDiv.className = "MRT";
                let categoryDiv = document.createElement("div");
                categoryDiv.className = "category";
                main.appendChild(teamDiv);
                teamDiv.appendChild(photoDiv);
                teamDiv.appendChild(titleDiv);
                teamDiv.appendChild(subtitleDiv);
                subtitleDiv.appendChild(mrtDiv);
                subtitleDiv.appendChild(categoryDiv);
                // img
                let img = document.createElement("img");
                img.className = "img";
                img.src = datas.data[i]['images'][0];
                photoDiv.appendChild(img);
                // title
                let name = document.createTextNode(datas.data[i]['name']);
                let text = name.cloneNode(true);
                titleDiv.appendChild(text);
                // MRT
                let nameMrt = document.createTextNode(datas.data[i]['mrt']);
                let textMrt = nameMrt.cloneNode(true);
                mrtDiv.appendChild(textMrt);
                // category
                let category = document.querySelectorAll(".category");
                let nameCategory = document.createTextNode(datas.data[i]['category']);
                let textCategory = nameCategory.cloneNode(true);
                categoryDiv.appendChild(textCategory);      
            };
        page = datas.nextpage;
        isLoading = false;
        console.log("isLoading:", isLoading);
        })
        .catch((error) => console.log(error))
    }



// function getData(datas){
//     let dataLength = datas.data.length;
//     for(i = 0; i < dataLength; i += 1){ 
//         // img               
//         let photo = document.querySelectorAll(".photo");
//         let img = document.createElement("img");
//         img.src = datas.data[i]['images'][0];
//         img.className = "img"
//         let imgClone = img.cloneNode(true);
//         photo[i].appendChild(imgClone);  
//         // tilte
//         let title = document.querySelectorAll(".title");
//         let name = document.createTextNode(datas.data[i]['name']);
//         let text = name.cloneNode(true);
//         title[i].appendChild(text);
//         // MRT
//         let MRT = document.querySelectorAll(".MRT");
//         let nameMrt = document.createTextNode(datas.data[i]['mrt']);
//         let textMrt = nameMrt.cloneNode(true);
//         MRT[i].appendChild(textMrt);
//         // category
//         let category = document.querySelectorAll(".category");
//         let nameCategory = document.createTextNode(datas.data[i]['category']);
//         let textCategory = nameCategory.cloneNode(true);
//         category[i].appendChild(textCategory);
//     }   
// }







// 抓取分類資料
let searchBar = document.querySelector(".searchBar");
let input= document.getElementById("input");

let categoryUrl = "http://127.0.0.1:3000/api/categories";
fetch(categoryUrl).then(response => {
    if(response.ok){
        return response.json();
    }else{
        throw Error('status response was not ok.');
    }
}).then(datas => {
    for(i=0; i < datas.data.length; i += 1){
        let barDiv = document.createElement("div");
        searchBar.appendChild(barDiv);
        barDiv.className = "searchBartag";
        barDiv.setAttribute("onclick", "select(this)");
        let category = document.createTextNode(datas.data[i]);
        let textCategory = category.cloneNode(true);
        barDiv.appendChild(textCategory);
    }
}).catch((error) => console.log(error))

// 將類別帶入 search bar
function select(elem){  
    let selectData = elem.textContent;
    input.value = selectData; 
}

// 顯示or隱藏清單
document.addEventListener("click", show)  //所有元件新增click事件
function show(elem){
    if(elem.target.id !== "input"){
        searchBar.style.visibility="hidden";
    }else{
        searchBar.style.visibility="visible";
    }
}

