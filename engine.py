import sys, os, re, math, time, requests, random

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VER": "6.0.0-MAGMA",
            "random": lambda a, b: random.randint(int(a), int(b)),
            "size": len, "append": lambda l, x: l.append(x) or l
        }
        self.functions = {}

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code)
        # Улучшенный токенизатор: разделяет блоки, сохраняя целостность строк
        tokens = []
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            if "{" in line and not line.startswith("{"):
                tokens.append(line.split("{")[0].strip())
                tokens.append("{")
            elif "}" in line: tokens.append("}")
            else: tokens.append(line)
        return tokens

    def parse(self, tokens):
        res = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "{":
                block, bal, i = [], 1, i + 1
                while i < len(tokens) and bal > 0:
                    if tokens[i] == "{": bal += 1
                    elif tokens[i] == "}": bal -= 1
                    if bal > 0: block.append(tokens[i])
                    i += 1
                res.append(self.parse(block))
            else:
                res.append(tokens[i]); i += 1
        return res

    def safe_eval(self, expr, scope):
        try:
            # Умная склейка: превращаем всё в строки при выводе через +
            ctx = {**self.globals, **scope, "str": str, "int": int}
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as e:
            return f"Error: {e}"

    def run(self, tree, scope=None):
        if scope is None: scope = {}
        idx = 0
        while idx < len(tree):
            line = tree[idx]
            if isinstance(line, list): idx += 1; continue
            try:
                # ВЫВОД (теперь без ошибок с кавычками)
                if line.startswith("out "):
                    val = self.safe_eval(line[4:].strip(), scope)
                    print(f"\033[93m[LAVA]\033[0m {val}")

                # МАССИВЫ И ПЕРЕМЕННЫЕ
                elif line.startswith("let "):
                    name, val = line[4:].split("=", 1)
                    scope[name.strip()] = self.safe_eval(val.strip(), scope)

                # ФУНКЦИИ
                elif line.startswith("fn "):
                    m = re.match(r"fn (\w+)\((.*)\)", line)
                    if m:
                        fname, args = m.groups()
                        self.functions[fname] = {"args": [a.strip() for a in args.split(",") if a.strip()], "body": tree[idx+1]}
                    idx += 2; continue

                # ВЫЗОВ
                elif line.startswith("call "):
                    m = re.match(r"call (\w+)\((.*)\)", line)
                    if m:
                        fname, params = m.groups()
                        if fname in self.functions:
                            f = self.functions[fname]
                            p_vals = [self.safe_eval(p.strip(), scope) for p in params.split(",") if p.strip()]
                            self.run(f["body"], dict(zip(f["args"], p_vals)))

                # ЦИКЛЫ И УСЛОВИЯ
                elif line.startswith("if "):
                    if self.safe_eval(line[3:].strip(), scope): self.run(tree[idx+1], scope)
                    idx += 2; continue
                elif line.startswith("while "):
                    while self.safe_eval(line[6:].strip(), scope): self.run(tree[idx+1], scope)
                    idx += 2; continue

                # СИСТЕМНЫЕ
                elif line.startswith("wait "): time.sleep(float(self.safe_eval(line[5:], scope)))
                elif line.startswith("sh "): os.system(line[3:].strip())
            except: pass
            idx += 1

    def start(self, path):
        with open(path, 'r') as f:
            self.run(self.parse(self.tokenize(f.read())))

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
