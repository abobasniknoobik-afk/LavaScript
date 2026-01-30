import sys, os, re, math, time, subprocess, json

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "9.2.0-MAGMA-LINK",
            "size": len, "str": str, "int": int, "now": lambda: time.ctime(),
            "platform": sys.platform
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
        # Очистка и замена булевых значений
        expr = " ".join(expr_list).replace("true", "True").replace("false", "False")
        try:
            # Используем глобальные + текущие переменные
            return eval(expr, {"__builtins__": None}, {**self.globals, **scope})
        except:
            return None

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                
                if cmd[0] == "out":
                    print(f"\033[92m[LAVA]\033[0m {self.safe_eval(cmd[1:], scope)}")
                
                elif cmd[0] == "let":
                    if "=" in cmd:
                        idx = cmd.index("=")
                        # Прямая запись в ТЕКУЩИЙ scope (никаких копий!)
                        scope[cmd[1]] = self.safe_eval(cmd[idx+1:], scope)
                
                elif cmd[0] == "call":
                    fname = cmd[1]
                    if fname in self.functions:
                        f = self.functions[fname]
                        try:
                            s, e = cmd.index("(")+1, cmd.index(")")
                            raw = " ".join(cmd[s:e])
                            vals = [self.safe_eval([v.strip()], scope) for v in raw.split(",") if v.strip()]
                            # Функции получают копию scope + свои аргументы
                            f_scope = {**scope, **dict(zip(f["args"], vals))}
                            self.run(f["body"], f_scope)
                        except: pass
                
                elif cmd[0] == "sh": os.system(" ".join(cmd[1:]).strip('"'))
                
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if path not in self.includes and os.path.exists(path):
                        self.includes.add(path)
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)

            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    name, s, e = h[1], h.index("(")+1, h.index(")")
                    args = [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()]
                    self.functions[name] = {"args": args, "body": node["body"]}
                elif h[0] == "if":
                    if self.safe_eval(h[1:], scope):
                        self.run(node["body"], scope) # Передаем тот же scope
                elif h[0] == "while":
                    l = 0
                    # ВАЖНО: проверяем условие в том же scope
                    while self.safe_eval(h[1:], scope) and l < 1000:
                        self.run(node["body"], scope)
                        l += 1

    def start(self, path):
        self.sync_git()
        with open(path, 'r', encoding='utf-8') as f:
            tree = self.parse_structure(self.tokenize(f.read()))
            # Главная память программы
            main_scope = {}
            self.run(tree, main_scope)

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
