function performSearch() {
    const query = document.getElementById('search-query').value;
    let searchUrl;
    searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;

    window.location.href = searchUrl;
}

function checkEnter(event) {
    if (event.key === 'Enter') {
        performSearch();
    }
}

// Функция для смены фона в зависимости от времени суток
function setBackground() {
    const hour = new Date().getHours();
    const body = document.body;

    if (hour >= 18 || hour < 6) {
        // Массив с именами файлов для вечерних фонов
        const nightBackgrounds = [
            'icons/wallpapers/background_night1.jpg',
            'icons/wallpapers/background_night2.jpg',
            'icons/wallpapers/background_night3.jpg',
            'icons/wallpapers/background_night4.jpg',
            'icons/wallpapers/background_night5.jpg',
            'icons/wallpapers/background_night6.jpg'
        ];

        // Выбор случайного фона
        const randomIndex = Math.floor(Math.random() * nightBackgrounds.length);
        body.style.backgroundImage = `url('${nightBackgrounds[randomIndex]}')`;
    } else {
        // День (6:00 - 18:00)
        body.style.backgroundImage = "url('background.jpg')";
    }
}

// Вызов функции при загрузке страницы
setBackground();