import sys, os, re, math, time, subprocess, random

class LavaScript:
    def __init__(self):
        # Группируем всё по оригинальным категориям LS
        self.ls_builtins = {
            # Модуль VAL (Типы и преобразования)
            "val.abs": abs, "val.bool": bool, "val.int": int, "val.str": str, 
            "val.float": float, "val.type": type, "val.ascii": ascii, "val.bin": bin,
            "val.hex": hex, "val.oct": oct, "val.chr": chr, "val.ord": ord,
            "val.bytes": bytes, "val.bytearray": bytearray, "val.complex": complex,
            
            # Модуль MATH (Математика)
            "math.max": max, "math.min": min, "math.sum": sum, "math.round": round,
            "math.pow": pow, "math.sqrt": math.sqrt, "math.ceil": math.ceil, 
            "math.floor": math.floor, "math.sin": math.sin, "math.cos": math.cos, 
            "math.log": math.log, "math.divmod": divmod,
            
            # Модуль SYS (Система и Итерация)
            "sys.size": len, "sys.platform": sys.platform, "sys.now": lambda: time.ctime(),
            "sys.sleep": time.sleep, "sys.exit": sys.exit, "sys.cwd": os.getcwd,
            "sys.ls": os.listdir, "sys.range": range, "sys.rev": reversed,
            "sys.sort": sorted, "sys.enum": enumerate, "sys.all": all, "sys.any": any,
            "sys.id": id, "sys.hash": hash, "sys.help": help, "sys.call": callable,
            
            # Модуль RAND (Рандом)
            "rand.int": random.randint, "rand.pick": random.choice, "rand.mix": random.shuffle,
            
            # Модуль IO (Ввод/Вывод и Динамика)
            "io.open": open, "io.input": input, "io.eval": eval, "io.exec": exec,
            "io.print": print, "io.dir": dir, "io.vars": vars, "io.globals": globals,
            "io.locals": locals,
            
            # Структуры данных
            "list": list, "dict": dict, "set": set, "tuple": tuple, "frozenset": frozenset
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
        expr = " ".join(expr_list).replace("true", "True").replace("false", "False")
        try:
            # Магия объединения памяти
            ctx = {**self.ls_builtins, **scope}
            return eval(expr, {"__builtins__": None}, ctx)
        except: return None

    def run(self, tree, scope):
        for node in tree:
            if node["type"] == "statement":
                cmd = node["content"]
                if not cmd: continue
                
                if cmd[0] == "out":
                    print(f"\033[38;5;208m[LAVA]\033[0m {self.safe_eval(cmd[1:], scope)}")
                
                elif cmd[0] == "let":
                    if "=" in cmd:
                        scope[cmd[1]] = self.safe_eval(cmd[cmd.index("=")+1:], scope)
                
                elif cmd[0] == "include":
                    path = cmd[1].strip('"')
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            self.run(self.parse_structure(self.tokenize(f.read())), scope)

            elif node["type"] == "block":
                h = node["header"]
                if h[0] == "fn":
                    name, s, e = h[1], h.index("(")+1, h.index(")")
                    self.functions[name] = {"args": [a.strip() for a in " ".join(h[s:e]).split(",") if a.strip()], "body": node["body"]}
                elif h[0] == "while":
                    limit = 0
                    while self.safe_eval(h[1:], scope) and limit < 2000:
                        self.run(node["body"], scope)
                        limit += 1

    def start(self, path):
        self.sync_git()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.run(self.parse_structure(self.tokenize(f.read())), {})

if __name__ == "__main__":
    if len(sys.argv) > 1: LavaScript().start(sys.argv[1])
