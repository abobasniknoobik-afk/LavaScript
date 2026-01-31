#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64, shutil, datetime
from types import SimpleNamespace

class LavaScript:
    def __init__(self):
        self.version = "v0.2.4_CRYSTAL"
        self.scope = {}

        # Внутренняя функция для Termux
        def run_tm(cmd_list):
            try:
                res = subprocess.run(cmd_list, capture_output=True).stdout.decode().strip()
                return res if res else ""
            except: return ""

        # Модуль MATH
        m_dict = {n: getattr(math, n) for n in dir(math) if not n.startswith("_")}
        m_dict["root"] = math.sqrt

        # Модуль FS
        fs_dict = {
            "read": lambda p: open(p, 'r').read(),
            "write": lambda p, d: open(p, 'w').write(d),
            "exists": os.path.exists,
            "remove": os.remove,
            "cwd": os.getcwd,
            "path": os.path.abspath,
            "ls": os.listdir
        }

        # Модуль TERMUX (Безопасный)
        def get_bat():
            res = run_tm(["termux-battery-status"])
            try:
                d = json.loads(res) if res else {}
                return {"percentage": d.get("percentage", 0), "status": d.get("status", "N/A")}
            except: return {"percentage": 0, "status": "Error"}

        # Модуль VAL
        v_dict = {
            "str": str, "int": int, "type": lambda x: type(x).__name__,
            "upper": lambda t: str(t).upper(), "lower": lambda t: str(t).lower()
        }

        # Окружение
        self.env = {
            "math": SimpleNamespace(**m_dict),
            "fs": SimpleNamespace(**fs_dict),
            "val": SimpleNamespace(**v_dict),
            "sys": SimpleNamespace(
                clear=lambda: os.system('clear' if os.name != 'nt' else 'cls'),
                exit=sys.exit, platform=sys.platform, date=lambda: time.ctime()
            ),
            "gui": SimpleNamespace(
                gold=lambda t: f"\x1b[33m{t}\x1b[0m", red=lambda t: f"\x1b[31m{t}\x1b[0m",
                green=lambda t: f"\x1b[32m{t}\x1b[0m", bold=lambda t: f"\x1b[1m{t}\x1b[0m"
            ),
            "termux": SimpleNamespace(
                battery=get_bat,
                toast=lambda m: run_tm(["termux-toast", str(m)]),
                vibrate=lambda d=200: run_tm(["termux-vibrate", "-d", str(d)])
            ),
            "net": SimpleNamespace(get=lambda url: urllib.request.urlopen(url).read().decode()),
            "crypto": SimpleNamespace(sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest())
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        # Важно: Eval должен видеть модули как переменные
        ctx = {**self.env, **self.scope}
        try:
            if line.startswith("let "):
                m = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if m:
                    name, expr = m.groups()
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
                if line.lower() in ["exit", "quit"]: break
                self.execute(line)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for l in f: engine.execute(l)
    else: engine.repl()
