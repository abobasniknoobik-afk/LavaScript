# ==========================================
# LavaScript System Utilities (utils.ls)
# Авторство: LS Team / Project Magma
# ==========================================

# 1. Красивое оформление интерфейса
fn draw_line() {
    out "------------------------------------------"
}

fn header(title) {
    call draw_line()
    out ">>> [ " + title + " ] <<<"
    call draw_line()
}

# 2. Системная информация
fn sys_info() {
    out "Engine: LavaScript " + VER
    out "OS: " + platform
    out "Time: " + str(now())
}

# 3. Утилиты для работы с данными
fn notify(msg) {
    out "[NOTIFY] " + str(msg)
}

fn check_list(arr) {
    let s = size(arr)
    out "Анализ массива... Обнаружено элементов: " + str(s)
    if s == 0 {
        out "ВНИМАНИЕ: Массив пуст!"
    }
}

# 4. Работа с файловой системой через Shell
fn list_files() {
    out "Список файлов в текущей директории:"
    sh "ls -p | grep -v /"
}

fn create_backup(filename) {
    out "Создание резервной копии: " + filename
    sh "cp " + filename + " " + filename + ".bak"
    out "Копия создана успешно."
}

# 5. Математические помощники
fn percent(total, part) {
    let res = (part / total) * 100
    out "Доля: " + str(res) + "%"
}
