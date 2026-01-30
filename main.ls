out "=== LAVA SCRIPT v13.1 FIXED ==="

let secret = rand.int(1, 100)
let root = math.sqrt(secret)

out "Число: " + val.str(secret)
out "Корень: " + val.str(root)

let files = sys.ls(sys.cwd())
let i = 0

out "Найдено объектов: " + val.str(sys.size(files))

while i < sys.size(files) {
    let f = files[i]
    out "Элемент: " + f
    let i = i + 1
}

out "=== ЗАВЕРШЕНО БЕЗ NONE ==="
