# === LAVA STDLIB v0.2 ===
let PI = math.pi
let E = math.e
let PLATFORM = sys.shell("uname -a")
let IS_TERMUX = fs.exists("/data/data/com.termux")

# Базовые уведомления при загрузке
let welcome_msg = "LavaScript Magma Core Loaded"
out gui.bold(gui.cyan(welcome_msg))
