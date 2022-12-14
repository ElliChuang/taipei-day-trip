const searchBarList = document.querySelector(".searchBarList");
const searchInput= document.getElementById("searchInput");
const submit = document.getElementById("submit");
const main = document.querySelector(".main")
let keyword = "";
let page = 0;
let isLoading = false;

let options = {
    root: null,
    rootMargins: "0px",
    threshold: 0.5
};

const observer = new IntersectionObserver(Intersect, options);
const target = document.querySelector(".footer");
observer.observe(target); 
function Intersect(entries) {
    entries.forEach(entry =>{
        if (entry.isIntersecting && isLoading === false && page !== null){
            getData(showData);
        }else if(!entry.isIntersecting && page === null){
            observer.unobserve(entry.target);
        }
    })
} 


function getData(callback) {    
    isLoading = true;
    fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
        .then((response) => {
            if(response.ok){
                return response.json();
            }else{
                throw new Error(`An error occurred:${response.status}`);
            }
        })
        .then((datas) => {
            if (datas.data.length === 0){
                main.innerText = "無篩選結果";
                observer.unobserve(target);
            }else{
                callback(datas);
            }
        })
        .catch((error) => console.log(error))
    }

getData(showData)

function showData(datas){
    let dataLength = datas.data.length;
    for(i = 0; i < dataLength; i += 1){ 
        let teamDiv = document.createElement("div");
        teamDiv.className = "team";
        let teamChildDiv = document.createElement("div");
        teamChildDiv.className = "teamChild";
        teamChildDiv.textContent = datas.data[i]['id'];
        teamChildDiv.setAttribute("onclick", "showAttraction(this)");
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
        teamDiv.appendChild(teamChildDiv);
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
        let nameCategory = document.createTextNode(datas.data[i]['category']);
        let textCategory = nameCategory.cloneNode(true);
        categoryDiv.appendChild(textCategory);  

    }
    isLoading = false;
    page = datas.nextpage
}


// 依關鍵字搜尋
submit.addEventListener("click", function keywordSearch(){
    keyword = searchInput.value;
    page = 0;
    removeDiv();
    observer.observe(target)
    getData(showData);
})

// 移除已建立的 div
function removeDiv(){
    let teamDiv = document.querySelectorAll(".team");
    let photoDiv = document.querySelectorAll(".photo");
    let titleDiv = document.querySelectorAll(".title");
    let subtitleDiv = document.querySelectorAll(".subtitle");
    let MRTDiv = document.querySelectorAll(".MRT");
    let categoryDiv = document.querySelectorAll(".category");
    for (i=0; i < teamDiv.length; i +=1 ){
        subtitleDiv[i].removeChild(MRTDiv[i]);
        subtitleDiv[i].removeChild(categoryDiv[i]);
        teamDiv[i].removeChild(subtitleDiv[i]);
        teamDiv[i].removeChild(titleDiv[i]);
        teamDiv[i].removeChild(photoDiv[i]);
        main.removeChild(teamDiv[i])
    }
    main.innerText = "";
}


// 抓取分類資料
let categoryUrl = "/api/categories";
fetch(categoryUrl).then(response => {
    if(response.ok){
        return response.json();
    }else{
        throw new Error(`An error occurred:${response.status}`);
    }
}).then(datas => {
    for(i=0; i < datas.data.length; i += 1){
        let barDiv = document.createElement("div");
        searchBarList.appendChild(barDiv);
        barDiv.className = "searchBarTag";
        let category = document.createTextNode(datas.data[i]);
        let textCategory = category.cloneNode(true);
        barDiv.appendChild(textCategory);
        barDiv.setAttribute("onclick", "select(this)");
    }
}).catch((error) => console.log(error))

// 將類別帶入 search bar
function select(elem){  
    let selectData = elem.textContent;
    searchInput.value = selectData; 
}

// 顯示or隱藏清單
document.addEventListener("click", show);  //所有元件新增click事件
function show(elem){
    if(elem.target.id !== "searchInput"){
        searchBarList.style.visibility="hidden";
    }else{
        searchBarList.style.visibility="visible";
    }
}

// 跳轉至指定景點介紹頁面 
function showAttraction(elem){
    let id = elem.textContent;
    document.location.href = "/attraction/" + id 
}
