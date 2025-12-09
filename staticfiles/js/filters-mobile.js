document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.querySelector(".home__filters-toggle");
    const content = document.querySelector(".home__filters-content");
    const arrow = document.querySelector(".home__filters-arrow");

    if (toggleBtn && content) {
        toggleBtn.addEventListener("click", () => {
            content.classList.toggle("active");
            arrow.classList.toggle("open");

            // Меняем стрелку
            arrow.textContent = content.classList.contains("active") ? "▾" : "▸";
        });
    }
});
