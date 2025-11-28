import unittest
from secretary import get_name, get_directory, add, documents, directories


class TestSecretary(unittest.TestCase):
    def setUp(self):
        """Восстанавливаем исходные данные перед каждым тестом"""
        global documents, directories
        documents[:] = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
            {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
        ]
        directories.clear()
        directories.update({
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        })

    def test_get_name(self):
        test_cases = [
            ("2207 876234", "Василий Гупкин"),
            ("11-2", "Геннадий Покемонов"),
            ("10006", "Аристарх Павлов"),
            ("5455 028765", "Василий Иванов"),
            ("999999", "Документ не найден"),
            ("", "Документ не найден"),
        ]
        for doc_number, expected in test_cases:
            with self.subTest(doc_number=doc_number):
                self.assertEqual(get_name(doc_number), expected)

    def test_get_directory(self):
        test_cases = [
            ("2207 876234", "1"),
            ("11-2", "1"),
            ("10006", "2"),
            ("5455 028765", "1"),
            ("999999", "Полки с таким документом не найдено"),
            ("", "Полки с таким документом не найдено"),
        ]
        for doc_number, expected in test_cases:
            with self.subTest(doc_number=doc_number):
                self.assertEqual(get_directory(doc_number), expected)

    def test_add(self):
        # Тест 1: добавление на существующую полку
        add("passport", "99999", "Новый Пользователь", "1")
        self.assertIn({"type": "passport", "number": "99999", "name": "Новый Пользователь"}, documents)
        self.assertIn("99999", directories["1"])

        # Тест 2: добавление на новую полку (должна создаться)
        add("invoice", "88888", "Ещё Один", "5")
        self.assertIn({"type": "invoice", "number": "88888", "name": "Ещё Один"}, documents)
        self.assertIn("88888", directories["5"])
        self.assertEqual(directories["5"], ["88888"])

        # Тест 3: проверка, что дубликаты разрешены (по условию не запрещены)
        add("passport", "99999", "Тот же Номер", "2")
        self.assertIn({"type": "passport", "number": "99999", "name": "Тот же Номер"}, documents)
        self.assertIn("99999", directories["2"])

