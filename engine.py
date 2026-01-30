import sys, os, re, math, time, subprocess, random

# Специальный класс для создания департаментов LS
class LSDepartment:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class LavaScript:
    def __init__(self):
        # Группируем всё в реальные объекты для чистого синтаксиса через точку
        self.val = LSDepartment(
            str=str, int=int, dec=float, logic=bool,
            kind=lambda x: type(x).__name__, module=abs,
            to_hex=hex, to_bin=bin, code=ord, char=chr
        )
        self.math = LSDepartment(
            root=math.sqrt, exp=pow, up=math.ceil, down=math.floor,
            sin=math.sin, cos=math.cos, log=math.log, fix=round,
            total=sum, peak=max, base=min
        )
        self.sys = LSDepartment(
            size=len, step=range, link=enumerate, halt=sys.exit,
            pause=time.sleep, path=os.getcwd, scan=os.listdir,
            env=sys.platform, now=lambda: time.ctime(), id=id,
            rev=reversed, sort=sorted
        )
        self.rand = LSDepartment(
            num=random.randint, select=random.choice, chaos=random.shuffle
        )
        self.io = LSDepartment(
            out=print, get=input, file=open, inject=eval,
            inspect=dir, vars=vars
        )
        
        # Базовый словарь для eval
        self.base_ctx = {
            "val": self.val, "math": self.math, "sys": self.sys,
            "rand": self.rand, "io": self.io,
            "list": list, "dict": dict, "set": set, "tuple": tuple
        }
        
        self.functions = {}
        self.includes = set()

    def sync_git(self):
        try: subprocess.run(["git", "pull"], capture_output=True)
        except: pass

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
            # Теперь ctx содержит РЕАЛЬНЫЕ объекты val, sys и т.д.
            ctx = {**self.base_ctx, **scope}
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as e:
            return f"<EvalError: {e}>"

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                
                if cmd[0] == "out":
                    res = self.safe_eval(cmd[1:], scope)
                    print(f"\033[38;5;208m[LAVA]\033[0m {str(res)}")
                
                elif cmd[0] == "let":
                    if "=" in cmd:
                        var_name = cmd[1]
                        expr = cmd[cmd.index("=")+1:]
                        scope[var_name] = self.safe_eval(expr, scope)
                
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)

            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    name = h[1]
                    s, e = h.index("(")+1, h.index(")")
                    args = [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()]
                    self.functions[name] = {"args": args, "body": node["body"]}
                elif h[0] == "while":
                    l = 0
                    while bool(self.safe_eval(h[1:], scope)) and l < 2000:
                        self.run(node["body"], scope)
                        l += 1
                elif h[0] == "if":
                    if bool(self.safe_eval(h[1:], scope)):
                        self.run(node["body"], scope)

    def start(self, path):
        self.sync_git()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), {})

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
