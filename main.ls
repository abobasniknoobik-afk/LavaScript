include "stdlib.ls"
include "utils.ls"

out "=== ЗАПУСК ВЫСОКОНАГРУЖЕННОЙ СХЕМЫ ==="

# 1. Сложный массив объектов (имитация JSON)
let server_farm = ["STABLE", "STABLE", "CRITICAL", "STABLE"]
let metrics = [15, 8, 25, 42, 5]

# 2. Запуск аналитики из stdlib
call analyze_data_stream(server_farm)

# 3. Вложенный цикл: прогоняем метрики через логику узлов
out "Сканирование нейро-слоя метрик..."
let x = 0
while x < size(metrics) {
    let m = metrics[x]
    out "Обработка пакета #" + str(x)
    
    # Вызов функции внутри цикла
    call simulate_node_logic(m)
    
    # Вложенное условие
    if m > 40 {
        out "ПРЕДУПРЕЖДЕНИЕ: Аномальный всплеск данных!"
        sh "echo 'Alert: High metric detected' >> alerts.log"
    }
    
    let x = x + 1
}

# 4. Проверка системных ресурсов через utils
call sys_header()
out "Статус системы: " + str(now())
out "=== ТЕСТ ЗАВЕРШЕН УСПЕШНО ==="
