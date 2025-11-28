"""
Unit-test для формы авторизации на Яндексе (https://passport.yandex.ru/auth/)

Цель теста:
- Убедиться, что страница авторизации загружается корректно.
- Проверить наличие ключевых элементов формы входа.
- Продемонстрировать использование Selenium для эмуляции пользовательских сценариев.

Важно:
Яндекс активно защищается от автоматизации (CAPTCHA, динамические формы, блокировка Selenium).
Поэтому тест фокусируется на проверке загрузки страницы и основных элементов,
а не на полной авторизации (которая требует 2FA, SMS и невозможна в автоматическом режиме).
"""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class TestYandexAuth(unittest.TestCase):

    def setUp(self):
        """Настройка браузера перед тестом"""
        options = Options()
        # options.add_argument("--headless")  # закомментировано для отладки
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        # Скрываем факт использования Selenium (обход защиты Яндекса)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Используем chromedriver из папки проекта
        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
        if not os.path.exists(driver_path):
            self.skipTest(f"chromedriver.exe не найден по пути: {driver_path}")

        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Закрытие браузера после теста"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_yandex_auth_form_loads(self):
        """
        Проверка: форма авторизации Яндекса загружается и содержит основные элементы.
        """
        self.driver.get("https://passport.yandex.ru/auth/")

        # Проверка заголовка
        title = self.driver.title
        self.assertTrue(
            "Авторизация" in title or "Яндекс" in title,
            f"Неожиданный заголовок: {title}"
        )

        try:
            # Ждём любое поле ввода (даже если скрыто)
            input_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
            self.assertIsNotNone(input_field, "Не найдено ни одного поля ввода")

            # Ждём кнопку "Войти"
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'], button[data-t*='next']"))
            )
            self.assertIsNotNone(login_button, "Кнопка 'Войти' не найдена")

        except Exception as e:
            self.fail(f"Форма авторизации не загрузилась: {e}")


if __name__ == '__main__':
    unittest.main()