<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>EventMatch — умный подбор подрядчиков</title>

    <link rel="stylesheet" href="style.css">
</head>

<body>

<header class="header">

    <div class="logo">
        Event<span>Match</span>
    </div>

    <nav>
        <a href="index.html">Главная</a>
        <a href="demo.html">Демо</a>
    </nav>

    <div class="accessibility">

        <button onclick="changeFont(1)">
            A+
        </button>

        <button onclick="changeFont(-1)">
            A−
        </button>

        <button onclick="toggleTheme()">
            ☾
        </button>

        <button onclick="toggleColorBlind()">
            ◉
        </button>

    </div>

</header>


<main>

<section class="hero">

    <div class="hero-content">

        <div class="badge">
            HACKATHON #79-LITE
        </div>

        <h1>
            Найдите подходящего
            подрядчика для мероприятия
        </h1>

        <p>
            EventMatch анализирует каталог подрядчиков
            и объясняет, почему каждый кандидат подходит
            именно под ваш запрос.
        </p>

        <a href="#search" class="main-button">
            Подобрать подрядчика →
        </a>

    </div>

</section>


<section id="search" class="search-section">

    <div class="section-title">

        <span>УМНЫЙ ПОДБОР</span>

        <h2>
            Параметры мероприятия
        </h2>

        <p>
            Выберите условия заказа.
            Мы не расширяем каталог —
            выбираем только из доступных подрядчиков.
        </p>

    </div>


    <div class="search-card">

        <div class="form-grid">

            <div class="form-group">

                <label>
                    Город
                </label>

                <select id="city">

                    <option value="">
                        Выберите город
                    </option>

                    <option value="Алматы">
                        Алматы
                    </option>

                    <option value="Астана">
                        Астана
                    </option>

                    <option value="Зарубежье">
                        Зарубежье
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Дата мероприятия
                </label>

                <input
                    type="date"
                    id="date"
                    min="2026-09-23"
                    max="2026-12-31"
                >

            </div>


            <div class="form-group">

                <label>
                    Тип мероприятия
                </label>

                <select id="eventFormat">

                    <option value="">
                        Выберите формат
                    </option>

                    <option value="свадьба">
                        Свадьба
                    </option>

                    <option value="той">
                        Той
                    </option>

                    <option value="корпоратив">
                        Корпоратив
                    </option>

                    <option value="конференция">
                        Конференция
                    </option>

                    <option value="юбилей">
                        Юбилей
                    </option>

                    <option value="день рождения">
                        День рождения
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Категория
                </label>

                <select id="category">

                    <option value="">
                        Выберите категорию
                    </option>

                    <option value="Ведущий">
                        Ведущий
                    </option>

                    <option value="Фотограф">
                        Фотограф
                    </option>

                    <option value="Видеограф">
                        Видеограф
                    </option>

                    <option value="Декоратор">
                        Декоратор
                    </option>

                    <option value="Флорист">
                        Флорист
                    </option>

                    <option value="Инструменталист">
                        Инструменталист
                    </option>

                    <option value="Подарки и сувениры">
                        Подарки и сувениры
                    </option>

                    <option value="Ведущий церемонии">
                        Ведущий церемонии
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Бюджет, ₸
                </label>

                <input
                    type="number"
                    id="budget"
                    placeholder="Например: 500000"
                >

            </div>


            <div class="form-group">

                <label>
                    Длительность, часов
                    <span class="optional">
                        необязательно
                    </span>
                </label>

                <input
                    type="number"
                    id="hours"
                    min="1"
                    placeholder="Например: 6"
                >

            </div>


            <div class="form-group">

                <label>
                    Язык
                    <span class="optional">
                        необязательно
                    </span>
                </label>

                <select id="language">

                    <option value="">
                        Любой
                    </option>

                    <option value="русский">
                        Русский
                    </option>

                    <option value="казахский">
                        Казахский
                    </option>

                    <option value="английский">
                        Английский
                    </option>

                </select>

            </div>

        </div>


        <button
            class="search-button"
            onclick="findContractors()"
        >
            Найти подходящих →
        </button>

    </div>

</section>


<section class="how">

    <div class="section-title">

        <span>КАК ЭТО РАБОТАЕТ</span>

        <h2>
            Не просто рейтинг
        </h2>

    </div>


    <div class="how-grid">

        <div class="how-card">

            <div class="number">
                01
            </div>

            <h3>
                Фильтруем
            </h3>

            <p>
                Исключаем подрядчиков,
                которые заняты в выбранную дату
                или не соответствуют обязательным условиям.
            </p>

        </div>


        <div class="how-card">

            <div class="number">
                02
            </div>

            <h3>
                Анализируем
            </h3>

            <p>
                Сравниваем бюджет, формат,
                язык, длительность и описание профиля.
            </p>

        </div>


        <div class="how-card">

            <div class="number">
                03
            </div>

            <h3>
                Объясняем
            </h3>

            <p>
                Показываем до трёх кандидатов
                и объясняем конкретно,
                почему каждый попал в выдачу.
            </p>

        </div>

    </div>

</section>

</main>


<footer>

    <strong>EventMatch</strong>

    <p>
        Smart contractor matching for Kazakhstan events.
    </p>

</footer>


<script src="data.js"></script>
<script src="app.js"></script>

</body>
</html>
const contractors = [

    {
        id: "HK-80581",

        anon_name: "Санджи Виндсмок",

        categories: ["Ведущий"],

        city: "Астана",

        city_imputed: false,

        synthetic: false,

        price_from_kzt: 800000,

        price_imputed: false,

        event_formats: [
            "свадьба",
            "той",
            "корпоратив",
            "юбилей"
        ],

        languages: [
            "русский",
            "казахский"
        ],

        max_hours: 8,

        busy_dates: [
            "2026-09-25",
            "2026-09-27",
            "2026-10-02",
            "2026-10-04",
            "2026-10-07"
        ],

        description:
            "Веду разноформатные мероприятия. " +
            "Персональный и креативный подход. " +
            "Большой опыт проведения мероприятий."
    },


    {
        id: "HK-76268",

        anon_name: "Сацуки Кусакабэ",

        categories: ["Фотограф"],

        city: "Алматы",

        city_imputed: false,

        synthetic: false,

        price_from_kzt: 200000,

        price_imputed: false,

        event_formats: [
            "свадьба",
            "той"
        ],

        languages: [
            "русский"
        ],

        max_hours: 10,

        busy_dates: [
            "2026-09-23",
            "2026-09-25",
            "2026-09-27",
            "2026-10-01"
        ],

        description:
            "Свадебный фотограф. " +
            "Люблю живые кадры, настоящие улыбки " +
            "и моменты, которые невозможно повторить."
    },


    {
        id: "HK-77793",

        anon_name: "Спайк Спигел",

        categories: ["Ведущий церемонии"],

        city: "Алматы",

        city_imputed: false,

        synthetic: false,

        price_from_kzt: 200000,

        price_imputed: false,

        event_formats: [
            "свадьба",
            "той"
        ],

        languages: [
            "казахский",
            "русский"
        ],

        max_hours: 3,

        busy_dates: [
            "2026-09-23",
            "2026-09-25",
            "2026-09-30"
        ],

        description:
            "Ведущая и церемониймейстер. " +
            "Ведение на казахском и русском языках."
    }

];
* {
    box-sizing: border-box;
}


html {
    scroll-behavior: smooth;
}


body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f7f7fb;

    color: #181820;

    line-height: 1.5;

    transition:
        background .25s,
        color .25s;

}


a {
    text-decoration: none;
    color: inherit;
}


.header {

    height: 76px;

    background: white;

    border-bottom:
        1px solid #e5e5ec;

    display: flex;

    align-items: center;

    padding:
        0 5%;

    gap: 35px;

    position: sticky;

    top: 0;

    z-index: 100;

}


.logo {

    font-size: 25px;

    font-weight: 800;

    margin-right: auto;

}


.logo span {

    color: #645cff;

}


nav {

    display: flex;

    gap: 25px;

}


nav a {

    color: #656575;

    font-weight: 600;

}


nav a:hover {

    color: #645cff;

}


.accessibility {

    display: flex;

    gap: 6px;

}


.accessibility button {

    border:
        1px solid #dddde6;

    background: white;

    border-radius: 8px;

    padding:
        8px 11px;

    cursor: pointer;

    font-weight: bold;

}


.hero {

    min-height: 600px;

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 70px 25px;

    background:

        radial-gradient(
            circle at 20% 20%,
            #ddd9ff,
            transparent 35%
        ),

        radial-gradient(
            circle at 80% 70%,
            #d8f5ff,
            transparent 35%
        );

}


.hero-content {

    max-width: 950px;

    text-align: center;

}


.badge {

    display: inline-block;

    background: #ebe9ff;

    color: #554be2;

    padding:
        7px 12px;

    border-radius: 50px;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1px;

}


.hero h1 {

    font-size:
        clamp(42px, 7vw, 78px);

    line-height: 1;

    letter-spacing: -3px;

    margin:
        25px 0;

}


.hero p {

    max-width: 700px;

    margin:
        0 auto 35px;

    color: #626271;

    font-size: 19px;

}


.main-button {

    display: inline-block;

    background: #645cff;

    color: white;

    padding:
        15px 25px;

    border-radius: 11px;

    font-weight: 700;

    border: none;

    cursor: pointer;

}


.search-section {

    max-width: 1100px;

    margin:
        auto;

    padding:
        80px 20px;

}


.section-title span {

    color: #645cff;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 2px;

}


.section-title h2 {

    font-size: 38px;

    margin:
        8px 0;

}


.section-title p {

    color: #686877;

}


.search-card {

    background: white;

    border:
        1px solid #e3e3eb;

    border-radius: 22px;

    padding: 30px;

    margin-top: 30px;

}


.form-grid {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 20px;

}


.form-group {

    display: flex;

    flex-direction: column;

    gap: 7px;

}


.form-group label {

    font-weight: 700;

}


.optional {

    color: #92929f;

    font-weight: normal;

    font-size: 12px;

}


select,
input {

    width: 100%;

    padding: 14px;

    border:
        1px solid #dedee7;

    border-radius: 10px;

    background: white;

    font-size: 15px;

}


.search-button {

    width: 100%;

    margin-top: 25px;

    padding: 16px;

    border: none;

    border-radius: 11px;

    background: #645cff;

    color: white;

    font-size: 16px;

    font-weight: 800;

    cursor: pointer;

}


.how {

    max-width: 1100px;

    margin: auto;

    padding:
        50px 20px 100px;

}


.how-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 20px;

    margin-top: 30px;

}


.how-card {

    background: white;

    border:
        1px solid #e3e3eb;

    padding: 28px;

    border-radius: 18px;

}


.number {

    color: #645cff;

    font-weight: 900;

}


.how-card h3 {

    font-size: 21px;

}


.how-card p {

    color: #696976;

}


footer {

    padding: 40px;

    text-align: center;

    background: #17171d;

    color: white;

}


.results-page {

    max-width: 1100px;

    margin: auto;

    padding:
        60px 20px;

}


.results-header {

    margin-bottom: 35px;

}


.results-header span {

    color: #645cff;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 2px;

}


.results-header h1 {

    font-size: 42px;

    margin:
        8px 0;

}


.results-header p {

    color: #6b6b78;

}


.back-button {

    display: inline-block;

    margin-top: 10px;

    color: #645cff;

    font-weight: 700;

}


.results-container {

    display: grid;

    gap: 20px;

}


.result-count {

    padding: 18px;

    background: #efeeff;

    border-radius: 12px;

    color: #4e47c9;

}


.contractor-card {

    background: white;

    border:
        1px solid #e2e2ea;

    border-radius: 20px;

    padding: 25px;

    position: relative;

}


.card-top {

    display: flex;

    justify-content: space-between;

    align-items: center;

}


.position {

    background: #645cff;

    color: white;

    padding:
        6px 10px;

    border-radius: 7px;

    font-weight: bold;

}


.real,
.synthetic {

    padding:
        5px 9px;

    border-radius: 50px;

    font-size: 11px;

    font-weight: bold;

}


.real {

    background: #e5f7ec;

    color: #21854a;

}


.synthetic {

    background: #fff0d7;

    color: #a46300;

}


.avatar {

    width: 65px;

    height: 65px;

    border-radius: 50%;

    background: #e9e7ff;

    color: #5149db;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 22px;

    font-weight: 800;

    margin-top: 20px;

}


.contractor-card h2 {

    margin:
        12px 0 3px;

}


.category {

    color: #645cff;

    font-weight: 700;

}


.location {

    color: #777783;

    margin-top: 7px;

}


.price {

    font-size: 21px;

    font-weight: 800;

    margin:
        18px 0;

}


.why {

    background: #f3f2ff;

    border-radius: 12px;

    padding: 17px;

}


.why h3 {

    margin-top: 0;

}


.why li {

    margin-bottom: 7px;

}


.description {

    margin-top: 18px;

    color: #62626e;

}


.contact-button {

    margin-top: 20px;

    width: 100%;

    padding: 13px;

    border: none;

    background: #645cff;

    color: white;

    border-radius: 10px;

    cursor: pointer;

    font-weight: 700;

}


.empty-result {

    text-align: center;

    background: white;

    border:
        1px solid #e3e3eb;

    border-radius: 20px;

    padding: 60px 30px;

}


.empty-icon {

    font-size: 50px;

}


.empty-result h2 {

    font-size: 28px;

}


.empty-result p {

    max-width: 600px;

    margin:
        15px auto 25px;

    color: #676773;

}


.explanation-section {

    margin-top: 60px;

    background: #17171d;

    color: white;

    padding: 35px;

    border-radius: 18px;

}


.explanation-section p {

    color: #c4c4cc;

}


body.dark {

    background: #101116;

    color: #eeeef5;

}


body.dark .header,
body.dark .search-card,
body.dark .how-card,
body.dark .contractor-card,
body.dark .empty-result {

    background: #191a21;

    border-color: #30313c;

}


body.dark input,
body.dark select {

    background: #191a21;

    color: white;

    border-color: #3a3b46;

}


body.dark .hero {

    background:
        radial-gradient(
            circle at 20% 20%,
            #25214d,
            transparent 35%
        );

}


body.dark .hero p,
body.dark .how-card p,
body.dark .description {

    color: #aaaab8;

}


.colorblind {

    filter:
        saturate(.35)
        contrast(1.15);

}


@media(max-width: 800px) {

    .form-grid,
    .how-grid {

        grid-template-columns: 1fr;

    }


    nav {

        display: none;

    }


    .hero h1 {

        letter-spacing: -1px;

    }

}


@media(max-width: 500px) {

    .header {

        padding:
            0 15px;

    }


    .hero {

        padding:
            50px 18px;

    }


    .search-card {

        padding: 20px;

    }


    .results-header h1 {

        font-size: 32px;

    }

}
