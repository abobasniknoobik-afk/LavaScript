# ТЕСТ v0.2.3
out gui["bold"](gui["green"]("--- ЗАПУСК НОВОГО ТЕСТА ---"))

# Проверка математики
let koren = math["root"](144)
out "Корень: " + val["str"](koren)

# Проверка FS
let mesto = fs["cwd"]()
out "Папка: " + mesto

# Проверка Батареи
let bp = termux["battery"]()
out "Заряд: " + val["str"](bp["percentage"])

out "--- ФИНИШ ---"
