out "--- LAVA ENGINE 5.1 ACTIVATED ---"

fn check_status(val) {
    if val > 50 {
        out "КРИТИЧЕСКИЙ УРОВЕНЬ: " + str(val)
    }
    if val <= 50 {
        out "СТАБИЛЬНО: " + str(val)
    }
}

let i = 1
while i <= 3 {
    # Теперь random передается как две цифры
    let power = random(1, 100)
    out "Запуск проверки #" + str(i)
    call check_status(power)
    let i = i + 1
}

out "--- ТЕСТ ЗАВЕРШЕН ---"
