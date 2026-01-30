import sys, os, re, math, time, subprocess, random

class LavaScript:
    def __init__(self):
        # Наш эксклюзивный набор команд под стиль LS
        self.ls_builtins = {
            # VAL - Работа с типами
            "val.str": str, "val.int": int, "val.dec": float, "val.logic": bool,
            "val.kind": lambda x: type(x).__name__, "val.module": abs,
            "val.to_hex": hex, "val.to_bin": bin, "val.code": ord, "val.char": chr,
            
            # MATH - Высшие вычисления
            "math.root": math.sqrt, "math.exp": pow, "math.up": math.ceil,
            "math.down": math.floor, "math.sin": math.sin, "math.cos": math.cos,
            "math.log": math.log, "math.fix": round, "math.total": sum,
            "math.peak": max, "math.base": min,
            
            # SYS - Взаимодействие с окружением
            "sys.size": len, "sys.step": range, "sys.link": enumerate,
            "sys.halt": sys.exit, "sys.pause": time.sleep, "sys.path": os.getcwd,
            "sys.scan": os.listdir, "sys.env": sys.platform, "sys.now": lambda: time.ctime(),
            "sys.id": id, "sys.rev": reversed, "sys.sort": sorted,
            
            # RAND - Генерация случайности
            "rand.num": random.randint, "rand.select": random.choice, "rand.chaos": random.shuffle,
            
            # IO - Ввод/Вывод
            "io.out": print, "io.get": input, "io.file": open, "io.inject": eval,
            "io.inspect": dir, "io.vars": vars,
            
            # Базовые структуры
            "list": list, "dict": dict, "set": set, "tuple": tuple
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
        res, i = [], 0
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
            ctx = {**self.ls_builtins, **scope}
            return eval(expr, {"__builtins__": None}, ctx)
        except Exception as e:
            return None

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                
                if cmd[0] == "out":
                    res = self.safe_eval(cmd[1:], scope)
                    # Фикс: принудительно превращаем в строку, если eval не смог склеить
                    print(f"\033[38;5;208m[LAVA]\033[0m {str(res)}")
                
                elif cmd[0] == "let":
                    if "=" in cmd:
                        var_name = cmd[1]
                        expr = cmd[cmd.index("=")+1:]
                        scope[var_name] = self.safe_eval(expr, scope)
                
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)

            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    name = h[1]
                    s, e = h.index("(")+1, h.index(")")
                    args = [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()]
                    self.functions[name] = {"args": args, "body": node["body"]}
                elif h[0] == "while":
                    l = 0
                    while bool(self.safe_eval(h[1:], scope)) and l < 2000:
                        self.run(node["body"], scope)
                        l += 1
                elif h[0] == "if":
                    if bool(self.safe_eval(h[1:], scope)):
                        self.run(node["body"], scope)

    def start(self, path):
        self.sync_git()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), {})

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
