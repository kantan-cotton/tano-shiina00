
document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".menu-toggle");
    const menu = document.querySelector("#menu");

    if (!button || !menu) return;

    button.addEventListener("click", () => {
        const isOpen = button.getAttribute("aria-expanded") === "true";

        button.setAttribute("aria-expanded", String(!isOpen));
        button.setAttribute(
            "aria-label",
            isOpen ? "メニューを開く" : "メニューを閉じる"
        );

        menu.classList.toggle("is-open", !isOpen);
    });

    document.addEventListener("click", (event) => {
        if (!menu.contains(event.target) &&
            !button.contains(event.target)) {
            menu.classList.remove("is-open");
            button.setAttribute("aria-expanded", "false");
            button.setAttribute("aria-label", "メニューを開く");
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            menu.classList.remove("is-open");
            button.setAttribute("aria-expanded", "false");
            button.setAttribute("aria-label", "メニューを開く");
        }
    });
});
