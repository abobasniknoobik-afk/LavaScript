out "=== LAVA SCRIPT v13.0 TITANIUM ==="

# 1. Работа с рандомом и математикой
let secret = rand.int(1, 100)
let root = math.sqrt(secret)
out "Случайное число: " + val.str(secret)
out "Его корень: " + val.str(root)

# 2. Работа со списками в стиле LS
let files = sys.ls(sys.cwd())
let i = 0

out "Файлов в папке: " + val.str(sys.size(files))

# Цикл с использованием оригинальных методов
while i < sys.size(files) {
    let f = files[i]
    out "Файл #" + val.str(i) + ": " + f
    let i = i + 1
}

out "Текущее время: " + sys.now()
out "=== СИСТЕМА СТАБИЛЬНА ==="
