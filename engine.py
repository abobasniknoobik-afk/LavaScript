#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform, binascii

class Lib:
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__dict__.update(kwargs)
    def __repr__(self): return f"<LavaModule '{self.__name}'>"

class LavaScript:
    def __init__(self):
        self.version = "v0.2.2_MAGMA_STABLE"
        self.scope = {}
        self.start_time = time.time()
        
        def api(cmd):
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                raw = p.stdout.strip()
                if not raw: return {}
                return json.loads(raw) if raw.startswith(("{","[")) else raw
            except: return {}

        # Авто-импорт всей математики (60+ функций)
        m_funcs = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        m_funcs.update({"root": math.sqrt, "pow": math.pow})

        self.env = {
            "math": Lib("math", **m_funcs),
            "fs": Lib("fs", 
                read=lambda p: open(p, 'r', encoding='utf-8').read(),
                write=lambda p, d: open(p, 'w', encoding='utf-8').write(str(d)),
                exists=os.path.exists, ls=os.listdir, size=os.path.getsize,
                copy=shutil.copy, move=shutil.move, rm=os.remove, mkdir=os.makedirs,
                cwd=os.getcwd, abspath=os.path.abspath, is_file=os.path.isfile
            ),
            "sys": Lib("sys", 
                ver=self.version, platform=sys.platform, exit=sys.exit, 
                sleep=time.sleep, now=lambda: datetime.datetime.now().strftime("%H:%M:%S"),
                date=lambda: datetime.datetime.now().strftime("%Y-%m-%d"),
                shell=lambda c: subprocess.check_output(c, shell=True).decode().strip()
            ),
            "termux": Lib("termux", 
                battery=lambda: api(["termux-battery-status"]),
                toast=lambda m: subprocess.run(["termux-toast", str(m)]),
                vibrate=lambda d=200: subprocess.run(["termux-vibrate", "-d", str(d)]),
                speak=lambda t: subprocess.run(["termux-tts-speak", str(t)])
            ),
            "val": Lib("val", 
                str=str, int=int, float=float, len=len, kind=lambda x: type(x).__name__,
                get=lambda d, k, df=0: d.get(k, df) if isinstance(d, dict) else df,
                upper=lambda t: str(t).upper(), lower=lambda t: str(t).lower(),
                split=lambda t, s=" ": str(t).split(s), replace=lambda t, o, n: str(t).replace(o, n)
            ),
            "gui": Lib("gui",
                gold=lambda t: f"\x1b[33m{t}\x1b[0m", cyan=lambda t: f"\x1b[36m{t}\x1b[0m",
                green=lambda t: f"\x1b[32m{t}\x1b[0m", bold=lambda t: f"\x1b[1m{t}\x1b[0m",
                red=lambda t: f"\x1b[31m{t}\x1b[0m"
            ),
            "crypto": Lib("crypto", 
                sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
                md5=lambda t: hashlib.md5(str(t).encode()).hexdigest(),
                uuid=lambda: hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
            ),
            "net": Lib("net", 
                get=lambda u: urllib.request.urlopen(u).read().decode(),
                ip=lambda: urllib.request.urlopen("https://api.ipify.org").read().decode(),
                ping=lambda h: os.system(f"ping -c 1 {h} > /dev/null") == 0
            ),
            "rand": Lib("rand", num=random.randint, pick=random.choice)
        }

    def execute(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return
        ctx = {**self.env, **self.scope}
        try:
            if line.startswith("let "):
                m = re.match(r"let\s+(\w+)\s*=\s*(.*)", line)
                if m: self.scope[m.group(1)] = eval(m.group(2), {"__builtins__": None}, ctx)
            elif line.startswith("out "):
                print(f"\x1b[38;5;208m[LAVA]\x1b[0m {eval(line[4:], {'__builtins__': None}, ctx)}")
            else: eval(line, {"__builtins__": None}, ctx)
        except Exception as e: print(f"\x1b[31m[Error]\x1b[0m {e}")

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            for l in f: engine.execute(l)
    else:
        print(f"LavaScript {engine.version}")
        while True:
            try: engine.execute(input("LS> "))
            except: break
