#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform, binascii

# Класс-контейнер для методов модуля
class Lib:
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__dict__.update(kwargs)
    def __repr__(self):
        return f"<LavaModule '{self.__name}'>"

class LavaScript:
    def __init__(self):
        self.version = "v0.4.1_MAGMA_GIANT"
        self.scope = {}
        self.start_time = time.time()

        # --- ВНУТРЕННИЕ УТИЛИТЫ ---
        def run_tm(args):
            try:
                p = subprocess.run(args, capture_output=True, text=True, timeout=3)
                return p.stdout.strip() if p.stdout else ""
            except: return ""

        def get_json(cmd):
            raw = run_tm(cmd)
            try: return json.loads(raw) if raw.startswith(("{","[")) else {}
            except: return {}

        # --- МОДУЛЬ: MATH (МАТЕМАТИКА) ---
        self.math = Lib("math",
            pi=math.pi, e=math.e, tau=math.tau,
            sqrt=math.sqrt, root=math.sqrt,
            pow=math.pow, abs=abs, mod=lambda x,y: x%y,
            ceil=math.ceil, floor=math.floor, round=round,
            sin=math.sin, cos=math.cos, tan=math.tan,
            log=math.log, log10=math.log10,
            fact=math.factorial, deg=math.degrees, rad=math.radians,
            is_nan=math.isnan, hypot=math.hypot, gcd=math.gcd
        )

        # --- МОДУЛЬ: FS (ФАЙЛОВАЯ СИСТЕМА) ---
        self.fs = Lib("fs",
            cwd=os.getcwd, path=os.path.abspath,
            ls=os.listdir, exists=os.path.exists,
            is_file=os.path.isfile, is_dir=os.path.isdir,
            size=os.path.getsize, home=lambda: os.path.expanduser("~"),
            read=lambda p: open(p, 'r', encoding='utf-8').read(),
            write=lambda p, d: open(p, 'w', encoding='utf-8').write(str(d)),
            append=lambda p, d: open(p, 'a', encoding='utf-8').write(str(d)),
            mkdir=lambda p: os.makedirs(p, exist_ok=True),
            rm=os.remove, rmdir=shutil.rmtree,
            copy=shutil.copy, move=shutil.move, rename=os.rename
        )

        # --- МОДУЛЬ: SYS (СИСТЕМА) ---
        self.sys = Lib("sys",
            ver=self.version, platform=sys.platform,
            os=platform.system(), arch=platform.machine(),
            clear=lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            sleep=time.sleep, exit=sys.exit,
            date=lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
            time=lambda: datetime.datetime.now().strftime("%H:%M:%S"),
            full_date=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            uptime=lambda: round(time.time() - self.start_time, 2),
            get_env=os.getenv, shell=lambda c: run_tm(c.split())
        )

        # --- МОДУЛЬ: CRYPTO (КРИПТОГРАФИЯ) ---
        self.crypto = Lib("crypto",
            md5=lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            sha1=lambda t: hashlib.sha1(str(t).encode()).hexdigest(),
            sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            sha512=lambda t: hashlib.sha512(str(t).encode()).hexdigest(),
            b64e=lambda t: base64.b64encode(str(t).encode()).decode(),
            b64d=lambda t: base64.b64decode(str(t)).decode(),
            crc32=lambda t: hex(binascii.crc32(str(t).encode()) & 0xffffffff)
        )

        # --- МОДУЛЬ: TERMUX (ANDROID API) ---
        self.termux = Lib("termux",
            battery=lambda: get_json(["termux-battery-status"]),
            toast=lambda m: subprocess.run(["termux-toast", str(m)]),
            vibrate=lambda d=200: subprocess.run(["termux-vibrate", "-d", str(d)]),
            torch=lambda s: subprocess.run(["termux-torch", "on" if s else "off"]),
            speak=lambda t: subprocess.run(["termux-tts-speak", str(t)]),
            clip_get=lambda: run_tm(["termux-clipboard-get"]),
            clip_set=lambda t: subprocess.run(["termux-clipboard-set", str(t)])
        )

        # --- МОДУЛЬ: GUI (ЦВЕТА) ---
        self.gui = Lib("gui",
            gold=lambda t: f"\x1b[33m{t}\x1b[0m", 
            red=lambda t: f"\x1b[31m{t}\x1b[0m",
            green=lambda t: f"\x1b[32m{t}\x1b[0m", 
            blue=lambda t: f"\x1b[34m{t}\x1b[0m",
            cyan=lambda t: f"\x1b[36m{t}\x1b[0m", 
            magenta=lambda t: f"\x1b[35m{t}\x1b[0m",
            bold=lambda t: f"\x1b[1m{t}\x1b[0m",
            bg_red=lambda t: f"\x1b[41m{t}\x1b[0m"
        )

        # --- МОДУЛЬ: NET (СЕТЬ) ---
        def net_get(url):
            try: return urllib.request.urlopen(url, timeout=5).read().decode()
            except: return "NetError"

        self.net = Lib("net",
            get=net_get,
            ping=lambda h: os.system(f"ping -c 1 {h} > /dev/null") == 0
        )

        # --- МОДУЛЬ: VAL (ДАННЫЕ) ---
        self.val = Lib("val",
            str=str, int=int, float=float, len=len,
            type=lambda x: type(x).__name__,
            upper=lambda t: str(t).upper(), lower=lambda t: str(t).lower(),
            json_p=json.loads, json_b=json.dumps,
            split=lambda t, s=" ": str(t).split(s),
            join=lambda l, s="": s.join(l)
        )

        # Глобальное окружение для Eval
        self.env = {
            "math": self.math, "fs": self.fs, "sys": self.sys,
            "crypto": self.crypto, "termux": self.termux,
            "gui": self.gui, "net": self.net, "val": self.val,
            "rand": Lib("rand", num=random.randint, choice=random.choice)
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
                res = eval(line[4:], {"__builtins__": None}, ctx)
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {res}")
                return
            eval(line, {"__builtins__": None}, ctx)
        except Exception as e:
            print(f"\x1b[31m[LS_ERROR]\x1b[0m {e}")

    def repl(self):
        self.sys.clear()
        print(f"🌋 LavaScript {self.version} (Magma Giant)")
        while True:
            try:
                line = input("\x1b[38;5;226mLS>\x1b[0m ")
                if line.lower() in ["exit", "quit"]: break
                self.execute(line)
            except: break

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            for l in f: engine.execute(l)
    else: engine.repl()
