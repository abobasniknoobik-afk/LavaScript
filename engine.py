#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request
from types import SimpleNamespace

class LavaScript:
    def __init__(self):
        self.version = "v0.1_TEST"
        self.scope = {}
        
        # Функции модулей
        def get_net(url):
            try:
                with urllib.request.urlopen(url, timeout=5) as r:
                    return r.read().decode('utf-8')
            except: return "Net Error"

        # Инициализация окружения (Модули)
        self.env = {
            "math": SimpleNamespace(root=math.sqrt, exp=pow, up=math.ceil, down=math.floor, total=sum),
            "val": SimpleNamespace(str=str, int=int, dec=float, kind=lambda x: type(x).__name__),
            "sys": SimpleNamespace(
                path=os.getcwd, scan=os.listdir, now=lambda: time.ctime(),
                pause=time.sleep, clear=lambda: os.system('clear'),
                info=lambda: print(f"\033[1;35mLavaScript {self.version}\033[0m")
            ),
            "gui": SimpleNamespace(
                red=lambda t: f"\033[31m{t}\033[0m",
                green=lambda t: f"\033[32m{t}\033[0m",
                blue=lambda t: f"\033[34m{t}\033[0m",
                gold=lambda t: f"\033[33m{t}\033[0m"
            ),
            "net": SimpleNamespace(get=get_net),
            "termux": SimpleNamespace(
                toast=lambda m: subprocess.run(["termux-toast", str(m)]),
                vibrate=lambda ms: subprocess.run(["termux-vibrate", "-d", str(ms)])
            )
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return

        # Собираем контекст для исполнения
        context = {**self.env, **self.scope}

        try:
            # Логика LET
            if line.startswith("let "):
                m = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if m:
                    name, expr = m.groups()
                    self.scope[name] = eval(expr, {"__builtins__": None}, context)
                return

            # Логика OUT
            if line.startswith("out "):
                expr = line[4:].strip()
                result = eval(expr, {"__builtins__": None}, context)
                print(f"\033[38;5;208m[LAVA]\033[0m {result}")
                return

            # Логика TYPE
            if line.startswith("type "):
                expr = line[5:].strip()
                result = eval(expr, {"__builtins__": None}, context)
                print(f"\033[38;5;111m[TYPE]\033[0m {type(result).__name__}")
                return

            # Прямой вызов функций (sys.info() и т.д.)
            eval(line, {"__builtins__": None}, context)

        except Exception as e:
            print(f"\033[31m[Error]\033[0m {e}")

    def repl(self):
        print(f"\033[1;33mLavaScript {self.version}\033[0m (Interactive REPL)")
        while True:
            try:
                line = input("\033[38;5;226mLS>\033[0m ")
                if line.lower() in ["exit", "quit"]: break
                self.execute(line)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version":
            print(f"LavaScript {engine.version}")
        else:
            if os.path.exists(sys.argv[1]):
                with open(sys.argv[1], 'r') as f:
                    for l in f: engine.execute(l)
    else:
        engine.repl()
