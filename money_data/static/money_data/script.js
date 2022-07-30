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

//"location.href='{% url 'money_data:delete_log' m.id %}'"

function trashCanPopUp() {
    blur = document.getElementById('main');
    blur2 = document.getElementById('navbar');
    blur.classList.toggle('active');
    blur2.classList.toggle('active');
    popup = document.getElementById('popup');
    popup.classList.toggle('active');
    console.log(sessionStorage.getItem('id'));
}