# LavaScript Professional v4.0
out "--- LAVA ENGINE 4.0 LOADED ---"

# 1. Объявление функции
fn greet(name) {
    out "Hello, " + name + "!"
}

# 2. Переменные и арифметика
let counter = 1
let limit = 3

# 3. Цикл While
out "Starting loop..."
while counter <= limit {
    out "Iteration: " + str(counter)
    call greet("Developer")
    let counter = counter + 1
}

# 4. Условия
if counter > limit {
    out "Process finished successfully."
}

out "System version: " + VERSION
