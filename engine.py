import sys, os, re, math, time, subprocess, random

class LSModule:
    def __init__(self, **funcs):
        self.__dict__.update(funcs)

class LavaScript:
    def __init__(self):
        self.ctx = {
            "val": LSModule(
                str=str, int=int, dec=float, logic=bool,
                kind=lambda x: type(x).__name__, module=abs,
                to_hex=hex, to_bin=bin, code=ord, char=chr,
                all=all, any=any, ascii=ascii, complex=complex,
                bytes=bytes, bytearray=bytearray, is_inst=isinstance,
                is_sub=issubclass
            ),
            "math": LSModule(
                root=math.sqrt, exp=pow, up=math.ceil, down=math.floor,
                sin=math.sin, cos=math.cos, log=math.log, fix=round,
                total=sum, peak=max, base=min, divmod=divmod
            ),
            "sys": LSModule(
                size=len, step=range, link=enumerate, halt=sys.exit,
                pause=time.sleep, path=os.getcwd, scan=os.listdir,
                env=sys.platform, now=lambda: time.ctime(), id=id,
                rev=reversed, sort=sorted, iter=iter, next=next,
                map=map, filter=filter, zip=zip
            ),
            "rand": LSModule(
                num=random.randint, select=random.choice, chaos=random.shuffle
            ),
            "io": LSModule(
                out=print, get=input, file=open, inject=eval, 
                run=exec, inspect=dir, vars=vars, loc=locals, glob=globals
            ),
            "list": list, "dict": dict, "set": set, "tuple": tuple
        }
        self.functions = {}
        self.includes = set()

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
        except Exception as e:
            return f"<Error: {e}>"

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                if cmd[0] == "out":
                    res = self.safe_eval(cmd[1:], scope)
                    print(f"\033[38;5;208m[LAVA]\033[0m {res}")
                elif cmd[0] == "let":
                    if "=" in cmd:
                        var_name = cmd[1]
                        scope[var_name] = self.safe_eval(cmd[cmd.index("=")+1:], scope)
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)
            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "while":
                    while bool(self.safe_eval(h[1:], scope)):
                        self.run(node["body"], scope)
                elif h[0] == "if":
                    if bool(self.safe_eval(h[1:], scope)):
                        self.run(node["body"], scope)
                elif h[0] == "fn":
                    name = h[1]
                    s, e = h.index("(")+1, h.index(")")
                    self.functions[name] = {"args": [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()], "body": node["body"]}

    def start(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), {})

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
