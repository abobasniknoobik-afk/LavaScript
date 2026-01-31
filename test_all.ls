# === ТЕСТ ГИГАНТСКОГО ДВИЖКА v0.3 ===
sys.clear()
out gui.bold(gui.cyan("--- ЗАПУСК ГЛОБАЛЬНОГО ТЕСТА ---"))

# 1. ТЕСТ MATH
let r = math.root(144)
let p = math.pi
out "Math: root(144)=" + val.str(r) + " PI=" + val.str(p)

# 2. ТЕСТ FS
let cur = fs.cwd()
out "FS: Текущая папка: " + cur
out "FS: Путь: " + fs.path(".")

# 3. ТЕСТ SYS
out "SYS: Платформа: " + sys.platform
out "SYS: Время: " + sys.time()

# 4. ТЕСТ CRYPTO
let hash = crypto.sha256("lava")
out "Crypto: SHA256('lava')=" + hash

# 5. ТЕСТ TERMUX (С защитой от пустых данных)
let b = termux.battery()
out "Battery: " + val.str(b["percentage"]) + "%"

# 6. ТЕСТ NET
out "Net: Твой IP (запрос)..."
let my_ip = net.get("https://api.ipify.org")
out "Net: IP=" + my_ip

# 7. ТЕСТ GUI
out gui.red("Красный ") + gui.green("Зеленый ") + gui.blue("Синий")

out gui.bold(gui.gold("--- ТЕСТ ЗАВЕРШЕН УСПЕШНО ---"))
