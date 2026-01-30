# Подключаем наши библиотеки
include "stdlib.ls"
include "utils.ls"

# Запуск системы
call sys_header()

# Создаем "взрослые" данные (объекты и списки)
let developer = "Admin"
let projects = ["LavaScript", "Vesuvius", "Magma"]

out "Добро пожаловать, " + developer
call array_summary(projects)

# Используем логику из stdlib
call math_max(100, 250)

# Системное действие из utils
call create_log("Сессия запущена пользователем " + developer)

out "Текущее время: " + now()
out "--- ПРОГРАММА ЗАВЕРШЕНА ---"
