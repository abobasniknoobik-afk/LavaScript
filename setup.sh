#!/bin/bash
# Установка LavaScript в систему Termux
echo -e "\e[33mУстановка LavaScript v0.2...\e[0m"

# Копируем движок в системный путь
cp engine.py $PREFIX/bin/lava
chmod +x $PREFIX/bin/lava

# Создаем ассоциацию файлов для Termux
mkdir -p ~/.termux/file-editor
cat << 'EOF' > ~/.termux/file-editor/ls_handler.sh
#!/bin/bash
clear
lava "$1"
echo -e "\n\e[34m--- Программа завершена. Нажмите Enter ---\e[0m"
read
EOF
chmod +x ~/.termux/file-editor/ls_handler.sh

echo -e "\e[32mГотово! Теперь используй команду 'lava имя_файла.ls'\e[0m"
