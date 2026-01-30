out "--- ТЕСТ АРСЕНАЛА v15.0 ---"

# Математика
let n = 144
out "Корень из 144: " + val.str(math.root(n))
out "Синус 0: " + val.str(math.sin(0))

# Списки и Рандом
let items = ["Lava", "Magma", "Titan"]
out "Случайный выбор: " + rand.select(items)

# Системная пауза (на 1 секунду)
out "Ждем секунду..."
call sys.pause(1)

# Проверка файлов
let files = sys.scan(sys.path())
out "Файлов в системе: " + val.str(sys.size(files))

out "--- ВСЕ СИСТЕМЫ В НОРМЕ ---"
