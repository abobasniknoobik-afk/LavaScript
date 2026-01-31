#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request, hashlib, json, base64, shutil, datetime
from types import SimpleNamespace

class LavaScript:
    def __init__(self):
        self.version = "v0.2_MAGMA"
        self.scope = {}
        
        # Вспомогательная функция для выполнения команд Termux
        def run_tm(cmd_list):
            try: return subprocess.run(cmd_list, capture_output=True).stdout.decode().strip()
            except: return "Termux API Error"

        # --- МОДУЛИ (Те самые 400+ команд) ---
        
        # 1. MATH (Полный набор)
        m_dict = {n: getattr(math, n) for n in dir(math) if not n.startswith("_")}
        
        # 2. VAL & TYPES
        v_dict = {
            "str": str, "int": int, "dec": float, "bool": bool,
            "lower": lambda t: str(t).lower(), "upper": lambda t: str(t).upper(),
            "split": lambda t, s=" ": str(t).split(s), "join": lambda l, s="": s.join(l),
            "replace": lambda t, o, n: str(t).replace(o, n),
            "type": lambda x: type(x).__name__, "hex": hex, "bin": bin,
            "len": len, "range": range
        }

        # 3. FS (Файловая система)
        fs_dict = {
            "read": lambda p: open(p, 'r').read(),
            "write": lambda p, d: open(p, 'w').write(d),
            "append": lambda p, d: open(p, 'a').write(d),
            "exists": os.path.exists, "remove": os.remove, "mkdir": os.mkdir,
            "rmdir": os.rmdir, "ls": os.listdir, "size": os.path.getsize,
            "copy": shutil.copy, "move": shutil.move, "cwd": os.getcwd,
            "path": os.path.abspath
        }

        # 4. SYS & TIME
        sys_dict = {
            "exit": sys.exit, "sleep": time.sleep, "now": lambda: time.ctime(),
            "ts": lambda: time.time(), "platform": sys.platform, "clear": lambda: os.system('clear'),
            "argv": sys.argv, "env": lambda k: os.getenv(k),
            "date": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 5. CRYPTO
        cr_dict = {
            "md5": lambda t: hashlib.md5(t.encode()).hexdigest(),
            "sha1": lambda t: hashlib.sha1(t.encode()).hexdigest(),
            "sha256": lambda t: hashlib.sha256(t.encode()).hexdigest(),
            "b64en": lambda t: base64.b64encode(t.encode()).decode(),
            "b64de": lambda t: base64.b64decode(t).decode()
        }

        # 6. NET
        net_dict = {
            "get": lambda url: urllib.request.urlopen(url, timeout=5).read().decode('utf-8'),
            "ping": lambda h: os.system(f"ping -c 1 {h} > /dev/null" if sys.platform != "win32" else f"ping -n 1 {h} > nul") == 0
        }

        # 7. TERMUX API
        tm_dict = {
            "toast": lambda m: run_tm(["termux-toast", str(m)]),
            "vibrate": lambda d=200: run_tm(["termux-vibrate", "-d", str(d)]),
            "speak": lambda t: run_tm(["termux-tts-speak", str(t)]),
            "battery": lambda: json.loads(run_tm(["termux-battery-status"])),
            "volume": lambda s, v: run_tm(["termux-volume", s, str(v)]),
            "brightness": lambda v: run_tm(["termux-brightness", str(v)]),
            "wifi": lambda: json.loads(run_tm(["termux-wifi-connectioninfo"])),
            "clipboard": lambda t=None: run_tm(["termux-clipboard-set", t]) if t else run_tm(["termux-clipboard-get"])
        }

        # 8. GUI & COLORS
        gui_dict = {
            "red": lambda t: f"\x1b[31m{t}\x1b[0m", 
            "green": lambda t: f"\x1b[32m{t}\x1b[0m",
            "blue": lambda t: f"\x1b[34m{t}\x1b[0m", 
            "gold": lambda t: f"\x1b[33m{t}\x1b[0m",
            "bold": lambda t: f"\x1b[1m{t}\x1b[0m",
            "underline": lambda t: f"\x1b[4m{t}\x1b[0m"
        }

        self.env = {
            "math": SimpleNamespace(**m_dict),
            "val": SimpleNamespace(**v_dict),
            "fs": SimpleNamespace(**fs_dict),
            "sys": SimpleNamespace(**sys_dict),
            "crypto": SimpleNamespace(**cr_dict),
            "net": SimpleNamespace(**net_dict),
            "termux": SimpleNamespace(**tm_dict),
            "gui": SimpleNamespace(**gui_dict),
            "json": SimpleNamespace(parse=json.loads, build=json.dumps),
            "rand": SimpleNamespace(num=random.randint, pick=random.choice, shuffle=random.shuffle)
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
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {eval(line[4:], {'__builtins__': None}, ctx)}")
                return
            if line.startswith("type "):
                res = eval(line[5:], {"__builtins__": None}, ctx)
                print(f"\x1b[38;5;111m[TYPE]\x1b[0m {type(res).__name__}")
                return
            eval(line, {"__builtins__": None}, ctx)
        except Exception as e:
            print(f"\x1b[31m[Error]\x1b[0m {e}")

    def repl(self):
        os.system('clear' if sys.platform != 'win32' else 'cls')
        print(f"\x1b[1;33mLavaScript {self.version}\x1b[0m")
        print("\x1b[38;5;244mInterpreter Ready. Type 'exit' to quit.\x1b[0m\n")
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
