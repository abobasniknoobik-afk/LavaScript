#!/usr/bin/env python3
import sys, os, re, math, time, subprocess, random, urllib.request

class LSModule:
    def __init__(self, **funcs):
        self.__dict__.update(funcs)

class LavaScript:
    def __init__(self):
        self.version = "v0.1_TEST"
        
        # Модуль для работы с цветом и текстом
        def color_text(code, text): return f"\033[{code}m{text}\033[0m"
        
        self.ctx = {
            "val": LSModule(
                str=str, int=int, dec=float, logic=bool, 
                kind=lambda x: type(x).__name__, 
                type=lambda x: print(f"Type: {type(x).__name__}") # Твоя идея с type!
            ),
            "math": LSModule(root=math.sqrt, exp=pow, up=math.ceil, down=math.floor, total=sum),
            "sys": LSModule(
                size=len, path=os.getcwd, scan=os.listdir, 
                now=lambda: time.ctime(), pause=time.sleep,
                clear=lambda: os.system('clear'), # Очистка экрана
                info=lambda: print(f"LavaScript v{self.version} on {sys.platform}")
            ),
            "gui": LSModule(
                red=lambda t: color_text("31", t),
                green=lambda t: color_text("32", t),
                blue=lambda t: color_text("34", t),
                gold=lambda t: color_text("33", t)
            ),
            "net": LSModule(get=lambda url: urllib.request.urlopen(url).read().decode('utf-8')),
            "termux": LSModule(
                toast=lambda m: subprocess.run(["termux-toast", str(m)]),
                vibrate=lambda ms: subprocess.run(["termux-vibrate", "-d", str(ms)])
            ),
            "rand": LSModule(num=random.randint, select=random.choice)
        }
        self.global_scope = {}

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code)
        pattern = r'(\{|\}|\[|\]|\(|\)|,|<<|>>|==|!=|>=|<=|[=+\-*/:]|[\w\.]+|"[^"]*")'
        tokens = []
        for line in code.split('\n'):
            line = line.strip()
            if not line: continue
            t = re.findall(pattern, line)
            if t: tokens.append(t)
        return tokens

    def parse_structure(self, tokens):
        res, i = [], 0
        while i < len(tokens):
            line = tokens[i]
            if "{" in line:
                block, bal, i = [], 1, i + 1
                while i < len(tokens) and bal > 0:
                    if "{" in tokens[i]: bal += 1
                    if "}" in tokens[i]: bal -= 1
                    if bal > 0: block.append(tokens[i])
                    i += 1
                res.append({"type": "block", "header": line, "body": self.parse_structure(block)})
            else:
                res.append({"type": "statement", "content": line})
                i += 1
        return res

    def safe_eval(self, expr_list, scope):
        expr = " ".join(expr_list).replace("true", "True").replace("false", "False")
        try:
            full_ctx = {**self.ctx, **scope}
            return eval(expr, {"__builtins__": None}, full_ctx)
        except Exception as e: return f"<Error: {e}>"

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd or len(cmd) == 0: continue
                if cmd[0] == "out":
                    res = self.safe_eval(cmd[1:], scope)
                    print(f"\033[38;5;208m[LAVA]\033[0m {res}")
                elif cmd[0] == "let":
                    if "=" in cmd:
                        idx = cmd.index("=")
                        var_name = cmd[1]
                        scope[var_name] = self.safe_eval(cmd[idx+1:], scope)
            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "while":
                    while bool(self.safe_eval(h[1:], scope)): self.run(node["body"], scope)
                elif h[0] == "if":
                    if bool(self.safe_eval(h[1:], scope)): self.run(node["body"], scope)

    def start(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), self.global_scope)

    def repl(self):
        print(f"LavaScript {self.version} (Interactive REPL)")
        while True:
            try:
                line = input("\033[38;5;226mLS>\033[0m ")
                if line.lower() in ["exit", "quit"]: break
                if not line.strip(): continue
                self.run(self.parse_structure(self.tokenize(line)), self.global_scope)
            except (KeyboardInterrupt, EOFError): break
            except Exception as e: print(f"System Error: {e}")

if __name__ == "__main__":
    engine = LavaScript()
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version": print(f"LavaScript {engine.version}")
        else: engine.start(sys.argv[1])
    else: engine.repl()
