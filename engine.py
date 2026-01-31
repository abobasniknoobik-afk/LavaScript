#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64, shutil, datetime
from types import SimpleNamespace

class LavaScript:
    def __init__(self):
        self.version = "v0.2.1_MAGMA"
        self.scope = {}

        # --- ВНУТРЕННИЕ УТИЛИТЫ ---
        def run_tm(cmd_list):
            try:
                res = subprocess.run(cmd_list, capture_output=True).stdout.decode().strip()
                return res if res else ""
            except: return ""

        def get_bat():
            res = run_tm(["termux-battery-status"])
            try: return json.loads(res) if res else {"percentage": 0, "status": "N/A"}
            except: return {"percentage": 0, "status": "Error"}

        # --- СБОРКА МОДУЛЕЙ ---
        
        # 1. MATH (Добавлен .root для совместимости)
        m_dict = {n: getattr(math, n) for n in dir(math) if not n.startswith("_")}
        m_dict["root"] = math.sqrt 

        # 2. VAL & TYPES (Обработка данных)
        v_dict = {
            "str": str, "int": int, "dec": float, "bool": bool, "len": len,
            "lower": lambda t: str(t).lower(), "upper": lambda t: str(t).upper(),
            "type": lambda x: type(x).__name__, "hex": hex, "bin": bin,
            "split": lambda t, s=" ": str(t).split(s), "join": lambda l, s="": s.join(l)
        }

        # 3. FS (Файловая система + Исправленный .path)
        fs_dict = {
            "read": lambda p: open(p, 'r').read(),
            "write": lambda p, d: open(p, 'w').write(d),
            "exists": os.path.exists, "remove": os.remove, "ls": os.listdir,
            "cwd": os.getcwd, "mkdir": os.mkdir, "size": os.path.getsize,
            "path": os.path.abspath, "copy": shutil.copy, "move": shutil.move
        }

        # 4. SYS & TIME
        sys_dict = {
            "exit": sys.exit, "sleep": time.sleep, "clear": lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            "platform": sys.platform, "now": lambda: time.ctime(),
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 5. NET & CRYPTO
        net_dict = {
            "get": lambda url: urllib.request.urlopen(url, timeout=5).read().decode('utf-8'),
            "ping": lambda h: os.system(f"ping -c 1 {h} > /dev/null" if os.name != 'nt' else f"ping -n 1 {h} > nul") == 0
        }
        cr_dict = {
            "sha256": lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            "md5": lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            "b64en": lambda t: base64.b64encode(str(t).encode()).decode()
        }

        # 6. TERMUX & GUI
        tm_dict = {
            "toast": lambda m: run_tm(["termux-toast", str(m)]),
            "vibrate": lambda d=200: run_tm(["termux-vibrate", "-d", str(d)]),
            "battery": get_bat,
            "speak": lambda t: run_tm(["termux-tts-speak", str(t)]),
            "clipboard": lambda t=None: run_tm(["termux-clipboard-set", t]) if t else run_tm(["termux-clipboard-get"])
        }
        gui_dict = {
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m", "red": lambda t: f"\x1b[31m{t}\x1b[0m",
            "green": lambda t: f"\x1b[32m{t}\x1b[0m", "blue": lambda t: f"\x1b[34m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m"
        }

        # Глобальное окружение
        self.env = {
            "math": SimpleNamespace(**m_dict), "val": SimpleNamespace(**v_dict),
            "fs": SimpleNamespace(**fs_dict), "sys": SimpleNamespace(**sys_dict),
            "net": SimpleNamespace(**net_dict), "crypto": SimpleNamespace(**cr_dict),
            "termux": SimpleNamespace(**tm_dict), "gui": SimpleNamespace(**gui_dict),
            "rand": SimpleNamespace(num=random.randint, pick=random.choice)
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
