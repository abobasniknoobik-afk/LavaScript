import os
import random
import time
import sys

class LavaScript:
    def __init__(self):
        self.variables = {
            'True': True, 'False': False,
            'lava_ver': '2.1.0',
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
                # TYPE: Вывод
                if line.startswith("type "):
                    print(eval(line[5:].strip(), {}, self.variables))

                # ASK: Ввод
                elif line.startswith("ask "):
                    name, q = line[4:].split("<<", 1)
                    self.variables[name.strip()] = input(eval(q.strip(), {}, self.variables))

                # FLOW (IF): Исправленный разбор
                elif line.startswith("flow "):
                    # Режем только по ПЕРВОМУ двоеточию
                    content = line[5:].strip()
                    cond, action = content.split(":", 1)
                    if eval(cond.strip(), {}, self.variables):
                        self.execute_one(action.strip())

                # LOOP (FOR): Исправленный разбор
                elif line.startswith("loop "):
                    content = line[5:].strip()
                    times, action = content.split(":", 1)
                    for _ in range(int(eval(times.strip(), {}, self.variables))):
                        self.execute_one(action.strip())

                # MOLTEN: Переменные
                elif "molten" in line and "<<" in line:
                    name, expr = line.replace("molten", "").split("<<", 1)
                    self.variables[name.strip()] = eval(expr.strip(), {}, self.variables)

                # WAIT и COOL
                elif line.startswith("wait "):
                    time.sleep(float(eval(line[5:], {}, self.variables)))
                elif line.startswith("cool "):
                    self.variables.pop(line[5:].strip(), None)

            except Exception as e:
                print(f"🌋 Ошибка в строке {ptr+1} ({line[:15]}...): {e}")
            ptr += 1

    def execute_one(self, action):
        # Внутренний обработчик для flow/loop
        if action.startswith("type "):
            print(eval(action[5:].strip(), {}, self.variables))
        elif "<<" in action:
            parts = action.split("<<", 1)
            self.variables[parts[0].strip()] = eval(parts[1].strip(), {}, self.variables)

if __name__ == "__main__":
    LavaScript().run()
