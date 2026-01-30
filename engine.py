import sys, os, re, math

class LavaScript:
    def __init__(self):
        self.globals = {
            "PI": math.pi, "VERSION": "4.0.0",
            "platform": sys.platform, "print": print,
            "len": len, "range": range, "str": str, "int": int
        }
        self.functions = {}

    def parse_blocks(self, tokens):
        """ Собирает токены в структуру с учетом вложенности { } """
        output = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "{":
                block = []
                balance = 1
                i += 1
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

    def evaluate(self, expr, scope):
        """ Безопасное вычисление выражений в контексте """
        try:
            return eval(expr, {"__builtins__": None, "math": math}, {**self.globals, **scope})
        except Exception as e:
            return f"<Error: {e}>"

    def run_block(self, block, scope=None):
        if scope is None: scope = {}
        ptr = 0
        while ptr < len(block):
            line = block[ptr]
            if isinstance(line, list): 
                ptr += 1
                continue

            # ОБЪЯВЛЕНИЕ ФУНКЦИЙ: fn name(arg) { code }
            if line.startswith("fn "):
                match = re.match(r"fn (\w+)\((.*)\)", line)
                if match:
                    name, args = match.groups()
                    self.functions[name] = {"args": [a.strip() for a in args.split(",")], "body": block[ptr+1]}
                ptr += 2

            # ЦИКЛ WHILE: while cond { code }
            elif line.startswith("while "):
                cond = line[6:].strip()
                body = block[ptr+1]
                while self.evaluate(cond, scope):
                    self.run_block(body, scope)
                ptr += 2

            # УСЛОВИЕ IF: if cond { code }
            elif line.startswith("if "):
                cond = line[3:].strip()
                body = block[ptr+1]
                if self.evaluate(cond, scope):
                    self.run_block(body, scope)
                ptr += 2

            # ВЫВОД: out expr
            elif line.startswith("out "):
                print(self.evaluate(line[4:].strip(), scope))

            # ПЕРЕМЕННЫЕ: let x = expr
            elif line.startswith("let "):
                name, val = line[4:].split("=", 1)
                scope[name.strip()] = self.evaluate(val.strip(), scope)

            # ВЫЗОВ ФУНКЦИИ: call name(val)
            elif line.startswith("call "):
                match = re.match(r"call (\w+)\((.*)\)", line)
                if match:
                    fname, val_expr = match.groups()
                    if fname in self.functions:
                        f = self.functions[fname]
                        val = self.evaluate(val_expr, scope)
                        f_scope = {f["args"][0]: val} if f["args"] else {}
                        self.run_block(f["body"], f_scope)
                ptr += 1
            else: ptr += 1

    def start(self, file):
        with open(file, 'r') as f:
            raw_code = f.read()
        # Чистим код и разбиваем на значимые куски (токены)
        raw_code = re.sub(r'#.*', '', raw_code)
        tokens = []
        for line in raw_code.split('\n'):
            line = line.strip()
            if not line: continue
            if "{" in line and not line.endswith("{"):
                parts = line.split("{")
                tokens.append(parts[0].strip())
                tokens.append("{")
            elif "}" in line:
                tokens.append("}")
            else:
                tokens.append(line)
        
        structured_code = self.parse_blocks(tokens)
        self.run_block(structured_code)

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
