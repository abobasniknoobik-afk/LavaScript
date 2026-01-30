import os

class LavaScript:
    def __init__(self):
        self.variables = {}

    def run(self):
        file_path = "main.ls"
        if not os.path.exists(file_path):
            print("🌋 Ошибка: Файл main.ls не найден!")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue

                # Команда TYPE: теперь может печатать всё
                if line.startswith("type "):
                    expr = line[5:].strip()
                    try:
                        # Пытаемся вычислить выражение (переменную или математику)
                        # Передаем self.variables, чтобы eval видел наши переменные
                        result = eval(expr, {}, self.variables)
                        print(result)
                    except:
                        # Если это просто текст в кавычках
                        print(expr.strip('"'))

                # Команда MOLTEN: теперь считает всё
                elif "molten" in line and "<<" in line:
                    line = line.replace("molten", "").strip()
                    name, expr = line.split("<<")
                    name = name.strip()
                    expr = expr.strip()
                    
                    try:
                        # Вычисляем значение перед сохранением
                        self.variables[name] = eval(expr, {}, self.variables)
                    except Exception as e:
                        print(f"🌋 Ошибка в переменной {name}: {e}")

if __name__ == "__main__":
    LavaScript().run()
