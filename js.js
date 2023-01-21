function openPopup(){
    popupp.classList.remove("openpopup");
    popup.classList.toggle("openpopup");
}

function openPopupp(){
    popup.classList.remove("openpopup");
    popupp.classList.toggle("openpopup");
    var user = document.getElementById("username").value;
    
}

function btn(n){
    for(let i=1;i<11;i++){
        var col = document.getElementById("color"+i).style.borderColor;
        document.getElementById("color"+i).style.backgroundColor = col;
    }
    var col = document.getElementById("color"+n).style.backgroundColor;
    document.getElementById("username").value = n;
    document.getElementById("color"+n).style.color = col;
    document.getElementById("color"+n).style.backgroundColor = "#222";
}

function noChange(){
    document.getElementById("username").value = 0;
}