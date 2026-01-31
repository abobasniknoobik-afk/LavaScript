# ТЕСТ ТИТАН v0.5
sys.clear()
out gui.bold(gui.gold("--- ЗАПУСК TITAN ENGINE ---"))

# Математика
let res = math.root(144) + math.pow(2, 3)
out "Math (12+8): " + val.str(res)

# Система
out "Версия: " + sys.ver
out "Аптайм: " + val.str(sys.uptime()) + "s"

# Криптография
let s = crypto.sha256("lava")
out "SHA256: " + s

# Termux
let b = termux.battery()
out "Заряд: " + val.str(b["percentage"]) + "%"

# Обработка текста
let tx = val.upper("lava script")
out "Текст: " + tx

out gui.bold(gui.green("--- ТЕСТ ЗАВЕРШЕН УСПЕШНО ---"))
