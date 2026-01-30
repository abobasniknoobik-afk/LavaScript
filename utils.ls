# ==========================================
# LavaScript Utilities (utils.ls)
# ==========================================

fn sys_header() {
    out "======================================"
    out "      LAVA ENGINE PRO v8.3.0"
    out "      Platform: " + platform
    out "======================================"
}

fn create_log(msg) {
    let timestamp = now()
    # Записываем лог через системную команду sh
    sh "echo '[" + timestamp + "] " + msg + "' >> system.log"
    out "Лог записан в system.log"
}

fn check_network() {
    out "Проверка соединения..."
    sh "ping -c 1 google.com"
}
