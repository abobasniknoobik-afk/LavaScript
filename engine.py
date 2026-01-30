import sys, os, re, math, time, requests, random

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VERSION": "5.0.0-ULTRA",
            "AUTHOR": "LS-Team", "platform": sys.platform
        }
        self.functions = {}

    def evaluate(self, expr, scope):
        try:
            # Математика и логика
            ctx = {**self.globals, **scope, "random": random.randint, "sin": math.sin}
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as e:
            return f"<EvalError: {e}>"

    def tokenize(self, code):
        code = re.sub(r'#.*', '', code) # Удаляем комментарии
        tokens = []
        # Умная разбивка с учетом блоков { }
        for line in code.split('\n'):
            line = line.strip()
            if not line: continue
            if "{" in line:
                tokens.append(line.split("{")[0].strip())
                tokens.append("{")
            elif "}" in line:
                tokens.append("}")
            else:
                tokens.append(line)
        return tokens

    def parse_blocks(self, tokens):
        output = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "{":
                block, balance, i = [], 1, i + 1
                while i < len(tokens) and balance > 0:
                    if tokens[i] == "{": balance += 1
                    if tokens[i] == "}": balance -= 1
                    if balance > 0: block.append(tokens[i])
                    i += 1
                output.append(self.parse_blocks(block))
            else:
                output.append(tokens[i])
                i += 1
        return output

    def run(self, block, scope=None):
        if scope is None: scope = {}
        ptr = 0
        while ptr < len(block):
            line = block[ptr]
            if isinstance(line, list): 
                ptr += 1
                continue
            
            try:
                # ВЫВОД
                if line.startswith("out "):
                    print(f"\033[96m[LS]\033[0m {self.evaluate(line[4:].strip(), scope)}")

                # ПЕРЕМЕННЫЕ
                elif line.startswith("let "):
                    name, val = line[4:].split("=", 1)
                    scope[name.strip()] = self.evaluate(val.strip(), scope)

                # ФУНКЦИИ
                elif line.startswith("fn "):
                    match = re.match(r"fn (\w+)\((.*)\)", line)
                    if match:
                        name, args = match.groups()
                        self.functions[name] = {"args": [a.strip() for a in args.split(",")], "body": block[ptr+1]}
                    ptr += 2; continue

                # ВЫЗОВ ФУНКЦИИ
                elif line.startswith("call "):
                    match = re.match(r"call (\w+)\((.*)\)", line)
                    if match:
                        fname, val_expr = match.groups()
                        if fname in self.functions:
                            f = self.functions[fname]
                            args_vals = [self.evaluate(v.strip(), scope) for v in val_expr.split(",")]
                            f_scope = dict(zip(f["args"], args_vals))
                            self.run(f["body"], f_scope)

                # УСЛОВИЯ И ЦИКЛЫ
                elif line.startswith("if "):
                    if self.evaluate(line[3:].strip(), scope): self.run(block[ptr+1], scope)
                    ptr += 2; continue
                elif line.startswith("while "):
                    while self.evaluate(line[6:].strip(), scope): self.run(block[ptr+1], scope)
                    ptr += 2; continue

                # СИСТЕМНЫЕ ФУНКЦИИ (РАБОТА С ФАЙЛАМИ И ТЕРМИНАЛОМ)
                elif line.startswith("write "): # write "file.txt" << "content"
                    path, data = line[6:].split("<<")
                    with open(self.evaluate(path, scope), "w") as f: f.write(str(self.evaluate(data, scope)))
                elif line.startswith("sh "):
                    os.system(line[3:].strip())
                elif line.startswith("wait "):
                    time.sleep(float(self.evaluate(line[5:], scope)))
                elif line.startswith("fetch "): # fetch url >> var
                    url, var = line[6:].split(">>")
                    res = requests.get(self.evaluate(url, scope))
                    scope[var.strip()] = res.text[:100] # Берем первые 100 символов

                # ВВОД
                elif line.startswith("ask "):
                    var, q = line[4:].split("<<")
                    scope[var.strip()] = input(self.evaluate(q, scope))

            except Exception as e:
                print(f"\033[91m[Error @ line {ptr}]: {e}\033[0m")
            ptr += 1

    def start(self, file):
        with open(file, 'r') as f:
            tokens = self.tokenize(f.read())
        self.run(self.parse_blocks(tokens))

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
    else: print("LavaScript Ultra 5.0 - No file provided.")
