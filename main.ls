# Подключаем библиотеки (имитация импорта через чтение файлов)
out gui.gold("--- ЗАПУСК MAIN ---")

let my_ip = net.ip()
out "Мой IP: " + my_ip

let b = termux.battery()
out "Заряд: " + val.str(val.get(b, "percentage", 0)) + "%"

out gui.green("--- СИСТЕМА OK ---")
