function get_prod() {
    let word = document.getElementById("product-search").value;
    fetch('http://127.0.0.1:5000/product_search?word=' + word, {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
    })
    .catch(error => {
        console.error('Произошла ошибка при отправке запроса:', error);
    });
}