# === ТЕСТ МАГМА ГИГАНТ ===
sys.clear()
out gui.bold(gui.magenta("--- ЗАПУСК ОБЗОРА СИСТЕМЫ ---"))

# Проверка ядра
out "Архитектура: " + sys.arch
out "Аптайм движка: " + val.str(sys.uptime()) + " сек"

# Проверка крипты
let secret = crypto.sha512("lava_is_hot")
out "SHA512 (первые 10): " + val.str(val.split(secret, "")[0]) # Просто тест длины

# Проверка файлов
let h = fs.home()
out "Домашняя папка: " + h

# Проверка Termux
let b = termux.battery()
out "Батарея: " + val.str(b["percentage"]) + "% (" + b["status"] + ")"

# Проверка Сети
out "IP: " + net.get("https://api.ipify.org")

out gui.bold(gui.green("--- ВСЕ МОДУЛИ ВКЛЮЧЕНЫ ---"))
