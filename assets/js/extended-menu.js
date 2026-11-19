
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".mobile-menu-toggle");
    const panel = document.querySelector(".mobile-menu-panel");
    const overlay = document.querySelector(".mobile-menu-overlay");
    const closeButton = document.querySelector(".mobile-menu-close");

    if (!toggle || !panel || !overlay || !closeButton) {
        return;
    }

    // メニューを開く
    const openMenu = () => {
        document.body.classList.add("mobile-menu-open");

        toggle.setAttribute("aria-expanded", "true");
        panel.setAttribute("aria-hidden", "false");
        overlay.setAttribute("aria-hidden", "false");

        closeButton.focus();
    };

    // メニューを閉じる
    const closeMenu = () => {
        document.body.classList.remove("mobile-menu-open");

        toggle.setAttribute("aria-expanded", "false");
        panel.setAttribute("aria-hidden", "true");
        overlay.setAttribute("aria-hidden", "true");

        toggle.focus();
    };

    // 開閉ボタン
    toggle.addEventListener("click", () => {
        const isOpen = toggle.getAttribute("aria-expanded") === "true";

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // 閉じるボタン
    closeButton.addEventListener("click", closeMenu);

    // パネル外をクリック
    overlay.addEventListener("click", closeMenu);

    // Escapeキーで閉じる
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" &&
            document.body.classList.contains("mobile-menu-open")) {
            closeMenu();
        }
    });

    // メニュー項目を選択したら閉じる
    panel.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });
});
