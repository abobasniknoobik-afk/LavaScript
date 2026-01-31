# ТЕСТ МАГМА v0.4
sys.clear()
out gui.bold(gui.magenta("--- ЗАПУСК ГЛОБАЛЬНОЙ ПРОВЕРКИ ---"))

# Математика
let m = math.pow(math.root(144), 2)
out "Math: " + val.str(m)

# Криптография
let c = crypto.sha512("lavacode")
out "Crypto SHA512: " + val.str(val.len(c)) + " chars"

# Файлы
out "FS: Твой ник в системе: " + sys.get_env("USER")
out "FS: Домашняя папка: " + fs.home()

# Железо (Android/Termux)
let b = termux.battery()
out "Termux: Заряд " + val.str(b["percentage"]) + "%"
out "Termux: Статус " + b["status"]

# Цвета
out gui.bg_red(gui.white(" СИСТЕМА СТАБИЛЬНА "))

out gui.bold(gui.gold("--- ТЕСТ v0.4 ЗАВЕРШЕН ---"))
