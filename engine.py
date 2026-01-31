#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64

class Module:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class LavaScript:
    def __init__(self):
        self.version = "v0.2.6_CRYSTAL"
        self.scope = {}

        def run_tm(cmd):
            try:
                res = subprocess.run(cmd, capture_output=True, timeout=1).stdout.decode().strip()
                return json.loads(res) if res.startswith("{") else {}
            except: return {}

        # Математика (root теперь работает всегда)
        m_dict = {n: getattr(math, n) for n in dir(math) if not n.startswith("_")}
        m_dict["root"] = math.sqrt

        # Файлы
        fs_dict = {
            "path": os.path.abspath, "cwd": os.getcwd(),
            "ls": os.listdir, "exists": os.path.exists,
            "read": lambda p: open(p, 'r').read()
        }

        # Окружение
        self.env = {
            "math": Module(**m_dict),
            "fs": Module(**fs_dict),
            "val": Module(str=str, type=lambda x: type(x).__name__, int=int),
            "sys": Module(
                platform=sys.platform, 
                clear=lambda: os.system('clear' if os.name != 'nt' else 'cls'),
                date=lambda: time.ctime(), exit=sys.exit
            ),
            "gui": Module(
                gold=lambda t: f"\x1b[33m{t}\x1b[0m", 
                green=lambda t: f"\x1b[32m{t}\x1b[0m",
                bold=lambda t: f"\x1b[1m{t}\x1b[0m"
            ),
            "termux": Module(
                battery=lambda: run_tm(["termux-battery-status"]) or {"percentage": 0, "status": "N/A"},
                toast=lambda m: subprocess.run(["termux-toast", str(m)])
            ),
            "net": Module(get=lambda url: urllib.request.urlopen(url).read().decode())
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
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
                self.execute(line)
            except: break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for l in f: engine.execute(l)
    else: engine.repl()
