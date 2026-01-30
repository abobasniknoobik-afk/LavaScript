# Мощная библиотека для работы со структурами
fn analyze_data_stream(data) {
    let i = 0
    out "--- НАЧАЛО ГЛУБОКОГО АНАЛИЗА ---"
    while i < size(data) {
        let item = data[i]
        out "Проверка узла: " + str(item)
        if item == "CRITICAL" {
            out "!!! ОБНАРУЖЕНА УГРОЗА В ПОТОКЕ !!!"
        }
        let i = i + 1
    }
}

fn simulate_node_logic(input_val) {
    # Имитация весов нейрона
    let weight = 0.5
    let threshold = 10
    let result = input_val * weight
    if result > threshold {
        out "Узел АКТИВИРОВАН: " + str(result)
    }
    if result <= threshold {
        out "Узел СПИТ: " + str(result)
    }
}
