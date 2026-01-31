# === ТЕСТ ГИГАНТСКОГО ДВИЖКА v0.4.5 ===
sys.clear()
out gui.bold(gui.cyan("--- ИНИЦИАЛИЗАЦИЯ МАГМЫ ---"))

# 1. Математический модуль
let radius = 12
let area = math.pi * math.pow(radius, 2)
out "Площадь круга (R=12): " + val.str(area)
out "Корень из 144: " + val.str(math.root(144))

# 2. Системный модуль
out "ОС: " + sys.os + " (" + sys.arch + ")"
out "Аптайм: " + val.str(sys.uptime()) + " сек"

# 3. Модуль безопасности
let my_hash = crypto.sha256("lava_secret")
out "SHA256: " + my_hash

# 4. Модуль Android (Termux)
let battery = termux.battery()
out "Заряд: " + val.str(battery["percentage"]) + "% [" + battery["status"] + "]"

# 5. Сетевой тест
out "Запрос внешнего IP..."
let ip = net.get("https://api.ipify.org")
out "Твой IP: " + ip

# 6. Работа со строками
let raw_text = "   Lava is Hot   "
let clean_text = val.lower(val.replace(raw_text, " ", ""))
out "Обработка текста: " + clean_text

out gui.bold(gui.green("--- ВСЕ СИСТЕМЫ В НОРМЕ ---"))
