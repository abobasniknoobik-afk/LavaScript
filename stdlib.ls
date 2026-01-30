# ==========================================
# LavaScript Standard Library (stdlib.ls)
# ==========================================

# Работа со строками
fn capitalize(text) {
    let result = str(text).upper()
    out "Преобразование: " + result
}

# Математические операции в стиле JS
fn math_max(a, b) {
    if a > b {
        out "Максимум: " + str(a)
    }
    if b >= a {
        out "Максимум: " + str(b)
    }
}

# Работа с массивами
fn array_summary(arr) {
    let s = size(arr)
    out "Элементов в массиве: " + str(s)
    out "Тип структуры: " + type(arr)
}
