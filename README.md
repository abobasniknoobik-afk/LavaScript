cat << 'EOF' > README.md
# 🌋 LavaScript (LS) — Спецификация / Specification

## [ RU ] — Русская версия

### 🛠 Основные команды
| Команда | Значение |
| :--- | :--- |
| `let` | Создание или обновление переменной |
| `out` | Вывод данных в консоль |
| `if { }` | Условный оператор |
| `while { }` | Цикл |
| `#` | Однострочный комментарий |

### 🧠 Модуль val (Типы)
- `val.str` — Преобразовать в строку
- `val.int` — Преобразовать в целое число
- `val.dec` — Преобразовать в дробь
- `val.kind` — Тип данных

### 📐 Модуль math (Математика)
- `math.root` — Квадратный корень
- `math.exp` — Степень
- `math.up / math.down` — Округление
- `math.total` — Сумма списка

### 📁 Модуль sys (Система)
- `sys.now` — Дата и время
- `sys.path` — Текущий путь
- `sys.scan` — Список файлов
- `sys.pause` — Пауза (сек)
- `sys.size` — Размер объекта

### 🌐 Модуль net & 📱 termux
- `net.get` — Запрос к сайту (URL)
- `termux.toast` — Уведомление на экран
- `termux.vibrate` — Вибрация (мс)

### 🌍 Интеграция в ОС
Чтобы ваша ОС понимала файлы `.ls`:
1. **Linux / Android (Termux):** Скопируйте `lavalang.xml` в `~/.local/share/mime/packages/` и выполните `update-mime-database ~/.local/share/mime`.
2. **Windows:** Запустите файл `register_ls.reg`. Система будет подписывать файлы как "LavaScript Source File".
3. **MacOS:** Добавьте расширение в настройки текстового редактора как "Plain Text".

---

## [ EN ] — English Version

### 🛠 Core Commands
| Command | Meaning |
| :--- | :--- |
| `let` | Create or update a variable |
| `out` | Print data to console |
| `if { }` | Conditional statement |
| `while { }` | Loop statement |
| `#` | Single-line comment |

### 🧠 Module val (Types)
- `val.str` — Convert to string
- `val.int` — Convert to integer
- `val.dec` — Convert to decimal
- `val.kind` — Get data type name

### 📐 Module math (Math)
- `math.root` — Square root
- `math.exp` — Exponentiation
- `math.up / math.down` — Rounding
- `math.total` — List sum

### 📁 Module sys (System)
- `sys.now` — Date and time
- `sys.path` — Current path
- `sys.scan` — List files
- `sys.pause` — Pause (sec)
- `sys.size` — Object size

### 🌐 Module net & 📱 termux
- `net.get` — Web request (URL)
- `termux.toast` — Screen notification
- `termux.vibrate` — Vibration (ms)

### 🌍 OS Integration
To make your OS recognize `.ls` files:
1. **Linux / Android (Termux):** Copy `lavalang.xml` to `~/.local/share/mime/packages/` and run `update-mime-database ~/.local/share/mime`.
2. **Windows:** Run `register_ls.reg`. The system will label files as "LavaScript Source File".
3. **MacOS:** Add the extension to your text editor settings as "Plain Text".

---
**Current Version:** v0.1_TEST 🌋
EOF
