# === LAVA UTILS v0.2 ===
# Генерация ID сессии
let session_id = crypto.md5(sys.now())

# Проверка интернета
let has_net = net.ping("8.8.8.8")

# Быстрый формат времени
let log_time = sys.now()
