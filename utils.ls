cat << 'EOF' > utils.ls
# Проверка системных ресурсов
out "Текущая директория: " + sys.path()
out "Время старта: " + sys.now()
out "Список файлов проекта:"
out sys.scan()
EOF
