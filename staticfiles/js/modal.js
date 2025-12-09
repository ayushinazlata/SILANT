document.addEventListener("DOMContentLoaded", function () {
    const openButtons = document.querySelectorAll("[data-modal-button]");
    const closeButtons = document.querySelectorAll("[data-modal-close]");
    const modals = document.querySelectorAll(".modal");
  
    // Открытие модалки
    openButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const id = button.getAttribute("data-id");
        const modal = document.querySelector(`.modal[data-modal-target="${id}"]`);
        if (modal) {
          modal.setAttribute("aria-hidden", "false");
        }
      });
    });
  
    // Закрытие модалки
    closeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const modal = button.closest(".modal");
        if (modal) {
          modal.setAttribute("aria-hidden", "true");
        }
      });
    });
  
    // Закрытие по Esc
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        modals.forEach((modal) => modal.setAttribute("aria-hidden", "true"));
      }
    });
  });
  