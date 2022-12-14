function getOrderInfor(){
    let url = "/api/booking";
    fetch(url,{
        method : "GET",
    }).then(function(response){
            return response.json();
    }).then(function(data){
        console.log(data);
    })
}
getOrderInfor()