#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LavaScript Engine (LS) - Magma Titan Edition
Version: 0.5.1
Platform: Termux / Linux
"""

import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform, binascii

class LavaModule:
    """Обертка для создания модульной структуры LavaScript"""
    def __init__(self, name, description, methods):
        self.__name = name
        self.__doc__ = description
        self.__dict__.update(methods)
    def __repr__(self):
        return f"<LavaModule '{self.__name}'>"

class LavaScript:
    def __init__(self):
        self.version = "v0.5.1_TITAN"
        self.scope = {}
        self.start_time = time.time()
        
        # --- ВНУТРЕННИЕ СИСТЕМНЫЕ ФУНКЦИИ ---
        def run_sys(args):
            try:
                p = subprocess.run(args, capture_output=True, text=True, timeout=3)
                return p.stdout.strip() if p.stdout else ""
            except: return ""

        def api_json(cmd):
            raw = run_sys(cmd)
            try: return json.loads(raw) if raw.startswith(("{","[")) else {}
            except: return {"status": "error", "message": "no_api_response"}

        # --- МОДУЛИ ДВИЖКА ---

        # 1. MATH: Продвинутые вычисления
        self.math_lib = LavaModule("math", "Advanced Math", {
            "pi": math.pi, "e": math.e, "sqrt": math.sqrt, "root": math.sqrt,
            "pow": math.pow, "abs": abs, "ceil": math.ceil, "floor": math.floor,
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "fact": math.factorial,
            "log": math.log, "log10": math.log10, "deg": math.degrees, "rad": math.radians,
            "hypot": math.hypot, "gcd": math.gcd, "mod": lambda x,y: x%y
        })

        # 2. FS: Файловый комбайн
        self.fs_lib = LavaModule("fs", "File Operations", {
            "cwd": os.getcwd, "path": os.path.abspath, "ls": os.listdir,
            "exists": os.path.exists, "is_file": os.path.isfile, "is_dir": os.path.isdir,
            "read": lambda p: open(p, 'r', encoding='utf-8').read(),
            "write": lambda p, d: open(p, 'w', encoding='utf-8').write(str(d)),
            "append": lambda p, d: open(p, 'a', encoding='utf-8').write(str(d)),
            "mkdir": lambda p: os.makedirs(p, exist_ok=True),
            "rm": os.remove, "rmdir": shutil.rmtree, "size": os.path.getsize,
            "copy": shutil.copy, "move": shutil.move, "home": lambda: os.path.expanduser("~")
        })

        # 3. SYS: Ядро и время
        self.sys_lib = LavaModule("sys", "System Core", {
            "ver": self.version, "os": platform.system(), "arch": platform.machine(),
            "platform": sys.platform, "uptime": lambda: round(time.time() - self.start_time, 2),
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
            "clear": lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            "exit": sys.exit, "sleep": time.sleep, "get_env": os.getenv
        })

        # 4. CRYPTO: Безопасность
        self.crypto_lib = LavaModule("crypto", "Cryptography", {
            "sha256": lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            "sha512": lambda t: hashlib.sha512(str(t).encode()).hexdigest(),
            "md5": lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            "b64e": lambda t: base64.b64encode(str(t).encode()).decode(),
            "b64d": lambda t: base64.b64decode(str(t)).decode(),
            "crc32": lambda t: hex(binascii.crc32(str(t).encode()) & 0xffffffff)
        })

        # 5. TERMUX: Прямой доступ к Android
        self.termux_lib = LavaModule("termux", "Android API", {
            "battery": lambda: api_json(["termux-battery-status"]),
            "wifi": lambda: api_json(["termux-wifi-connectioninfo"]),
            "toast": lambda m: subprocess.run(["termux-toast", str(m)]),
            "vibrate": lambda d=200: subprocess.run(["termux-vibrate", "-d", str(d)]),
            "speak": lambda t: subprocess.run(["termux-tts-speak", str(t)]),
            "torch": lambda s: subprocess.run(["termux-torch", "on" if s else "off"]),
            "clip_set": lambda t: subprocess.run(["termux-clipboard-set", str(t)]),
            "clip_get": lambda: run_sys(["termux-clipboard-get"])
        })

        # 6. GUI: Стилизация вывода
        self.gui_lib = LavaModule("gui", "Interface", {
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m", "red": lambda t: f"\x1b[31m{t}\x1b[0m",
            "green": lambda t: f"\x1b[32m{t}\x1b[0m", "cyan": lambda t: f"\x1b[36m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m", "bg_red": lambda t: f"\x1b[41m{t}\x1b[0m"
        })

        # 7. VAL: Работа с типами
        self.val_lib = LavaModule("val", "Data Handling", {
            "str": str, "int": int, "float": float, "len": len,
            "type": lambda x: type(x).__name__, "json_p": json.loads,
            "upper": lambda t: str(t).upper(), "lower": lambda t: str(t).lower(),
            "replace": lambda t, o, n: str(t).replace(o, n),
            "split": lambda t, s=" ": str(t).split(s)
        })

        self.env = {
            "math": self.math_lib, "fs": self.fs_lib, "sys": self.sys_lib,
            "crypto": self.crypto_lib, "termux": self.termux_lib,
            "gui": self.gui_lib, "val": self.val_lib,
            "net": Lib("net", get=lambda u: urllib.request.urlopen(u, timeout=5).read().decode()),
            "rand": Lib("rand", num=random.randint, choice=random.choice)
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        ctx = {**self.env, **self.scope}
        try:
            if line.startswith("let "):
                m = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if m: self.scope[m.group(1)] = eval(m.group(2), {"__builtins__": None}, ctx)
                return
            if line.startswith("out "):
                res = eval(line[4:], {"__builtins__": None}, ctx)
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {res}")
                return
            eval(line, {"__builtins__": None}, ctx)
        except Exception as e:
            print(f"\x1b[31m[LS_ERROR]\x1b[0m {type(e).__name__}: {e}")

    def repl(self):
        self.sys_lib.clear()
        print(f"\x1b[1;33m🌋 LavaScript {self.version} [REPL MODE]\x1b[0m")
        while True:
            try:
                cmd = input("\x1b[38;5;226mLS>\x1b[0m ")
                if cmd.lower() in ["exit", "quit"]: break
                self.execute(cmd)
            except: break

if __name__ == "__main__":
    ls = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            for l in f: ls.execute(l)
    else: ls.repl()

class Lib: # Вспомогательный класс для net/rand
    def __init__(self, name, **kwargs):
        self.__dict__.update(kwargs)
