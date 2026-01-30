import os
import random
import time
import sys

class LavaScript:
    def __init__(self):
        # Встроенные функции и переменные
        self.variables = {
            'True': True, 'False': False,
            'lava_ver': '2.0.0',
            'random': lambda r: random.randint(0, int(r)),
            'int': int, 'str': str, 'len': len
        }

    def run(self):
        if not os.path.exists("main.ls"): return
        with open("main.ls", "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
        
        ptr = 0
        while ptr < len(lines):
            line = lines[ptr]
            
            try:
                # ASK: Ввод данных
                if line.startswith("ask "):
                    var_name, q = line[4:].split("<<")
                    self.variables[var_name.strip()] = input(eval(q, {}, self.variables))

                # TYPE: Печать (поддерживает цвета через символы)
                elif line.startswith("type "):
                    print(eval(line[5:].strip(), {}, self.variables))

                # MOLTEN: Переменные и Математика
                elif "molten" in line and "<<" in line:
                    name, expr = line.replace("molten", "").split("<<")
                    self.variables[name.strip()] = eval(expr.strip(), {}, self.variables)

                # FLOW (IF): Условие
                elif line.startswith("flow "):
                    cond, action = line[5:].split(":")
                    if eval(cond, {}, self.variables):
                        self.execute_one(action.strip())

                # LOOP (FOR): Повторение (loop 5 : type "Hi")
                elif line.startswith("loop "):
                    times, action = line[5:].split(":")
                    for _ in range(int(eval(times, {}, self.variables))):
                        self.execute_one(action.strip())

                # COOL: Удаление переменной
                elif line.startswith("cool "):
                    del self.variables[line[5:].strip()]

                # WAIT: Пауза
                elif line.startswith("wait "):
                    time.sleep(float(eval(line[5:], {}, self.variables)))

            except Exception as e:
                print(f"🌋 Ошибка в строке {ptr+1}: {e}")
            ptr += 1

    def execute_one(self, action):
        if action.startswith("type "): print(eval(action[5:], {}, self.variables))
        elif "<<" in action: # Позволяет менять переменные внутри циклов/условий
            n, e = action.split("<<")
            self.variables[n.strip()] = eval(e.strip(), {}, self.variables)

if __name__ == "__main__":
    LavaScript().run()
