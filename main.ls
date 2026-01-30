out "=== ТЕСТ СИСТЕМЫ v10.0 ==="

let status = ["START", "PROCESS", "FINISH"]
let i = 0

out "Длина массива: " + str(size(status))

while i < size(status) {
    let current = status[i]
    out "Шаг " + str(i) + ": " + str(current)
    let i = i + 1
}

if i == 3 {
    out "Логика IF: Работает"
}

out "=== ТЕСТ ЗАВЕРШЕН ==="
