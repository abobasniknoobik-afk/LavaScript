import sys, os, re, math, time, random, json

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "8.6.0-HYPERION",
            "random": lambda a, b: random.randint(int(a), int(b)),
            "size": len, "str": str, "int": int, "now": lambda: time.ctime(),
            "platform": sys.platform, "type": lambda x: type(x).__name__
        }
        self.functions = {}
        self.includes = set()

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code)
        tokens = []
        pattern = r'(\{|\}|\[|\]|\(|\)|,|<<|>>|==|!=|>=|<=|[=+\-*/:]|[\w\.]+|"[^"]*")'
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
            return eval(expr, {"__builtins__": None}, {**self.globals, **scope})
        except Exception as e: return f"<Error: {e}>"

    def register_all(self, tree, scope):
        """Регистрирует все функции во всех файлах рекурсивно"""
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
                    with open(path, 'r') as f:
                        sub_tree = self.parse_structure(self.tokenize(f.read()))
                        self.register_all(sub_tree, scope)

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
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
                            # Запускаем в общем контексте, чтобы функции видели переменные
                            self.run(f["body"], {**scope, **dict(zip(f["args"], vals))})
                        except Exception as e:
                            print(f"Call Error: {e}")
            elif node["type"] == "block" and node["header"][0] != "fn":
                h = node["header"]
                if h[0] == "if":
                    if self.safe_eval(h[1:], scope): self.run(node["body"], scope)
                elif h[0] == "while":
                    while self.safe_eval(h[1:], scope): self.run(node["body"], scope)

    def start(self, path):
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            tree = self.parse_structure(self.tokenize(f.read()))
            scope = {}
            self.register_all(tree, scope) # Сначала регистрируем всё из всех include
            self.run(tree, scope)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        LavaScript().start(sys.argv[1])
