out "=== LAVA SCRIPT ORIGINAL SYSTEM ==="

# Используем свои методы
let data = ["Core", "Magma", "Flow"]
let count = sys.size(data)
let i = 0

out "Версия системы: " + val.str(count)

while i < count {
    let node = data[i]
    out "Обработка узла: " + node
    
    # Свои математические функции
    let power = math.max(10, 50)
    
    if i == 1 {
        out "Мощность на узле: " + val.str(power)
    }
    
    let i = i + 1
}

out "Время завершения: " + sys.now()
