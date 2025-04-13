var menu = document.querySelector(".menu")
var button_menu = document.querySelector(".menu-button")

button_menu.addEventListener("click", function() {
    menu.classList.toggle("active")
})


document.getElementById("sort-select").addEventListener("change", function () {
    const selectedValue = this.value; 
    if (selectedValue) {
        window.location.href = selectedValue; 
    }
});