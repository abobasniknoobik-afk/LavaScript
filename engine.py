#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform, binascii

class Lib:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class LavaScript:
    def __init__(self):
        self.version = "v0.4_MAGMA_OVERLOAD"
        self.scope = {}
        self.start_time = time.time()
        self.history = []

        # --- ВНУТРЕННИЕ СИСТЕМНЫЕ ВЫЗОВЫ ---
        def run_command(args):
            try:
                proc = subprocess.run(args, capture_output=True, text=True, timeout=5)
                return proc.stdout.strip() if proc.stdout else ""
            except: return ""

        def safe_json(raw):
            try: return json.loads(raw) if raw else {}
            except: return {}

        # --- МОДУЛЬ: MATH (МАТЕМАТИКА+) ---
        math_lib = Lib(
            pi=math.pi, e=math.e, tau=math.tau,
            sqrt=math.sqrt, root=math.sqrt, 
            sin=math.sin, cos=math.cos, tan=math.tan,
            asin=math.asin, acos=math.acos, atan=math.atan,
            ceil=math.ceil, floor=math.floor, round=round,
            log=math.log, log10=math.log10, exp=math.exp,
            pow=math.pow, abs=abs, mod=lambda x, y: x % y,
            fact=math.factorial, deg=math.degrees, rad=math.radians,
            hypot=math.hypot, gcd=math.gcd, is_nan=math.isnan
        )

        # --- МОДУЛЬ: FS (ФАЙЛОВЫЙ КОМБАЙН) ---
        fs_lib = Lib(
            cwd=os.getcwd, path=os.path.abspath, 
            ls=os.listdir, exists=os.path.exists,
            is_file=os.path.isfile, is_dir=os.path.isdir,
            mkdir=os.makedirs, rm=os.remove, rmdir=shutil.rmtree,
            size=os.path.getsize, ctime=os.path.getctime,
            read=lambda p: open(p, 'r', encoding='utf-8').read(),
            write=lambda p, d: open(p, 'w', encoding='utf-8').write(str(d)),
            append=lambda p, d: open(p, 'a', encoding='utf-8').write(str(d)),
            copy=shutil.copy, move=shutil.move,
            rename=os.rename, home=lambda: os.path.expanduser("~")
        )

        # --- МОДУЛЬ: SYS (ЯДРО СИСТЕМЫ) ---
        sys_lib = Lib(
            platform=sys.platform, os=platform.system(),
            arch=platform.machine(), node=platform.node(),
            ver=self.version, exit=sys.exit,
            sleep=time.sleep, clear=lambda: os.system('clear' if os.name != 'nt' else 'cls'),
            date=lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
            time=lambda: datetime.datetime.now().strftime("%H:%M:%S"),
            ts=time.time, uptime=lambda: time.time() - self.start_time,
            get_env=lambda k: os.getenv(k), set_env=lambda k, v: os.environ.update({k: v}),
            shell=lambda c: subprocess.run(c, shell=True, capture_output=True, text=True).stdout
        )

        # --- МОДУЛЬ: CRYPTO (БЕЗОПАСНОСТЬ) ---
        crypto_lib = Lib(
            md5=lambda t: hashlib.md5(str(t).encode()).hexdigest(),
            sha1=lambda t: hashlib.sha1(str(t).encode()).hexdigest(),
            sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            sha512=lambda t: hashlib.sha512(str(t).encode()).hexdigest(),
            b64e=lambda t: base64.b64encode(str(t).encode()).decode(),
            b64d=lambda t: base64.b64decode(str(t)).decode(),
            crc32=lambda t: format(binascii.crc32(str(t).encode()) & 0xFFFFFFFF, '08x'),
            hex_e=lambda t: binascii.hexlify(str(t).encode()).decode(),
            hex_d=lambda t: binascii.unhexlify(str(t)).decode()
        )

        # --- МОДУЛЬ: TERMUX (ANDROID API) ---
        tm_lib = Lib(
            battery=lambda: safe_json(run_command(["termux-battery-status"])),
            vibrate=lambda d=200: run_command(["termux-vibrate", "-d", str(d)]),
            toast=lambda m: run_command(["termux-toast", str(m)]),
            speak=lambda t: run_command(["termux-tts-speak", str(t)]),
            brightness=lambda v: run_command(["termux-brightness", str(v)]),
            volume=lambda s, v: run_command(["termux-volume", str(s), str(v)]),
            torch=lambda s: run_command(["termux-torch", "on" if s else "off"]),
            clip_get=lambda: run_command(["termux-clipboard-get"]),
            clip_set=lambda t: run_command(["termux-clipboard-set", str(t)]),
            wifi=lambda: safe_json(run_command(["termux-wifi-connectioninfo"])),
            contact=lambda: safe_json(run_command(["termux-contact-list"]))
        )

        # --- МОДУЛЬ: GUI (ОФОРМЛЕНИЕ) ---
        gui_lib = Lib(
            red=lambda t: f"\x1b[31m{t}\x1b[0m", green=lambda t: f"\x1b[32m{t}\x1b[0m",
            blue=lambda t: f"\x1b[34m{t}\x1b[0m", gold=lambda t: f"\x1b[33m{t}\x1b[0m",
            cyan=lambda t: f"\x1b[36m{t}\x1b[0m", bold=lambda t: f"\x1b[1m{t}\x1b[0m",
            magenta=lambda t: f"\x1b[35m{t}\x1b[0m", black=lambda t: f"\x1b[30m{t}\x1b[0m",
            white=lambda t: f"\x1b[37m{t}\x1b[0m", bg_red=lambda t: f"\x1b[41m{t}\x1b[0m",
            reset="\x1b[0m"
        )

        # --- МОДУЛЬ: VAL (ТИПЫ И ДАННЫЕ) ---
        val_lib = Lib(
            str=str, int=int, float=float, bool=bool, 
            type=lambda x: type(x).__name__, len=len,
            json_p=json.loads, json_b=json.dumps,
            upper=lambda t: str(t).upper(), lower=lambda t: str(t).lower(),
            split=lambda t, s=" ": str(t).split(s), join=lambda l, s="": s.join(l),
            replace=lambda t, o, n: str(t).replace(o, n),
            trim=lambda t: str(t).strip()
        )

        self.env = {
            "math": math_lib, "fs": fs_lib, "sys": sys_lib,
            "crypto": crypto_lib, "termux": tm_lib, "gui": gui_lib,
            "val": val_lib, "rand": Lib(num=random.randint, choice=random.choice)
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
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"\x1b[1;33m🌋 LavaScript {self.version}\x1b[0m")
        while True:
            try:
                line = input("\x1b[38;5;226mLS>\x1b[0m ")
                if line.lower() in ["exit", "quit", "sys.exit()"]: break
                self.execute(line)
            except: break

if __name__ == "__main__":
    ls = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            for l in f: ls.execute(l)
    else: ls.repl()
