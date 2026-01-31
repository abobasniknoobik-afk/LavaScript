# ТЕСТ ДЛЯ v0.2.6
sys.clear()
out gui.bold(gui.green("--- ЗАПУСК ИДЕАЛЬНОГО ТЕСТА ---"))

# 1. Тест математики
let k = math.root(144)
out "Математика (root): " + val.str(k)

# 2. Тест системы
out "ОС: " + sys.platform
out "Дата: " + sys.date()

# 3. Тест путей
let p = fs.path(".")
out "Путь: " + p

# 4. Тест батареи (С ЗАЩИТОЙ)
let b = termux.battery()
let proc = b["percentage"]
out "Заряд: " + val.str(proc) + "%"

# 5. Тест сети
out "Твой IP: " + net.get("https://api.ipify.org")

out gui.bold(gui.gold("--- ТЕСТ ЗАВЕРШЕН БЕЗ ОШИБОК ---"))
