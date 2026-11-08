
document.addEventListener("DOMContentLoaded", async () => {
    const authStatus = document.getElementById("auth-status");
    const userProfile = document.getElementById("user-profile");

    const userName = document.getElementById("user-name");
    const userUsername = document.getElementById("user-username");
    const userCurrency = document.getElementById("user-currency");

    const telegram = window.Telegram?.WebApp;

    // Проверяем, открыто ли приложение через Telegram
    if (!telegram || !telegram.initData) {
        authStatus.textContent =
            "Открой Spendly через Telegram-бота для авторизации.";
        return;
    }

    // Инициализация Telegram Mini App
    telegram.ready();
    telegram.expand();

    try {
        const response = await fetch("/api/auth/telegram", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                initData: telegram.initData
            })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(
                result.error || "Не удалось авторизоваться"
            );
        }

        const user = result.user;

        // Показываем профиль авторизованного пользователя
        userName.textContent =
            `Имя: ${user.first_name} ${user.last_name || ""}`.trim();

        userUsername.textContent = user.username
            ? `Telegram: @${user.username}`
            : "Telegram: не указан";

        userCurrency.textContent =
            `Валюта: ${user.currency}`;

        authStatus.textContent = "Авторизация успешна!";
        userProfile.hidden = false;

    } catch (error) {
        console.error("Ошибка авторизации:", error);

        authStatus.textContent =
            error.message || "Ошибка при авторизации.";
    }
});
