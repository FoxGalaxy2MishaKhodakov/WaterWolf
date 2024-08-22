// Функция для выполнения поиска
function performSearch() {
    const query = document.getElementById('search-query').value;
    let searchUrl;
    searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;

    window.location.href = searchUrl;
}
