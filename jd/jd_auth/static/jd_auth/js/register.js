
// кнопка смены формы регистраций
var button_email = document.querySelector(".button-email");
var button_phone = document.querySelector(".button-phone");
var email_form = document.querySelector(".email-form");
var phone_form = document.querySelector(".phone-form");

button_phone.addEventListener("click", function() {
    email_form.classList.add("active")
    phone_form.classList.remove("active")
    button_email.classList.remove("active")
    button_phone.classList.add("active")
})
button_email.addEventListener("click", function() {
    email_form.classList.remove("active")
    phone_form.classList.add("active")
    button_email.classList.add("active")
    button_phone.classList.remove("active")
})



// поле ввода номера телефона
var inp = document.getElementById("id_phone_hidden");
var phone_field = document.getElementById("id_phone");


inp.onclick = function() {
    inp.value = "+";
}

var old = 0;


inp.onkeydown = function(event) {
    var curLen = inp.value.length;

    if (!/^\d$/.test(event.key) && event.key !== "Backspace" && event.key !== "Delete") {
        return false; // Запрещаем ввод нецифровых символов
    }
    if (curLen < old){
        old--;
        return;
    }
    if (curLen == 0) {
        inp.value = "+";
    }
    if (curLen == 2) 
        inp.value = inp.value + "(";
        
    if (curLen == 6)
        inp.value = inp.value + ")-";
        
    if (curLen == 11)
        inp.value = inp.value + "-"; 
        
    if (curLen == 14)
        inp.value = inp.value + "-";  
        
    if (curLen > 16)
        inp.value = inp.value.substring(0, inp.value.length - 1);
        
    old++;
}

function FinalRegister() {
    // приводим номер к виду +79999999999 потому что бэкенд только так принимает номера
    const digits = inp.value.replace(/\D/g, '');
    phone_field.value = "+" + digits;
}