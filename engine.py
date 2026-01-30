#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request

class LavaScript:
    def __init__(self):
        self.version = "v0.1_TEST"
        self.global_scope = {}
        
        # Модули в виде словарей (самый стабильный вариант для eval)
        self.modules = {
            "val": {"str": str, "int": int, "dec": float, "kind": lambda x: type(x).__name__},
            "math": {"root": math.sqrt, "exp": pow, "up": math.ceil, "down": math.floor, "total": sum},
            "sys": {
                "size": len, "path": os.getcwd, "scan": os.listdir, "now": lambda: time.ctime(),
                "pause": time.sleep, "clear": lambda: os.system('clear'),
                "info": lambda: print(f"\x1b[1;35mLavaScript v{self.version}\x1b[0m on {sys.platform}")
            },
            "gui": {
                "red": lambda t: f"\x1b[31m{t}\x1b[0m",
                "green": lambda t: f"\x1b[32m{t}\033[0m",
                "blue": lambda t: f"\x1b[34m{t}\x1b[0m",
                "gold": lambda t: f"\x1b[33m{t}\x1b[0m"
            },
            "net": {"get": lambda url: urllib.request.urlopen(url).read().decode('utf-8')},
            "termux": {
                "toast": lambda m: subprocess.run(["termux-toast", str(m)]),
                "vibrate": lambda ms: subprocess.run(["termux-vibrate", "-d", str(ms)])
            }
        }

    def safe_eval(self, code, scope):
        code = code.strip()
        if not code: return ""
        # Объединяем модули и переменные
        env = {**self.modules, **scope}
        try:
            # Превращаем словари в объекты "на лету" через SimpleNamespace для поддержки точки
            from types import SimpleNamespace
            for key in self.modules:
                if isinstance(self.modules[key], dict):
                    env[key] = SimpleNamespace(**self.modules[key])
            
            return eval(code, {"__builtins__": None}, env)
        except Exception as e:
            return f"<Error: {e}>"

    def run_line(self, line, scope):
        line = line.strip()
        if not line or line.startswith("#"): return

        if line.startswith("let "):
            match = re.match(r'^let\s+(\w+)\s*=\s*(.*)$', line)
            if match:
                var_name, expr = match.groups()
                scope[var_name] = self.safe_eval(expr, scope)
            return

        if line.startswith("out "):
            expr = line[4:].strip()
            print(f"\x1b[38;5;208m[LAVA]\x1b[0m {self.safe_eval(expr, scope)}")
            return

        if line.startswith("type "):
            expr = line[5:].strip()
            val = self.safe_eval(expr, scope)
            print(f"\x1b[38;5;111m[TYPE]\x1b[0m {type(val).__name__}")
            return

        self.safe_eval(line, scope)

    def repl(self):
        print(f"\x1b[1;33mLavaScript {self.version}\x1b[0m (Interactive REPL)")
        while True:
            try:
                line = input("\x1b[38;5;226mLS>\x1b[0m ")
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
