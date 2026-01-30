import sys, os, re, math, time, requests, random, json

class LavaScript:
    def __init__(self):
        # Встроенные методы в стиле JS/Python
        self.globals = {
            "PI": math.pi, "E": math.e,
            "VER": "8.0.0-PRO",
            "type": lambda x: type(x).__name__,
            "abs": abs, "round": round, "max": max, "min": min,
            "keys": lambda d: list(d.keys()),
            "values": lambda d: list(d.values()),
            "parse_json": json.loads,
            "to_json": json.dumps,
            "random": lambda a, b: random.randint(int(a), int(b)),
            "now": lambda: time.time(),
            "exit": sys.exit
        }
        self.functions = {}
        self.includes = set()

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code)
        tokens = []
        # Регулярка для захвата блоков, строк и символов
        pattern = r'(\{|\}|\[|\]|\(|\)|,|<<|>>|==|!=|>=|<=|[=+\-*/]|[\w\.]+|"[^"]*")'
        for line in code.split('\n'):
            line = line.strip()
            if not line: continue
            line_tokens = re.findall(pattern, line)
            if line_tokens:
                # Группируем токены в линии для парсера
                tokens.append(line_tokens)
        return tokens

    def parse_blocks(self, tokens):
        result = []
        i = 0
        while i < len(tokens):
            line = tokens[i]
            if "{" in line:
                block = []
                balance = 1
                i += 1
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
        # Собираем список токенов обратно в строку для Python-вычисления
        expr = " ".join(expr_list)
        try:
            ctx = {**self.globals, **scope}
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as e:
            return f"EvalError: {e}"

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                
                # INCLUDE (Импорт файлов)
                if cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if path not in self.includes and os.path.exists(path):
                        self.includes.add(path)
                        with open(path, 'r') as f:
                            self.run(self.parse_blocks(self.tokenize(f.read())), scope)

                # OUT (Печать)
                elif cmd[0] == "out":
                    print(f"\033[92m[Lava]\033[0m {self.safe_eval(cmd[1:], scope)}")

                # LET (Переменные)
                elif cmd[0] == "let":
                    eq_idx = cmd.index("=")
                    name = cmd[1]
                    scope[name] = self.safe_eval(cmd[eq_idx+1:], scope)

                # CALL (Вызов функции)
                elif cmd[0] == "call":
                    fname = cmd[1]
                    if fname in self.functions:
                        f = self.functions[fname]
                        # Упрощенный разбор аргументов в скобках
                        args_str = "".join(cmd[cmd.index("(")+1 : cmd.index(")")])
                        arg_vals = [self.safe_eval([a.strip()], scope) for a in args_str.split(",") if a.strip()]
                        f_scope = dict(zip(f["args"], arg_vals))
                        self.run(f["body"], f_scope)

                # SYSTEM
                elif cmd[0] == "sh": os.system(" ".join(cmd[1:]).strip('"'))
                elif cmd[0] == "wait": time.sleep(float(self.safe_eval(cmd[1:], scope)))

            elif node["type"] == "block":
                header = node["header"]
                # FUNCTION DEFINITION
                if header[0] == "fn":
                    fname = header[1]
                    args_str = "".join(header[header.index("(")+1 : header.index(")")])
                    self.functions[fname] = {
                        "args": [a.strip() for a in args_str.split(",") if a.strip()],
                        "body": node["body"]
                    }
                # IF
                elif header[0] == "if":
                    cond = header[1:]
                    if self.safe_eval(cond, scope):
                        self.run(node["body"], scope)
                # WHILE
                elif header[0] == "while":
                    cond = header[1:]
                    while self.safe_eval(cond, scope):
                        self.run(node["body"], scope)

    def execute(self, path):
        if not os.path.exists(path): return
        with open(path, 'r') as f:
            tokens = self.tokenize(f.read())
            tree = self.parse_blocks(tokens)
            self.run(tree)

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().execute(sys.argv[1])
