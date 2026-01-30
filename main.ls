cat << 'EOF' > main.ls
out "Запуск LavaScript v16.0 Titanium"
let name = "Разработчик"
out "Привет, " + name

let x = 10
let y = 20
out "Сумма x + y = " + val.str(x + y)

if x < y {
  out "Условие x < y работает!"
}
EOF
