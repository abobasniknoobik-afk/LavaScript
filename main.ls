out "=== ЗАПУСК ПОЛНОЙ ПРОВЕРКИ ==="

let server_status = ["OK", "STABLE", "CRITICAL", "OK"]
let i = 0

while i < size(server_status) {
    let current = server_status[i]
    out "Анализ узла #" + str(i) + ": " + str(current)
    
    if current == "CRITICAL" {
        out "!!! ВНИМАНИЕ: СБОЙ СЕРВЕРА !!!"
    }
    
    let i = i + 1
}

out "=== ПРОВЕРКА ЗАВЕРШЕНА ==="
