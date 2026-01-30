import sys, os, re, math, time, subprocess, json

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "9.0.0-CORE",
            "size": len, "str": str, "int": int, "now": lambda: time.ctime(),
            "platform": sys.platform, "type": lambda x: type(x).__name__
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
        # Очистка выражения для корректного Python-синтаксиса
        expr = expr.replace("true", "True").replace("false", "False")
        try:
            return eval(expr, {"__builtins__": None}, {**self.globals, **scope})
        except Exception as e:
            return None

    def register_all(self, tree, scope):
        for node in tree:
            if node["type"] == "block" and node["header"][0] == "fn":
                h = node["header"]
                name = h[1]
                s, e = h.index("(")+1, h.index(")")
                args = [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()]
                self.functions[name] = {"args": args, "body": node["body"]}
            elif node["type"] == "statement" and node["content"][0] == "include":
                path = node["content"][1].strip('"')
                if path not in self.includes and os.path.exists(path):
                    self.includes.add(path)
                    with open(path, 'r', encoding='utf-8') as f:
                        self.register_all(self.parse_structure(self.tokenize(f.read())), scope)

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                if cmd[0] == "out":
                    val = self.safe_eval(cmd[1:], scope)
                    print(f"\033[92m[LAVA]\033[0m {val}")
                elif cmd[0] == "let":
                    if "=" in cmd:
                        idx = cmd.index("=")
                        var_name = cmd[1]
                        scope[var_name] = self.safe_eval(cmd[idx+1:], scope)
                elif cmd[0] == "call":
                    fname = cmd[1]
                    if fname in self.functions:
                        f = self.functions[fname]
                        try:
                            s, e = cmd.index("(")+1, cmd.index(")")
                            raw = " ".join(cmd[s:e])
                            vals = [self.safe_eval([v.strip()], scope) for v in raw.split(",") if v.strip()]
                            # Запуск функции с обновленным scope
                            self.run(f["body"], {**scope, **dict(zip(f["args"], vals))})
                        except: pass
            
            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "if":
                    condition = self.safe_eval(h[1:], scope)
                    if condition: self.run(node["body"], scope)
                elif h[0] == "while":
                    # Жесткая проверка условия
                    limit = 0
                    while self.safe_eval(h[1:], scope) and limit < 2000:
                        self.run(node["body"], scope)
                        limit += 1
                    if limit >= 2000:
                        print("\033[91m[CRITICAL]\033[0m Infinite loop detected and stopped.")

    def start(self, path):
        self.sync_git()
        if not os.path.exists(path): return
        with open(path, 'r', encoding='utf-8') as f:
            tree = self.parse_structure(self.tokenize(f.read()))
            scope = {}
            self.register_all(tree, scope)
            self.run(tree, scope)

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
