# === ГЛАВНЫЙ ФАЙЛ LAVA ===
out gui.bold(gui.gold("=== ПРИВЕТ ИЗ LAVASCRIPT ==="))

# Безопасный запрос батареи
let b_data = termux.battery()
let percent = val.get(b_data, "percentage", "N/A")
out "Заряд устройства: " + val.str(percent) + "%"

out "Система: " + sys.platform

# Геометрия
let radius = 12
let res = math.pi * math.pow(radius, 2)
out "Площадь круга (r=12): " + val.str(res)

out gui.bold(gui.red("LAVA IS HOT"))
