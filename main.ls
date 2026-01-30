include "stdlib.ls"
include "utils.ls"

out "--- LAVA SCRIPT PRO ACTIVATED ---"

let user = "Admin"
let items = [10, 20, 30]

# Теперь вызовы будут работать 100%
call array_summary(items)
call math_max(50, 80)

out "--- ПРОГРАММА ЗАВЕРШЕНА ---"
