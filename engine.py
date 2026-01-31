import sys, os, re, math, time, subprocess, random, urllib.request
import hashlib, json, base64, shutil, datetime, platform, binascii

class Lib:
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__dict__.update(kwargs)
    def __repr__(self): return f"<LavaModule '{self.__name}'>"

class LavaScript:
    def __init__(self):
        self.version = "v0.2_MAGMA"
        self.scope = {}
        
        # Авто-заполнение math (60+ функций)
        math_funcs = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        math_funcs["root"] = math.sqrt
        
        # API Termux
        def api(cmd):
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                return json.loads(p.stdout) if p.stdout.strip().startswith(("{","[")) else p.stdout.strip()
            except: return {}

        self.env = {
            "math": Lib("math", **math_funcs),
            "fs": Lib("fs", read=lambda p: open(p, 'r').read(), write=lambda p, d: open(p, 'w').write(str(d)), 
                     ls=os.listdir, exists=os.path.exists, rm=os.remove, mkdir=os.makedirs,
                     size=os.path.getsize, copy=shutil.copy, move=shutil.move, cwd=os.getcwd),
            "termux": Lib("termux", battery=lambda: api(["termux-battery-status"]), toast=lambda m: api(["termux-toast", str(m)]),
                         vibrate=lambda d: api(["termux-vibrate", "-d", str(d)]), speak=lambda t: api(["termux-tts-speak", str(t)])),
            "val": Lib("val", str=str, int=int, kind=lambda x: type(x).__name__, 
                      upper=lambda t: str(t).upper(), lower=lambda t: str(t).lower(), 
                      split=lambda t, s=" ": str(t).split(s), replace=lambda t, o, n: str(t).replace(o, n)),
            "sys": Lib("sys", ver=self.version, exit=sys.exit, sleep=time.sleep, clear=lambda: os.system('clear'),
                      now=lambda: datetime.datetime.now().strftime("%H:%M:%S")),
            "crypto": Lib("crypto", sha256=lambda t: hashlib.sha256(str(t).encode()).hexdigest(), md5=lambda t: hashlib.md5(str(t).encode()).hexdigest()),
            "net": Lib("net", get=lambda u: urllib.request.urlopen(u).read().decode(), ping=lambda h: os.system(f"ping -c 1 {h} > /dev/null") == 0),
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
        except Exception as e: print(f"\x1b[31m[LS_ERROR]\x1b[0m {e}")

if __name__ == "__main__":
    ls = LavaScript()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for l in f: ls.execute(l)
