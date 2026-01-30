out "=== ТЕСТ СТАБИЛЬНОСТИ v14.2 ==="

# Обязательно используй () для вызова системных функций
let path = sys.path()
out "Путь: " + path

let num = rand.num(1, 10)
out "Рандом: " + val.str(num)

let files = sys.scan(path)
out "Объектов: " + val.str(sys.size(files))

out "=== ФИНИШ ==="
