import sys, os, re, math, time, requests, random, json

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "8.3.0-PRO",
            "random": lambda a, b: random.randint(int(a), int(b)),
            "size": len, "str": str, "int": int, "now": lambda: time.ctime(),
            "platform": sys.platform,
            "keys": lambda d: list(d.keys()) if isinstance(d, dict) else [],
            "clear": lambda: os.system('clear')
        }
        self.functions = {}
        self.includes = set()

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code)
        tokens = []
        # Паттерн, который понимает даже сложные вложенные структуры
        pattern = r'(\{|\}|\[|\]|\(|\)|,|<<|>>|==|!=|>=|<=|[=+\-*/:]|[\w\.]+|"[^"]*")'
        for line in code.split('\n'):
            line = line.strip()
            if not line: continue
            line_tokens = re.findall(pattern, line)
            if line_tokens: tokens.append(line_tokens)
        return tokens

    def parse_blocks(self, tokens):
        result = []
        i = 0
        while i < len(tokens):
            line = tokens[i]
            if "{" in line:
                block, balance, i = [], 1, i + 1
                while i < len(tokens) and balance > 0:
                    if "{" in tokens[i]: balance += 1
                    if "}" in tokens[i]: balance -= 1
                    if balance > 0: block.append(tokens[i])
                    i += 1
                result.append({"type": "block", "header": line, "body": self.parse_blocks(block)})
            else:
                result.append({"type": "statement", "content": line})
                i += 1
        return result

    def safe_eval(self, expr_list, scope):
        expr = " ".join(expr_list)
        # Убираем двоеточия из простых выражений, если они там затесались
        expr = expr.replace(" : ", ":")
        try:
            return eval(expr, {"__builtins__": None}, {**self.globals, **scope})
        except Exception as e:
            return f"<Error: {e}>"

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                
                if cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if path not in self.includes and os.path.exists(path):
                        self.includes.add(path)
                        with open(path, 'r') as f:
                            self.run(self.parse_blocks(self.tokenize(f.read())), scope)
                
                elif cmd[0] == "out":
                    print(f"\033[94m[Lava]\033[0m {self.safe_eval(cmd[1:], scope)}")
                
                elif cmd[0] == "let":
                    if "=" in cmd:
                        idx = cmd.index("=")
                        scope[cmd[1]] = self.safe_eval(cmd[idx+1:], scope)
                
                elif cmd[0] == "call":
                    fname = cmd[1]
                    if fname in self.functions:
                        f = self.functions[fname]
                        # Умный разбор параметров
                        try:
                            start, end = cmd.index("(") + 1, cmd.index(")")
                            raw_args = " ".join(cmd[start:end])
                            vals = [self.safe_eval([a.strip()], scope) for a in raw_args.split(",") if a.strip()]
                            self.run(f["body"], {**scope, **dict(zip(f["args"], vals))})
                        except: self.run(f["body"], scope)

            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    name = h[1]
                    # Извлекаем аргументы функции
                    try:
                        args = [a.strip() for a in " ".join(h[h.index("(")+1:h.index(")")]).split(",") if a.strip()]
                        self.functions[name] = {"args": args, "body": node["body"]}
                    except: pass
                elif h[0] == "if":
                    if self.safe_eval(h[1:], scope): self.run(node["body"], scope)
                elif h[0] == "while":
                    while self.safe_eval(h[1:], scope): self.run(node["body"], scope)

    def start(self, path):
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            self.run(self.parse_blocks(self.tokenize(f.read())))

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
