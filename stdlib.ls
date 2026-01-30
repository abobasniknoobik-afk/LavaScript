# LavaScript Standard Library (v1.0)
# Присваиваем авторство: Created by LS Team 2026

fn math_power(base, exp) {
    let res = base ** exp
    out "Power Result: " + str(res)
}

fn array_info(arr) {
    out "Array size: " + str(size(arr))
    out "First element: " + str(arr[0])
}

fn system_diag() {
    out "System diagnostics..."
    out "Engine Version: " + VER
    out "Current OS: " + platform
}
