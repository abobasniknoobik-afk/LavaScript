include "stdlib.ls"

out "--- LAVA SCRIPT PRO ACTIVATED ---"

# Работаем в стиле JS
let users = ["Admin", "Owner", "Guest"]
let config = {"status": "active", "level": 5}

out "User list: " + str(users)

# Вызов функции из другого файла
call array_info(users)

let i = 0
while i < size(users) {
    let current = users[i]
    out "Checking user: " + current
    if current == "Owner" {
        out "Access Level: MAX"
        call system_diag()
    }
    let i = i + 1
}

out "Program finished at: " + str(now())
