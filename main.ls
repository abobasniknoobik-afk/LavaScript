# LavaScript Ultra 5.0 Test
out "--- ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ LAVA ---"

# 1. Работа с системными командами
out "Список файлов в директории:"
sh ls

# 2. Создание функции
fn check_status(val) {
    if val > 50 {
        out "Статус: КРИТИЧЕСКИЙ (" + str(val) + ")"
    }
    if val <= 50 {
        out "Статус: НОРМА (" + str(val) + ")"
    }
}

# 3. Интерактив и Цикл
ask name << "Введите имя оператора: "
out "Приветствую, " + name

let i = 1
while i <= 3 {
    let power = random(1, 100)
    call check_status(power)
    let i = i + 1
    wait 0.5
}

# 4. Работа с интернетом и файлами
out "Запрос данных из сети..."
fetch "https://google.com" >> site_data
out "Данные получены. Сохраняю лог..."
write "log.txt" << "User " + name + " accessed system. Data: " + site_data

out "--- ПРОГРАММА ЗАВЕРШЕНА ---"
