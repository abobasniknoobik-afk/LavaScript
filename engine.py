#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request

class LSModule:
    def __init__(self, **funcs):
        self.__dict__.update(funcs)

class LavaScript:
    def __init__(self):
        self.version = "v0.1_TEST"
        self.global_scope = {}
        
        # Модули
        self.modules = {
            "val": LSModule(str=str, int=int, dec=float, kind=lambda x: type(x).__name__),
            "math": LSModule(root=math.sqrt, exp=pow, up=math.ceil, down=math.floor, total=sum),
            "sys": LSModule(
                size=len, path=os.getcwd, scan=os.listdir, now=lambda: time.ctime(),
                pause=time.sleep, clear=lambda: os.system('clear'),
                info=lambda: print(f"\033[1;35mLavaScript v{self.version}\033[0m on {sys.platform}")
            ),
            "gui": LSModule(
                red=lambda t: f"\033[31m{t}\033[0m",
                green=lambda t: f"\033[32m{t}\033[0m",
                blue=lambda t: f"\033[34m{t}\033[0m",
                gold=lambda t: f"\033[33m{t}\033[0m"
            ),
            "net": LSModule(get=lambda url: urllib.request.urlopen(url).read().decode('utf-8')),
            "termux": LSModule(
                toast=lambda m: subprocess.run(["termux-toast", str(m)]),
                vibrate=lambda ms: subprocess.run(["termux-vibrate", "-d", str(ms)])
            )
        }

    def safe_eval(self, code, scope):
        if not code.strip(): return ""
        # Создаем чистое окружение
        env = {**self.modules, **scope}
        try:
            return eval(code, {"__builtins__": None}, env)
        except Exception as e:
            return f"<Error: {e}>"

    def run_line(self, line, scope):
        line = line.strip()
        if not line or line.startswith("#"): return

        # Логика LET (let x = выражение)
        if line.startswith("let "):
            match = re.match(r'^let\s+(\w+)\s*=\s*(.*)$', line)
            if match:
                var_name, expr = match.groups()
                scope[var_name] = self.safe_eval(expr, scope)
            return

        # Логика OUT (out выражение)
        if line.startswith("out "):
            expr = line[4:].strip()
            print(f"\033[38;5;208m[LAVA]\033[0m {self.safe_eval(expr, scope)}")
            return

        # Логика TYPE (type выражение)
        if line.startswith("type "):
            expr = line[5:].strip()
            val = self.safe_eval(expr, scope)
            print(f"\033[38;5;111m[TYPE]\033[0m {type(val).__name__}")
            return

        # Просто вызов (например sys.info())
        self.safe_eval(line, scope)

    def repl(self):
        print(f"\033[1;33mLavaScript {self.version}\033[0m (Interactive REPL)")
        while True:
            try:
                line = input("\033[38;5;226mLS>\033[0m ")
                if line.lower() in ["exit", "quit"]: break
                self.run_line(line, self.global_scope)
            except (KeyboardInterrupt, EOFError): break
            except Exception as e: print(f"Runtime Error: {e}")

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version": print(f"LavaScript {engine.version}")
        else:
            with open(sys.argv[1], 'r') as f:
                for line in f: engine.run_line(line, engine.global_scope)
    else: engine.repl()
