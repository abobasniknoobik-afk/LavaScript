#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LavaScript Engine (LS)
Version: 0.4.5 Magma Giant
Description: Расширенный интерпретатор LavaScript для Termux.
"""

import sys
import os
import re
import math
import time
import subprocess
import random
import urllib.request
import hashlib
import json
import base64
import shutil
import datetime
import platform
import binascii

# --- ЯДРО СИСТЕМЫ КЛАССОВ ---

class LavaModule:
    """Класс для создания пространств имен модулей"""
    def __init__(self, name, description, methods):
        self.__name__ = name
        self.__doc__ = description
        for key, value in methods.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"<LavaModule '{self.__name__}'>"

class LavaScript:
    def __init__(self):
        self.version = "v0.4.5_GIANT"
        self.scope = {}
        self.start_time = time.time()
        
        # --- СЕКЦИЯ ВНУТРЕННИХ УТИЛИТ ---
        
        def _run_sh(cmd):
            """Безопасный запуск системных команд"""
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                return res.stdout.strip()
            except Exception:
                return ""

        def _get_json_api(cmd):
            """Получение и парсинг JSON из Termux API"""
            raw = _run_sh(cmd)
            try:
                return json.loads(raw) if raw.startswith(("{", "[")) else {}
            except:
                return {"error": "invalid_json", "raw": raw}

        # --- МОДУЛЬ 1: MATH (Математика и тригонометрия) ---
        # Расширенная библиотека для вычислений
        self.math_lib = LavaModule("math", "Advanced Mathematics", {
            "pi": math.pi,
            "e": math.e,
            "sqrt": math.sqrt,
            "root": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "ceil": math.ceil,
            "floor": math.floor,
            "round": round,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "fact": math.factorial,
            "deg": math.degrees,
            "rad": math.radians,
            "gcd": math.gcd,
            "hypot": math.hypot,
            "inf": float('inf'),
            "nan": float('nan')
        })

        # --- МОДУЛЬ 2: FS (Работа с файловой системой) ---
        # Всё для управления файлами и папками
        self.fs_lib = LavaModule("fs", "File System Operations", {
            "cwd": os.getcwd,
            "path": os.path.abspath,
            "ls": os.listdir,
            "exists": os.path.exists,
            "is_file": os.path.isfile,
            "is_dir": os.path.isdir,
            "size": os.path.getsize,
            "mkdir": lambda p: os.makedirs(p, exist_ok=True),
            "rm": os.remove,
            "rmdir": shutil.rmtree,
            "read": lambda p: open(p, 'r', encoding='utf-8').read(),
            "write": lambda p, d: open(p, 'w', encoding='utf-8').write(str(d)),
            "append": lambda p, d: open(p, 'a', encoding='utf-8').write(str(d)),
            "copy": shutil.copy,
            "move": shutil.move,
            "home": lambda: os.path.expanduser("~"),
            "rename": os.rename
        })

        # --- МОДУЛЬ 3: SYS (Инспекция системы) ---
        self.sys_lib = LavaModule("sys", "System Diagnostics", {
            "ver": self.version,
            "platform": sys.platform,
            "os": platform.system(),
            "arch": platform.machine(),
            "uptime": lambda: round(time.time() - self.start_time, 3),
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
            "timestamp": time.time,
            "sleep": time.sleep,
            "clear": lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            "exit": sys.exit,
            "get_env": os.getenv,
            "argv": sys.argv
        })

        # --- МОДУЛЬ 4: CRYPTO (Криптография и Хеширование) ---
        self.crypto_lib = LavaModule("crypto", "Cryptography Methods", {
            "md5": lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            "sha1": lambda t: hashlib.sha1(str(t).encode()).hexdigest(),
            "sha256": lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            "sha512": lambda t: hashlib.sha512(str(t).encode()).hexdigest(),
            "b64e": lambda t: base64.b64encode(str(t).encode()).decode(),
            "b64d": lambda t: base64.b64decode(str(t)).decode(),
            "crc32": lambda t: hex(binascii.crc32(str(t).encode()) & 0xffffffff),
            "uuid": lambda: _run_sh(["uuidgen"]) if os.name != 'nt' else "not_supported"
        })

        # --- МОДУЛЬ 5: TERMUX (Интеграция с Android) ---
        self.termux_lib = LavaModule("termux", "Android API Hooks", {
            "battery": lambda: _get_json_api(["termux-battery-status"]),
            "wifi": lambda: _get_json_api(["termux-wifi-connectioninfo"]),
            "toast": lambda m: subprocess.run(["termux-toast", "-s", str(m)]),
            "vibrate": lambda d=200: subprocess.run(["termux-vibrate", "-d", str(d)]),
            "torch": lambda s: subprocess.run(["termux-torch", "on" if s else "off"]),
            "speak": lambda t: subprocess.run(["termux-tts-speak", str(t)]),
            "clip_set": lambda t: subprocess.run(["termux-clipboard-set", str(t)]),
            "clip_get": lambda: _run_sh(["termux-clipboard-get"]),
            "volume": lambda s, v: subprocess.run(["termux-volume", str(s), str(v)])
        })

        # --- МОДУЛЬ 6: GUI (Цвета и стилизация терминала) ---
        self.gui_lib = LavaModule("gui", "Terminal UI Elements", {
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m",
            "red": lambda t: f"\x1b[31m{t}\x1b[0m",
            "green": lambda t: f"\x1b[32m{t}\x1b[0m",
            "blue": lambda t: f"\x1b[34m{t}\x1b[0m",
            "cyan": lambda t: f"\x1b[36m{t}\x1b[0m",
            "magenta": lambda t: f"\x1b[35m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m",
            "bg_red": lambda t: f"\x1b[41m{t}\x1b[0m",
            "underline": lambda t: f"\x1b[4m{t}\x1b[0m"
        })

        # --- МОДУЛЬ 7: VAL (Обработка типов и JSON) ---
        self.val_lib = LavaModule("val", "Data Conversion", {
            "str": str, "int": int, "float": float, "len": len,
            "type": lambda x: type(x).__name__,
            "json_p": json.loads,
            "json_b": json.dumps,
            "upper": lambda t: str(t).upper(),
            "lower": lambda t: str(t).lower(),
            "split": lambda t, s=" ": str(t).split(s),
            "join": lambda l, s="": s.join(l),
            "replace": lambda t, o, n: str(t).replace(o, n)
        })

        # Сборка финального окружения
        self.env = {
            "math": self.math_lib, "fs": self.fs_lib, "sys": self.sys_lib,
            "crypto": self.crypto_lib, "termux": self.termux_lib,
            "gui": self.gui_lib, "val": self.val_lib,
            "net": LavaModule("net", "Networking", {
                "get": lambda url: urllib.request.urlopen(url, timeout=5).read().decode(),
                "ping": lambda h: os.system(f"ping -c 1 {h} > /dev/null") == 0
            }),
            "rand": LavaModule("rand", "Randomness", {
                "num": random.randint,
                "choice": random.choice,
                "range": random.randrange
            })
        }

    def execute(self, line):
        """Парсинг и выполнение строки кода"""
        line = line.strip()
        if not line or line.startswith("#"):
            return
            
        ctx = {**self.env, **self.scope}
        
        try:
            # Определение переменных: let x = expr
            if line.startswith("let "):
                match = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if match:
                    name, expr = match.groups()
                    self.scope[name] = eval(expr, {"__builtins__": None}, ctx)
                return

            # Вывод в консоль: out expr
            if line.startswith("out "):
                res = eval(line[4:], {"__builtins__": None}, ctx)
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {res}")
                return

            # Выполнение выражений без вывода
            eval(line, {"__builtins__": None}, ctx)

        except Exception as e:
            print(f"\x1b[31m[LS_ERROR]\x1b[0m {type(e).__name__}: {e}")

    def repl(self):
        """Интерактивная оболочка REPL"""
        self.sys_lib.clear()
        print(f"\x1b[1;33m🌋 LavaScript {self.version}\x1b[0m")
        print(f"\x1b[38;5;244mEngine started in {self.sys_lib.uptime()}s\x1b[0m\n")
        while True:
            try:
                prompt = input("\x1b[38;5;226mLS>\x1b[0m ")
                if prompt.lower() in ["exit", "quit"]: break
                self.execute(prompt)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        # Пакетный режим выполнения файлов
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                for line in f:
                    engine.execute(line)
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found.")
    else:
        # Режим консоли
        engine.repl()
