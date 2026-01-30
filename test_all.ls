out "--- ЗАПУСК ГЛОБАЛЬНОГО ТЕСТА v0.1_TEST ---"

let check_math = math.root(100)
out "Тест Math (корень 100): " + val.str(check_math)

let check_sys = sys.path()
out "Тест Sys (путь): " + check_sys

out "Тест Net (запрос IP)..."
let my_ip = net.get("https://api.ipify.org")
out "Твой IP: " + my_ip

out "Тест Termux (вибрация и уведомление)..."
termux.toast("LavaScript v0.1_TEST: Все системы в норме!")
termux.vibrate(300)

out "--- ТЕСТ ЗАВЕРШЕН УСПЕШНО ---"
