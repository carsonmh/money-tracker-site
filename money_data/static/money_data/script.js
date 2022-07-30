var buttonElement = document.getElementById("buttonElement");
var formElement = document.getElementById("formElement");

function showForm (){
    formElement.style.display = "block";
    buttonElement.style.display = "none";
}

function hideForm (){
    formElement.style.display = "none";
    buttonElement.style.display = "block";
}