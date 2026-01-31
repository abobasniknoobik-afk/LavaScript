# 🌋 LavaScript v0.2 - Magma Edition
sys.clear()
out gui.bold(gui.gold("=== ПРИВЕТ ИЗ LAVASCRIPT ==="))

# Проверка системных данных
let my_os = sys.platform
let battery = termux.battery()
out "Система: " + my_os
out "Заряд АКБ: " + val.str(battery["percentage"]) + "%"

# Магия вычислений
let r = 12
let s = math.pi * math.pow(r, 2)
out "Площадь круга с радиусом 12: " + val.str(s)

# Работа с текстом
let msg = "lava is hot"
out gui.green(val.upper(msg))

termux.toast("LavaScript v0.2 успешно запущен!")
