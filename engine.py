#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64

class Module:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class LavaScript:
    def __init__(self):
        self.version = "v0.2.5_SOLID"
        self.scope = {}

        # Безопасный вызов Termux
        def run_tm(cmd_list):
            try:
                p = subprocess.run(cmd_list, capture_output=True, timeout=2)
                return p.stdout.decode().strip()
            except: return ""

        # Безопасная батарея
        def get_bat():
            raw = run_tm(["termux-battery-status"])
            try:
                data = json.loads(raw) if raw.startswith("{") else {}
                return {"percentage": data.get("percentage", 0), "status": data.get("status", "N/A")}
            except: return {"percentage": 0, "status": "Error"}

        # Инициализация модулей как объектов классов
        self.env = {
            "math": Module(
                pi=math.pi, sqrt=math.sqrt, root=math.sqrt, sin=math.sin
            ),
            "fs": Module(
                cwd=os.getcwd, path=os.path.abspath, ls=os.listdir,
                exists=os.path.exists, read=lambda p: open(p, 'r').read()
            ),
            "val": Module(
                str=str, int=int, type=lambda x: type(x).__name__,
                upper=lambda t: str(t).upper(), lower=lambda t: str(t).lower()
            ),
            "sys": Module(
                clear=lambda: os.system('clear' if os.name != 'nt' else 'cls'),
                exit=sys.exit, platform=sys.platform, date=lambda: time.ctime()
            ),
            "gui": Module(
                gold=lambda t: f"\x1b[33m{t}\x1b[0m", red=lambda t: f"\x1b[31m{t}\x1b[0m",
                green=lambda t: f"\x1b[32m{t}\x1b[0m", bold=lambda t: f"\x1b[1m{t}\x1b[0m"
            ),
            "termux": Module(
                battery=get_bat,
                vibrate=lambda d=200: run_tm(["termux-vibrate", "-d", str(d)]),
                toast=lambda m: run_tm(["termux-toast", str(m)])
            ),
            "net": Module(
                get=lambda url: urllib.request.urlopen(url).read().decode()
            )
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        # Теперь eval точно увидит атрибуты классов через точку
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
