out "--- LAVA ENGINE 6.0: MAGMA EDITION ---"

# 1. Работа с массивами
let storage = [10, 20, 30]
out "Начальный массив: " + str(storage)

# 2. Сложная функция
fn process(item, factor) {
    let calc = item * factor
    out "Обработка: " + str(item) + " -> " + str(calc)
}

# 3. Цикл и условия
let i = 0
while i < size(storage) {
    let current = storage[i]
    if current > 15 {
        call process(current, 2)
    }
    let i = i + 1
}

# 4. Системный тест
out "Версия ядра: " + VER
out "Операция завершена успешно."
