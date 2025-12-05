import os
import json
from logging import getLogger, StreamHandler, FileHandler, Formatter, ERROR

class FileNotFound(Exception):
    """Файл не знайдено"""

class FileCorrupted(Exception):
    """Файл пошкоджено або нечитабельний"""

def logger(exception_type, mode="console"):
    """
    :exception_type: — тип винятку, який буде логуватися
    :mode: — "console" або "file"
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            log = getLogger(func.__name__)
            log.setLevel(ERROR)
            log.handlers.clear()

            if mode == "console":
                handler = StreamHandler()
            elif mode == "file":
                handler = FileHandler("log.txt", encoding="utf-8")
            else:
                raise ValueError("Невідомий режим логування!")

            formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            log.addHandler(handler)

            try:
                return func(*args, **kwargs)

            except exception_type as e:
                log.error(f"Помилка: {e}")
                raise

        return wrapper

    return decorator

class JSONFileManager:
    def __init__(self, directory="data", filename="data.json"):

        os.makedirs(directory, exist_ok=True)

        self.filepath = os.path.join(directory, filename)

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write("{}")
            raise FileNotFound(f"Файл '{self.filepath}' не існував — створено новий.")

    @logger(FileCorrupted, mode="console")
    def read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            raise FileCorrupted("Не вдалося прочитати JSON-файл.")

    @logger(FileCorrupted, mode="file")
    def write(self, data: dict | list):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception:
            raise FileCorrupted("Не вдалося записати у JSON-файл.")

    @logger(FileCorrupted, mode="file")
    def append(self, new_data: dict | list):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = json.load(f)

            if isinstance(content, list) and isinstance(new_data, list):
                content.extend(new_data)
            elif isinstance(content, list):
                content.append(new_data)
            elif isinstance(content, dict) and isinstance(new_data, dict):
                content.update(new_data)
            else:
                raise FileCorrupted("Некоректний формат JSON для дописування.")

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)

        except Exception:
            raise FileCorrupted("Помилка при дописуванні в JSON-файл.")

try:
    fm = JSONFileManager("storage", "test.json")

    fm.write({"city": "Lviv", "numbers": [1, 2, 4, 3]})
    print("Читання:", fm.read())

    fm.append({"abc": 123})
    print("Після додавання:", fm.read())

except Exception as e:
    print("Виняток:", e)
