# Очистка экрана (теперь работает!)
sys.clear()

out gui.bold(gui.gold("=== ПРИВЕТ ИЗ LAVASCRIPT ==="))

# Безопасная проверка батареи
let b = termux.battery()
let p = val.get(b, "percentage", "N/A")
out "Заряд: " + val.str(p) + "%"

out "Система: " + sys.platform

# Проверка строк
let text = "lava is hot"
out val.upper(text)

# Математика
let r = 12
let area = math.pi * math.pow(r, 2)
out "Площадь круга: " + val.str(area)
