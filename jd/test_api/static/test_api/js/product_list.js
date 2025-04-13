
// Код подгрузки товаров

var main_conteiner = document.querySelector(".main-box-card")
var link_URL = "http://127.0.0.1:8000/api/v1/products/"
var isLoading = false


function loading_param_path() {
    const user_path = window.location.pathname
    const param_path = user_path.replace("/api/v1", "")
    link_URL += param_path
    main_conteiner.innerHTML = ''
    start_product_set()
}


function error_none_product() {
    // отображает ошибку если товары не найдены
    var conteiner = document.querySelector(".error-text-404")
    conteiner.classList.remove("active")
}



function render_product_card(products) {
    // отрисовывает карточки товаров

    products.forEach(product => {
        const card = `
            <div class="card">
                <div class="card-img">
                    <img src="${product.UrlsImages[0]}" alt="">
                    <p>-${product.sale}</p>
                </div>

                <div class="card-textbox">
                    <p>
                        <span>${product.sale_price}р</span>
                        <span>${product.price}р</span>
                    </p>

                    <p>${product.name}</p>
                </div>

                <button value="${product.id}">в корзину</button>

            </div>
        `

        main_conteiner.insertAdjacentHTML("beforeend", card)
    }) 
}


function sendrequest_fetch(url){
    return fetch(url).then(response => {
        return response.json()
    })
}



function start_product_set() {
    sendrequest_fetch(link_URL)
        .then(data => {
            if (data.results.length == 0){
                error_none_product()
            } else {
                render_product_card(data.results)
                link_URL = data.next
            }
        })
        .catch(err => console.log(err))
}



function add_basket_user(elem) {
    if (token !== "None") {
        const url_basket = "http://127.0.0.1:8000/api/v1/basket/"

        fetch(url_basket, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"product_id": elem.value})
        }).then(response => console.log(response))
    } else {
        console.log("Нет авторизаций")
    }
}

main_conteiner.addEventListener("click", function(event) {
    const target = event.target; 


    if (target.tagName === "BUTTON" && target.textContent === "в корзину") {
        add_basket_user(target); 
    }
});


document.addEventListener("DOMContentLoaded", () => {

    // парсим api товаров

    start_product_set()


    function showMoreCards() {

        if(isLoading || !link_URL) return;

        isLoading = true

        sendrequest_fetch(link_URL)
        .then(data => {
            render_product_card(data.results)
            link_URL = data.next
            isLoading = false
        })
        .catch(err => {
            console.error(err)
            isLoading = false
        })
    }

    window.addEventListener("scroll", () => {
        if (main_conteiner.offsetHeight - 500 <= window.scrollY) {
            showMoreCards()
        }
    })

    // отслеживаем параметры запроса 
    const links = document.querySelectorAll("#link-sort")

    links.forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault()

            const param = link.getAttribute("data-param")
            const [key, value] = param.split("=")
            const url = new URL(window.location.href)

            if (url.searchParams.get(key) != value) {
                url.searchParams.set(key, value)
                history.pushState(null, '', url)
                loading_param_path()
            }
        })
    })
})



