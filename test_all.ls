# === LAVASCRIPT CRYSTAL TEST ===
sys.clear()
out gui.bold(gui.gold("--- ЗАПУСК ГЛОБАЛЬНОГО ТЕСТА v0.2.4 ---"))

# 1. Математика (Тест .root)
let x = math.root(144)
out "Математика (root 144): " + val.str(x)

# 2. Файловая система (Тест .path и .cwd)
let p = fs.path(fs.cwd())
out "Путь проекта: " + p

# 3. Termux (Тест батареи - теперь как функция)
let b_data = termux.battery()
out "Заряд батареи: " + val.str(b_data["percentage"]) + "%"

# 4. Типы данных
let s = "lava"
out "Тип переменной: " + val.type(s)

# 5. Сеть (Запрос IP)
out "Проверка сети..."
let my_ip = net.get("https://api.ipify.org")
out "Твой IP: " + my_ip

out gui.bold(gui.green("--- ТЕСТ ЗАВЕРШЕН УСПЕШНО ---"))
