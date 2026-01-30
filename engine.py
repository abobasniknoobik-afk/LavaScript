import sys, os, re, math, time, subprocess, json

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "8.8.0-ANTI-CHAOS",
            "size": len, "str": str, "int": int, "now": lambda: time.ctime(),
            "platform": sys.platform, "type": lambda x: type(x).__name__
        }
        self.functions = {}
        self.includes = set()
        self.max_iter = 1000  # Защита: не более 1000 итераций в цикле

    def sync_git(self):
        try:
            # Печатаем только если есть реальные обновления, чтобы не спамить
            subprocess.run(["git", "pull"], capture_output=True)
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
        res = []
        i = 0
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
        expr = " ".join(expr_list)
        try:
            # Если вычисление падает, возвращаем None, а не строку "Error"
            return eval(expr, {"__builtins__": None}, {**self.globals, **scope})
        except: return None 

    def register_all(self, tree, scope):
        for node in tree:
            if node["type"] == "block" and node["header"][0] == "fn":
                h = node["header"]
                name = h[1]
                try:
                    s, e = h.index("(")+1, h.index(")")
                    args = [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()]
                    self.functions[name] = {"args": args, "body": node["body"]}
                except: pass
            elif node["type"] == "statement" and node["content"][0] == "include":
                path = node["content"][1].strip('"')
                if path not in self.includes and os.path.exists(path):
                    self.includes.add(path)
                    with open(path, 'r', encoding='utf-8') as f:
                        sub_tree = self.parse_structure(self.tokenize(f.read()))
                        self.register_all(sub_tree, scope)

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if cmd[0] == "out":
                    print(f"\033[92m[LAVA]\033[0m {self.safe_eval(cmd[1:], scope)}")
                elif cmd[0] == "let":
                    if "=" in cmd:
                        idx = cmd.index("=")
                        scope[cmd[1]] = self.safe_eval(cmd[idx+1:], scope)
                elif cmd[0] == "call":
                    fname = cmd[1]
                    if fname in self.functions:
                        f = self.functions[fname]
                        try:
                            s, e = cmd.index("(")+1, cmd.index(")")
                            raw = " ".join(cmd[s:e])
                            vals = [self.safe_eval([v.strip()], scope) for v in raw.split(",") if v.strip()]
                            self.run(f["body"], {**scope, **dict(zip(f["args"], vals))})
                        except: self.run(f["body"], scope)
            elif node["type"] == "block" and node["header"][0] != "fn":
                h = node["header"]
                if h[0] == "if":
                    if self.safe_eval(h[1:], scope): self.run(node["body"], scope)
                elif h[0] == "while":
                    iters = 0
                    while self.safe_eval(h[1:], scope) and iters < self.max_iter:
                        self.run(node["body"], scope)
                        iters += 1
                    if iters >= self.max_iter:
                        print("\033[91m[LS-FATAL]\033[0m Превышен лимит итераций (Anti-Chaos).")

    def start(self, path):
        self.sync_git()
        if not os.path.exists(path): return
        with open(path, 'r', encoding='utf-8') as f:
            tree = self.parse_structure(self.tokenize(f.read()))
            scope = {}
            self.register_all(tree, scope)
            self.run(tree, scope)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        LavaScript().start(sys.argv[1])
