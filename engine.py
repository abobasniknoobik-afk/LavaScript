#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform

class Module:
    def __init__(self, name, methods):
        self.name = name
        for key, value in methods.items():
            setattr(self, key, value)

class LavaScript:
    def __init__(self):
        self.version = "v0.3_MAGMA_GIANT"
        self.scope = {}
        self.start_time = time.time()
        
        # --- ВНУТРЕННИЙ ДВИЖОК TERMUX ---
        def run_tm(args):
            try:
                res = subprocess.run(args, capture_output=True, timeout=3)
                out = res.stdout.decode().strip()
                return out if out else "{}"
            except: return "{}"

        # --- МОДУЛЬ: MATH (Математика) ---
        math_methods = {
            "pi": math.pi, "e": math.e,
            "sqrt": math.sqrt, "root": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "ceil": math.ceil, "floor": math.floor,
            "log": math.log, "log10": math.log10,
            "pow": math.pow, "abs": math.fabs,
            "factorial": math.factorial, "deg": math.degrees, "rad": math.radians
        }

        # --- МОДУЛЬ: FS (Файловая система) ---
        fs_methods = {
            "cwd": os.getcwd,
            "path": os.path.abspath,
            "exists": os.path.exists,
            "mkdir": lambda p: os.mkdir(p),
            "rmdir": lambda p: os.rmdir(p),
            "ls": os.listdir,
            "read": lambda p: open(p, "r", encoding="utf-8").read(),
            "write": lambda p, d: open(p, "w", encoding="utf-8").write(str(d)),
            "append": lambda p, d: open(p, "a", encoding="utf-8").write(str(d)),
            "remove": os.remove,
            "size": os.path.getsize,
            "copy": shutil.copy,
            "move": shutil.move,
            "is_file": os.path.isfile,
            "is_dir": os.path.isdir
        }

        # --- МОДУЛЬ: SYS (Система и Время) ---
        sys_methods = {
            "platform": sys.platform,
            "os": platform.system(),
            "arch": platform.machine(),
            "version": self.version,
            "clear": lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            "sleep": time.sleep,
            "exit": sys.exit,
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
            "full_date": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": lambda: time.time(),
            "uptime": lambda: time.time() - self.start_time,
            "argv": sys.argv
        }

        # --- МОДУЛЬ: CRYPTO (Шифрование) ---
        crypto_methods = {
            "md5": lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            "sha1": lambda t: hashlib.sha1(str(t).encode()).hexdigest(),
            "sha256": lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            "b64en": lambda t: base64.b64encode(str(t).encode()).decode(),
            "b64de": lambda t: base64.b64decode(str(t)).decode(),
            "hash": lambda t: hash(t)
        }

        # --- МОДУЛЬ: NET (Сеть) ---
        def http_get(url):
            try:
                with urllib.request.urlopen(url, timeout=5) as r:
                    return r.read().decode('utf-8')
            except Exception as e: return f"Error: {e}"

        net_methods = {
            "get": http_get,
            "ping": lambda h: os.system(f"ping -c 1 {h} > /dev/null") == 0
        }

        # --- МОДУЛЬ: TERMUX (API Android) ---
        def get_battery():
            try:
                data = json.loads(run_tm(["termux-battery-status"]))
                return data if data else {"percentage": 0, "status": "Unknown"}
            except: return {"percentage": 0, "status": "Error"}

        tm_methods = {
            "battery": get_battery,
            "toast": lambda m: run_tm(["termux-toast", str(m)]),
            "vibrate": lambda d=200: run_tm(["termux-vibrate", "-d", str(d)]),
            "speak": lambda t: run_tm(["termux-tts-speak", str(t)]),
            "volume": lambda s, v: run_tm(["termux-volume", str(s), str(v)]),
            "brightness": lambda v: run_tm(["termux-brightness", str(v)]),
            "clipboard_set": lambda t: run_tm(["termux-clipboard-set", str(t)]),
            "clipboard_get": lambda: run_tm(["termux-clipboard-get"])
        }

        # --- МОДУЛЬ: GUI (Цвета и оформление) ---
        gui_methods = {
            "red": lambda t: f"\x1b[31m{t}\x1b[0m",
            "green": lambda t: f"\x1b[32m{t}\x1b[0m",
            "blue": lambda t: f"\x1b[34m{t}\x1b[0m",
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m",
            "cyan": lambda t: f"\x1b[36m{t}\x1b[0m",
            "magenta": lambda t: f"\x1b[35m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m",
            "underline": lambda t: f"\x1b[4m{t}\x1b[0m",
            "reset": "\x1b[0m"
        }

        # --- МОДУЛЬ: VAL (Типы данных) ---
        val_methods = {
            "str": str, "int": int, "float": float, "bool": bool,
            "type": lambda x: type(x).__name__,
            "len": len,
            "upper": lambda t: str(t).upper(),
            "lower": lambda t: str(t).lower(),
            "json_parse": json.loads,
            "json_build": json.dumps
        }

        # --- СБОРКА ОКРУЖЕНИЯ ---
        self.env = {
            "math": Module("math", math_methods),
            "fs": Module("fs", fs_methods),
            "sys": Module("sys", sys_methods),
            "crypto": Module("crypto", crypto_methods),
            "net": Module("net", net_methods),
            "termux": Module("termux", tm_methods),
            "gui": Module("gui", gui_methods),
            "val": Module("val", val_methods),
            "rand": Module("rand", {
                "num": random.randint,
                "choice": random.choice,
                "shuffle": random.shuffle
            })
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        
        ctx = {**self.env, **self.scope}
        
        try:
            # Обработка переменных (let name = value)
            if line.startswith("let "):
                match = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if match:
                    name, expr = match.groups()
                    self.scope[name] = eval(expr, {"__builtins__": None}, ctx)
                return

            # Обработка вывода (out value)
            if line.startswith("out "):
                res = eval(line[4:], {"__builtins__": None}, ctx)
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {res}")
                return

            # Прямое выполнение команд
            eval(line, {"__builtins__": None}, ctx)

        except Exception as e:
            print(f"\x1b[31m[LS_ERROR]\x1b[0m {e}")

    def repl(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"\x1b[1;33mLavaScript {self.version}\x1b[0m")
        print("\x1b[38;5;242mType 'sys.exit()' to quit.\x1b[0m\n")
        while True:
            try:
                line = input("\x1b[38;5;226mLS>\x1b[0m ")
                self.execute(line)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                for script_line in f:
                    engine.execute(script_line)
        except Exception as e:
            print(f"Failed to load file: {e}")
    else:
        engine.repl()
