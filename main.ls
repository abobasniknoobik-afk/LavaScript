out "=== ЗАПУСК LAVA SCRIPT v14.0 ==="

# 1. Тест RAND и MATH
let chance = rand.num(1, 100)
let power = math.root(chance)
out "Случайный заряд: " + val.str(chance)
out "Корень мощности: " + val.str(math.fix(power, 2))

# 2. Тест SYS (Сканирование папки)
let location = sys.path()
let files = sys.scan(location)
let total = sys.size(files)

out "Локация: " + location
out "Найдено объектов: " + val.str(total)

# 3. Цикл обработки
let i = 0
while i < total {
    let item = files[i]
    if i < 5 {
        out "Объект #" + val.str(i) + ": " + item
    }
    let i = i + 1
}

out "Проверка завершена в: " + sys.now()
out "=== СИСТЕМА СТАБИЛЬНА ==="
