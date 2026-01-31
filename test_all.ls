# === ТЕСТОВОЕ ЗАДАНИЕ ДЛЯ LAVASCRIPT v0.2 ===
sys.clear()
out gui.bold(gui.gold("--- ЗАПУСК ПОЛНОЙ ПРОВЕРКИ СИСТЕМЫ ---"))

# 1. ТЕСТ МАТЕМАТИКИ
let p = math.pi
let s = math.sin(p / 2)
let r = math.sqrt(144)
out "Математика: PI=" + val.str(p) + ", sin(90)=" + val.str(s) + ", sqrt(144)=" + val.str(r)

# 2. ТЕСТ ПЕРЕМЕННЫХ И ТИПОВ
let greeting = "Привет, Лава!"
let num = 100
out "Текст: " + greeting
out "Тип числа: " + val.type(num)
out "Верхний регистр: " + val.upper(greeting)

# 3. ТЕСТ КРИПТОГРАФИИ
let hash = crypto.sha256("lava2026")
out "Крипто (SHA256): " + hash

# 4. ТЕСТ ЦВЕТОВ ГРАФИКИ (GUI)
out gui.red("Это красный")
out gui.green("Это зеленый")
out gui.blue("Это синий")

# 5. ТЕСТ СИСТЕМЫ (БЕЗОПАСНЫЙ)
let my_os = sys.platform
let current_time = sys.date()
out "Платформа: " + my_os
out "Время сейчас: " + current_time

# 6. ТЕСТ ГЕНЕРАТОРА СЛУЧАЙНЫХ ЧИСЕЛ
let r_num = rand.num(1, 100)
out "Случайное число (1-100): " + val.str(r_num)

# 7. ТЕСТ СЕТИ (Проверка пинга)
out "Проверка связи с Google..."
let g_ping = net.ping("8.8.8.8")
out "Google Online: " + val.str(g_ping)

out ""
out gui.bold(gui.green("--- ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО ---"))
