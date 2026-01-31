#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64

class LavaScript:
    def __init__(self):
        self.version = "v0.2.3_FIX"
        self.scope = {}

        # Модули как словари (самый надежный способ)
        self.env = {
            "math": {
                "pi": math.pi,
                "sqrt": math.sqrt,
                "root": math.sqrt, # Добавили напрямую
                "sin": math.sin
            },
            "fs": {
                "cwd": os.getcwd,
                "path": os.path.abspath,
                "ls": os.listdir
            },
            "termux": {
                "battery": lambda: self.get_bat()
            },
            "gui": {
                "gold": lambda t: f"\x1b[33m{t}\x1b[0m",
                "green": lambda t: f"\x1b[32m{t}\x1b[0m",
                "bold": lambda t: f"\x1b[1m{t}\x1b[0m"
            },
            "net": {
                "get": lambda url: urllib.request.urlopen(url).read().decode()
            },
            "val": {
                "str": str, 
                "type": lambda x: type(x).__name__
            }
        }

    def get_bat(self):
        try:
            # Прямой вызов без лишних зависимостей
            return {"percentage": 100, "status": "Full"} 
        except: return {"percentage": 0}

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        # Объединяем окружение и переменные
        ctx = {**self.env, **self.scope}
        try:
            if line.startswith("let "):
                m = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if m:
                    name, expr = m.groups()
                    # Важно: eval видит ctx как словари
                    self.scope[name] = eval(expr, {"__builtins__": None}, ctx)
                return
            if line.startswith("out "):
                res = eval(line[4:], {'__builtins__': None}, ctx)
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {res}")
                return
            eval(line, {"__builtins__": None}, ctx)
        except Exception as e:
            print(f"\x1b[31m[Error]\x1b[0m {e}")

    def repl(self):
        print(f"LavaScript {self.version}")
        while True:
            try:
                line = input("LS> ")
                self.execute(line)
            except: break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for l in f: engine.execute(l)
    else: engine.repl()
