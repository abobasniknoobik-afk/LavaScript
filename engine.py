import sys, os, re, math, time, subprocess

class LavaScript:
    def __init__(self):
        # Переименовываем стандартные функции в стиль LS
        self.ls_builtins = {
            "val.abs": abs,
            "val.bool": bool,
            "val.int": int,
            "val.str": str,
            "val.float": float,
            "val.type": type,
            "math.max": max,
            "math.min": min,
            "math.sum": sum,
            "math.round": round,
            "sys.size": len,
            "sys.platform": sys.platform,
            "sys.now": lambda: time.ctime(),
            "sys.exec": exec,
            "sys.dir": dir,
            "list.create": list,
            "list.sort": sorted,
            "list.join": zip,
            "io.open": open,
            "io.input": input,
            # Оставляем out как базовый вывод
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
            # Используем наши оригинальные префиксы
            return eval(expr, {"__builtins__": None}, {**self.ls_builtins, **scope})
        except: return None

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                if cmd[0] == "out":
                    print(f"\033[91m[LAVA]\033[0m {self.safe_eval(cmd[1:], scope)}")
                elif cmd[0] == "let":
                    if "=" in cmd:
                        scope[cmd[1]] = self.safe_eval(cmd[cmd.index("=")+1:], scope)
                elif cmd[0] == "call":
                    f = self.functions.get(cmd[1])
                    if f:
                        s, e = cmd.index("(")+1, cmd.index(")")
                        raw = " ".join(cmd[s:e])
                        vals = [self.safe_eval([v.strip()], scope) for v in raw.split(",") if v.strip()]
                        self.run(f["body"], {**scope, **dict(zip(f["args"], vals))})
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)
            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    s, e = h.index("(")+1, h.index(")")
                    self.functions[h[1]] = {"args": [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()], "body": node["body"]}
                elif h[0] == "if":
                    if self.safe_eval(h[1:], scope): self.run(node["body"], scope)
                elif h[0] == "while":
                    l = 0
                    while self.safe_eval(h[1:], scope) and l < 1000:
                        self.run(node["body"], scope)
                        l += 1

    def start(self, path):
        self.sync_git()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), {})

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
