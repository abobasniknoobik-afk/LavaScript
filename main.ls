include "stdlib.ls"
include "utils.ls"

out "=== ТЕСТ НА СТАБИЛЬНОСТЬ ==="

let server_status = ["OK", "OK", "CRITICAL", "OK"]
let i = 0

# Проход по массиву с защитой
while i < size(server_status) {
    let current = server_status[i]
    out "Обработка узла: " + str(current)
    
    if current == "CRITICAL" {
        out "--- ПАНИКА: Узел упал! ---"
    }
    
    # ВАЖНО: всегда увеличиваем индекс в конце
    let i = i + 1
}

out "=== СИСТЕМА ВЫСТОЯЛА ==="
