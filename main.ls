# Подключаем внешние функции
include "utils.ls"

out "Запуск основной программы..."
call info()

let data = [5, 10, 15]
out "Размер массива: " + str(size(data))

if size(data) > 0 {
    out "Массив не пуст, система стабильна."
}
