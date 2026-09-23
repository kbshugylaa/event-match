function openLogin() {
    document.getElementById("loginModal").style.display = "flex";
}

function closeLogin() {
    document.getElementById("loginModal").style.display = "none";
}

function sendCode() {

    const phone = document.getElementById("phone").value.trim();

    if (phone.length < 10) {
        alert("Введите корректный номер телефона.");
        return;
    }

    document.getElementById("phoneStep").style.display = "none";
    document.getElementById("codeStep").style.display = "block";

    document.getElementById("phoneDisplay").innerText =
        "+7 " + phone;
}


function verifyCode() {

    const code = document.getElementById("code").value.trim();

    if (code !== "1234") {
        alert("Неверный код. Для демо используйте 1234.");
        return;
    }

    closeLogin();

    document.getElementById("hero").style.display = "none";
    document.querySelector(".section").style.display = "none";
    document.querySelector(".navbar").style.display = "none";

    document.getElementById("searchPage").style.display = "block";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function backToPhone() {

    document.getElementById("codeStep").style.display = "none";
    document.getElementById("phoneStep").style.display = "block";
}


/*
    DEMO DATA

    Позже сюда можно подключить
    hackathon-dataset-anonymized.jsonl
*/

const contractors = [

    {
        name: "Айдос",
        category: "Ведущий",
        city: "Алматы",
        price: 120000,
        events: ["Той", "Свадьба", "Корпоратив"],
        languages: ["Русский", "Казахский"],
        hours: 6,
        busy: ["2026-11-20"],
        description: "Ведущий свадеб, тоев и корпоративов."
    },

    {
        name: "Данияр",
        category: "Ведущий",
        city: "Алматы",
        price: 150000,
        events: ["Той", "Юбилей"],
        languages: ["Казахский"],
        hours: 5,
        busy: ["2026-11-14"],
        description: "Казахскоязычный ведущий для тоев и юбилеев."
    },

    {
        name: "Мадина",
        category: "Фотограф",
        city: "Алматы",
        price: 100000,
        events: ["Свадьба", "Той", "День рождения"],
        languages: ["Русский", "Казахский"],
        hours: 8,
        busy: [],
        description: "Фотограф мероприятий и свадеб."
    },

    {
        name: "Арман",
        category: "Фотограф",
        city: "Алматы",
        price: 180000,
        events: ["Свадьба", "Корпоратив"],
        languages: ["Русский"],
        hours: 10,
        busy: ["2026-11-14"],
        description: "Свадебный и корпоративный фотограф."
    },

    {
        name: "Гүлмира",
        category: "Флорист",
        city: "Алматы",
        price: 70000,
        events: ["Свадьба", "Той", "Юбилей"],
        languages: ["Казахский", "Русский"],
        hours: null,
        busy: [],
        description: "Флористика и оформление мероприятий."
    },

    {
        name: "Decor Lab",
        category: "Декоратор",
        city: "Астана",
        price: 140000,
        events: ["Свадьба", "Корпоратив"],
        languages: ["Русский"],
        hours: null,
        busy: [],
        description: "Декор свадеб и корпоративных мероприятий."
    }

];


function findContractors() {

    const city = document.getElementById("city").value;
    const date = document.getElementById("date").value;
    const event = document.getElementById("event").value;
    const category = document.getElementById("category").value;
    const budget = Number(document.getElementById("budget").value);
    const hoursValue = document.getElementById("hours").value;
    const hours = hoursValue ? Number(hoursValue) : null;
    const language = document.getElementById("language").value;

    let candidates = contractors.filter(c =>
        c.city === city &&
        c.category === category
    );

    if (candidates.length === 0) {

        showEmpty(
            "В этом городе такой категории нет",
            `В городе «${city}» пока нет подрядчиков категории «${category}» в каталоге.`
        );

        return;
    }


    /*
        Проверяем дату
    */

    let free = candidates.filter(c =>
        !c.busy.includes(date)
    );


    /*
        Проверяем бюджет
    */

    let budgetCandidates = free.filter(c =>
        c.price <= budget
    );


    /*
        Проверяем формат
    */

    let eventCandidates = budgetCandidates.filter(c =>
        c.events.includes(event)
    );


    /*
        Проверяем язык
    */

    let finalCandidates = eventCandidates.filter(c => {

        if (!language) return true;

        return c.languages.includes(language);

    });


    /*
        Проверяем длительность
    */

    if (hours !== null) {

        finalCandidates = finalCandidates.filter(c => {

            if (c.hours === null) return true;

            return c.hours >= hours;

        });

    }


    /*
        Сценарий без результатов
    */

    if (finalCandidates.length === 0) {

        let reasons = [];

        if (free.length === 0) {
            reasons.push(`все ${candidates.length} кандидата заняты на выбранную дату`);
        }

        if (free.length > 0 && budgetCandidates.length === 0) {
            reasons.push("ни один свободный кандидат не проходит по бюджету");
        }

        if (budgetCandidates.length > 0 && eventCandidates.length === 0) {
            reasons.push(`ни один кандидат не работает с форматом «${event}»`);
        }

        if (eventCandidates.length > 0 && language) {
            reasons.push(`нет кандидата, работающего на языке «${language}»`);
        }

        if (reasons.length === 0) {
            reasons.push("кандидаты не проходят по заданным условиям");
        }

        showEmpty(
            "Подходящих подрядчиков не найдено",
            reasons.join(". ") + "."
        );

        return;
    }


    /*
        Детерминированное ранжирование
    */

    finalCandidates.sort((a, b) => {

        const scoreA = calculateScore(
            a,
            budget,
            event,
            language,
            hours
        );

        const scoreB = calculateScore(
            b,
            budget,
            event,
            language,
            hours
        );

        if (scoreB !== scoreA) {
            return scoreB - scoreA;
        }

        return a.name.localeCompare(b.name);

    });


    const selected = finalCandidates.slice(0, 3);

    renderResults(
        selected,
        budget,
        event,
        language,
        hours,
        date
    );
}


function calculateScore(
    contractor,
    budget,
    event,
    language,
    hours
) {

    let score = 0;

    /*
        Чем ближе цена к бюджету,
        тем выше score
    */

    if (contractor.price <= budget) {

        const priceRatio =
            contractor.price / budget;

        score += Math.round(priceRatio * 30);

    }

    if (contractor.events.includes(event)) {
        score += 30;
    }

    if (language &&
        contractor.languages.includes(language)) {

        score += 20;

    }

    if (hours !== null &&
        (contractor.hours === null ||
         contractor.hours >= hours)) {

        score += 20;

    }

    return score;
}


function renderResults(
    candidates,
    budget,
    event,
    language,
    hours,
    date
) {

    const results = document.getElementById("results");

    results.innerHTML = `
        <div class="result-title">
            <h2>Подобрали ${candidates.length} подрядчика</h2>
            <p>Порядок определён соответствием условиям вашего запроса.</p>
        </div>
    `;


    candidates.forEach(c => {

        let reasons = [];

        if (c.price <= budget) {

            reasons.push(
                `цена от ${formatPrice(c.price)} ₸ укладывается в ваш бюджет ${formatPrice(budget)} ₸`
            );

        }

        if (c.events.includes(event)) {

            reasons.push(
                `работает с форматом «${event}»`
            );

        }

        if (language &&
            c.languages.includes(language)) {

            reasons.push(
                `работает на языке «${language}»`
            );

        }

        if (
            hours !== null &&
            c.hours !== null &&
            c.hours >= hours
        ) {

            reasons.push(
                `может работать до ${c.hours} ч., что покрывает ваши ${hours} ч.`
            );

        }

        if (c.hours === null) {

            reasons.push(
                "работа не привязана к количеству часов на площадке"
            );

        }


        const reasonText =
            reasons.slice(0, 2).join("; ") + ".";


        results.innerHTML += `

            <div class="result-card">

                <div class="result-top">

                    <div class="result-avatar">
                        ${c.name.charAt(0)}
                    </div>

                    <div class="result-name">

                        <b>${c.name}</b>

                        <span>
                            ${c.category} · ${c.city}
                        </span>

                    </div>

                    <div class="price">
                        от ${formatPrice(c.price)} ₸
                    </div>

                </div>


                <div class="explanation">

                    <b>Почему здесь?</b>

                    <p>
                        ${reasonText}
                    </p>

                </div>

            </div>

        `;

    });

}


function showEmpty(title, text) {

    const results =
        document.getElementById("results");

    results.innerHTML = `

        <div class="empty">

            <h3>${title}</h3>

            <p>${text}</p>

        </div>

    `;
}


function formatPrice(number) {

    return new Intl.NumberFormat("ru-RU")
        .format(number);

}
