#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64, shutil, datetime
from types import SimpleNamespace

class LavaScript:
    def __init__(self):
        self.version = "v0.2.2_MAGMA"
        self.scope = {}

        # Безопасный запуск команд оболочки
        def run_tm(cmd_list):
            try:
                res = subprocess.run(cmd_list, capture_output=True).stdout.decode().strip()
                return res if res else ""
            except: return ""

        # Фикс ошибки NoneType для батареи
        def get_bat():
            res = run_tm(["termux-battery-status"])
            try:
                data = json.loads(res) if res else {}
                return {
                    "percentage": data.get("percentage", 0),
                    "status": data.get("status", "Unknown"),
                    "health": data.get("health", "Good")
                }
            except:
                return {"percentage": 0, "status": "Error"}

        # --- СИСТЕМА МОДУЛЕЙ ---
        
        # 1. MATH (Добавлен .root)
        m_dict = {n: getattr(math, n) for n in dir(math) if not n.startswith("_")}
        m_dict["root"] = math.sqrt 

        # 2. FS (Добавлен .path)
        fs_dict = {
            "read": lambda p: open(p, 'r').read(),
            "write": lambda p, d: open(p, 'w').write(d),
            "exists": os.path.exists, "remove": os.remove, "ls": os.listdir,
            "cwd": os.getcwd, "path": os.path.abspath, "size": os.path.getsize
        }

        # 3. VAL & TYPES
        v_dict = {
            "str": str, "int": int, "dec": float, "bool": bool,
            "type": lambda x: type(x).__name__, "len": len,
            "upper": lambda t: str(t).upper(), "lower": lambda t: str(t).lower()
        }

        # 4. SYS & GUI
        sys_dict = {
            "exit": sys.exit, "sleep": time.sleep, "platform": sys.platform,
            "clear": lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        gui_dict = {
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m", "red": lambda t: f"\x1b[31m{t}\x1b[0m",
            "green": lambda t: f"\x1b[32m{t}\x1b[0m", "blue": lambda t: f"\x1b[34m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m"
        }

        self.env = {
            "math": SimpleNamespace(**m_dict), "fs": SimpleNamespace(**fs_dict),
            "val": SimpleNamespace(**v_dict), "sys": SimpleNamespace(**sys_dict),
            "gui": SimpleNamespace(**gui_dict), "termux": SimpleNamespace(battery=get_bat),
            "net": SimpleNamespace(get=lambda url: urllib.request.urlopen(url).read().decode()),
            "crypto": SimpleNamespace(sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest())
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
        print(f"\x1b[1;33mLavaScript {self.version}\x1b[0m")
        while True:
            try:
                line = input("\x1b[38;5;226mLS>\x1b[0m ")
                if line.lower() in ["exit", "quit"]: break
                self.execute(line)
            except (KeyboardInterrupt, EOFError): break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for l in f: engine.execute(l)
    else: engine.repl()
