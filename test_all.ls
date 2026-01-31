# === ИСПРАВЛЕННЫЙ ГЛОБАЛЬНЫЙ ТЕСТ ===
sys.clear()
out gui.bold(gui.gold("--- ПЕРЕЗАПУСК ТЕСТА v0.2.1 ---"))

# Тест корня (теперь через .root)
let r = math.root(144)
out "Корень из 144: " + val.str(r)

# Тест батареи (теперь безопасно)
let bat = termux.battery()
out "Заряд: " + val.str(bat["percentage"]) + "%"

# Тест пути
let my_dir = fs.cwd()
out "Текущая папка: " + my_dir

out gui.green("--- ТЕПЕРЬ ВСЁ ЧИСТО! ---")
