document.addEventListener("DOMContentLoaded", function () {
    const burger = document.getElementById("burgerBtn");
    const menu = document.getElementById("mobileMenu");

    if (!burger || !menu) return;

    burger.addEventListener("click", function () {
        menu.classList.toggle("active");
        burger.classList.toggle("active");
    });
});
