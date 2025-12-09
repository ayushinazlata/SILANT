document.addEventListener("DOMContentLoaded", function () {

    if (window.innerWidth > 768) return;

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

        // если строк нет → выходим
        if (rows.length === 0) return;

        // если первая строка содержит "Данных не найдено" → выходим
        if (rows[0].innerText.includes("Данных не найдено")) return;

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
                tbodyMobile.children[i].appendChild(td);
            });
        });

        mobileTable.appendChild(tbodyMobile);
        mobileWrapper.appendChild(mobileTable);

        wrapper.insertAdjacentElement("afterend", mobileWrapper);
    }
});
