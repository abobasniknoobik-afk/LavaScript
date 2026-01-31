# === LAVASCRIPT SOLID TEST v0.2.5 ===
sys.clear()
out gui.bold(gui.gold("--- КРИСТАЛЬНЫЙ ТЕСТ ---"))

# 1. Math (Проверка root)
let r = math.root(144)
out "Root test: " + val.str(r)

# 2. FS (Проверка path)
let my_path = fs.path(".")
out "Path test: " + my_path

# 3. Termux Battery (ЗАМЕТЬ СКОБКИ: battery()["percentage"])
let bat = termux.battery()
let perc = bat["percentage"]
out "Battery: " + val.str(perc) + "%"

# 4. Net
out "Net test (IP)..."
let ip = net.get("https://api.ipify.org")
out "IP: " + ip

out gui.green("--- ТЕСТ ПРОЙДЕН ---")
