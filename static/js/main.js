document.addEventListener("DOMContentLoaded", function () {
    /* Бургер меню */
    const burger = document.getElementById("burgerBtn");
    const menu = document.getElementById("mobileMenu");

    if (burger && menu) {
        burger.addEventListener("click", function () {
            menu.classList.toggle("active");
            burger.classList.toggle("active");
        });
    }

    /* Раскрытие списка фильтров для мобильных версий */
    document.querySelectorAll(".home__filters-area").forEach((area) => {
        const toggleBtn = area.querySelector(".home__filters-toggle");
        const content = area.querySelector(".home__filters-content");
        const arrow = area.querySelector(".home__filters-arrow");

        if (toggleBtn && content && arrow) {
            toggleBtn.addEventListener("click", () => {
                content.classList.toggle("active");
                arrow.classList.toggle("open");
                arrow.textContent = content.classList.contains("active") ? "▾" : "▸";
            });
        }
    });

    /* Модальное окно */
    const openButtons = document.querySelectorAll("[data-modal-button]");
    const closeButtons = document.querySelectorAll("[data-modal-close]");
    const modals = document.querySelectorAll(".modal");

    /* Открытие */
    openButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const id = button.getAttribute("data-id");
            const modal = document.querySelector(`.modal[data-modal-target="${id}"]`);
            if (modal) {
                modal.setAttribute("aria-hidden", "false");
                document.body.classList.add("body--no-scroll");
            }
        });
    });

    /* Закрытие */
    closeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const modal = button.closest(".modal");
            if (modal) {
                modal.setAttribute("aria-hidden", "true");
                document.body.classList.remove("body--no-scroll");
            }
        });
    });

    /* Закрытие по Esc */
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            modals.forEach((modal) => modal.setAttribute("aria-hidden", "true"));
            document.body.classList.remove("body--no-scroll");
        }
    });

    /* Автоматическое открытие модалки после POST или ошибки */
    const openModal = document.querySelector("#reference-open-modal");
    if (openModal) {
        const openId = openModal.dataset.openId;
        if (openId) {
            const modal = document.querySelector(`.modal[data-modal-target="${openId}"]`);
            if (modal) {
                modal.setAttribute("aria-hidden", "false");
                document.body.classList.add("body--no-scroll");
            }
        }
    }

    /* Трансформирование таблицы для мобильной версии */
    if (window.innerWidth <= 768) {
        const tables = document.querySelectorAll(".home__table");

        tables.forEach((table) => {
            makeMobileTable(table);
        });

        function makeMobileTable(originalTable) {
            const wrapper = originalTable.closest(".home__table-wrapper");
            if (!wrapper) return;

            const thead = originalTable.querySelector("thead");
            const tbody = originalTable.querySelector("tbody");
            if (!thead || !tbody) return;

            const rows = [...tbody.querySelectorAll("tr")];
            if (rows.length === 0) return;

            if (wrapper.querySelector(".empty-data-message")) return;

            const headers = [...thead.querySelectorAll("th")].map(th =>
                th.textContent.trim()
            );

            const mobileWrapper = document.createElement("div");
            mobileWrapper.className = "mobile-table-wrapper";

            const mobileTable = document.createElement("table");
            mobileTable.className = "mobile-table";

            const tbodyMobile = document.createElement("tbody");

            headers.forEach(header => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<th class="mobile-label">${header}</th>`;
                tbodyMobile.appendChild(tr);
            });

            rows.forEach(row => {
                const cells = [...row.querySelectorAll("td")];
                cells.forEach((cell, i) => {
                    const td = document.createElement("td");
                    td.innerHTML = cell.innerHTML;
                    if (tbodyMobile.children[i]) {
                        tbodyMobile.children[i].appendChild(td);
                    }
                });
            });

            mobileTable.appendChild(tbodyMobile);
            mobileWrapper.appendChild(mobileTable);

            wrapper.insertAdjacentElement("afterend", mobileWrapper);
        }
    }

    /* Select2 инициализация */
    if (window.jQuery && $.fn.select2) {
        $('select').select2({
            placeholder: "Выберите...",
            allowClear: true,
            width: 'style',
            dropdownPosition: 'below',
            language: {
                noResults: function () {
                    return "Ничего не найдено";
                },
                searching: function () {
                    return "Поиск...";
                }
            }
        });
    }
});
