import os

class LavaScript:
    def __init__(self):
        # Здесь мы храним переменные
        self.variables = {}

    def run(self):
        file_path = "main.ls"
        if not os.path.exists(file_path):
            print("🌋 Ошибка: Файл main.ls не найден!")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith("#"):
                    continue

                # Команда TYPE (печать текста или переменной)
                if line.startswith("type "):
                    content = line[5:].strip()
                    if content.startswith('"') and content.endswith('"'):
                        print(content.strip('"'))
                    else:
                        # Если не в кавычках, ищем переменную
                        print(self.variables.get(content, f"Ошибка: Переменная '{content}' не найдена"))

                # Команда MOLTEN (создание переменной)
                # Синтаксис: molten имя << значение
                elif "molten" in line and "<<" in line:
                    line = line.replace("molten", "").strip()
                    parts = line.split("<<")
                    var_name = parts[0].strip()
                    var_value = parts[1].strip().strip('"')
                    self.variables[var_name] = var_value

if __name__ == "__main__":
    interpreter = LavaScript()
    interpreter.run()
