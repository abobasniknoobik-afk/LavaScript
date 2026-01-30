import sys, os, re, math, time, requests, random

class LavaScript:
    def __init__(self):
        # Глобальное пространство имен
        self.globals = {
            "PI": math.pi, "VERSION": "5.1.0-FIX",
            "platform": sys.platform, "str": str, "int": int,
            "random": lambda a, b: random.randint(int(a), int(b))
        }
        self.functions = {}

    def tokenize(self, code):
        # Очистка от комментариев и пустых строк
        code = re.sub(r'#.*', '', code)
        tokens = []
        for line in code.split('\n'):
            l = line.strip()
            if not l: continue
            # Умное разделение блоков { }
            if "{" in l:
                parts = l.split("{")
                if parts[0].strip(): tokens.append(parts[0].strip())
                tokens.append("{")
            elif "}" in l:
                tokens.append("}")
            else:
                tokens.append(l)
        return tokens

    def parse_to_blocks(self, tokens):
        res = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "{":
                block, balance, i = [], 1, i + 1
                while i < len(tokens) and balance > 0:
                    if tokens[i] == "{": balance += 1
                    elif tokens[i] == "}": balance -= 1
                    if balance > 0: block.append(tokens[i])
                    i += 1
                res.append(self.parse_to_blocks(block))
            else:
                res.append(tokens[i])
                i += 1
        return res

    def eval_expr(self, expr, scope):
        try:
            # Объединяем глобалки, локалки и встроенные функции
            context = {**self.globals, **scope}
            return eval(expr, {"__builtins__": None}, context)
        except Exception as e:
            return f"EvalError: {e}"

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        idx = 0
        while idx < len(tree):
            line = tree[idx]
            if isinstance(line, list):
                idx += 1; continue
            
            try:
                # ВЫВОД (OUT)
                if line.startswith("out "):
                    print(f"\033[95m[Lava]\033[0m {self.eval_expr(line[4:].strip(), scope)}")

                # ПЕРЕМЕННЫЕ (LET)
                elif line.startswith("let "):
                    name, val = line[4:].split("=", 1)
                    scope[name.strip()] = self.eval_expr(val.strip(), scope)

                # ОПРЕДЕЛЕНИЕ ФУНКЦИИ (FN)
                elif line.startswith("fn "):
                    m = re.match(r"fn (\w+)\((.*)\)", line)
                    if m:
                        fname, args = m.groups()
                        self.functions[fname] = {
                            "args": [a.strip() for a in args.split(",") if a.strip()],
                            "body": tree[idx+1]
                        }
                    idx += 2; continue

                # ВЫЗОВ ФУНКЦИИ (CALL)
                elif line.startswith("call "):
                    m = re.match(r"call (\w+)\((.*)\)", line)
                    if m:
                        fname, params = m.groups()
                        if fname in self.functions:
                            f = self.functions[fname]
                            # Вычисляем параметры в текущем scope
                            p_vals = [self.eval_expr(p.strip(), scope) for p in params.split(",") if p.strip()]
                            # Создаем локальный scope для функции
                            f_scope = dict(zip(f["args"], p_vals))
                            self.run(f["body"], f_scope)

                # УСЛОВИЕ (IF)
                elif line.startswith("if "):
                    cond = line[3:].strip()
                    if self.eval_expr(cond, scope):
                        self.run(tree[idx+1], scope)
                    idx += 2; continue

                # ЦИКЛ (WHILE)
                elif line.startswith("while "):
                    cond = line[6:].strip()
                    body = tree[idx+1]
                    while self.eval_expr(cond, scope):
                        self.run(body, scope)
                    idx += 2; continue

                # СИСТЕМНЫЕ
                elif line.startswith("ask "):
                    v, q = line[4:].split("<<")
                    scope[v.strip()] = input(self.eval_expr(q, scope))
                elif line.startswith("sh "):
                    os.system(line[3:].strip())
                elif line.startswith("wait "):
                    time.sleep(float(self.eval_expr(line[5:], scope)))

            except Exception as e:
                print(f"🌋 Runtime Error at '{line}': {e}")
            idx += 1

    def execute(self, file_path):
        with open(file_path, 'r') as f:
            tokens = self.tokenize(f.read())
            tree = self.parse_to_blocks(tokens)
            self.run(tree)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        LavaScript().execute(sys.argv[1])
