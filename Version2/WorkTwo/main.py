class CodeInterpreter:
    def __init__(self):
        self.code = []
        self.data_stack = []
        self.registers = [{}]
        self.position = 1

    def load_code(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        self.code = [line.strip().split() for line in lines]

    def execute(self):
        while True:
            instruction = self.code[int(self.position)]

            operation = instruction[0]
            method_name = f'op_{operation.lower()}'
            method = getattr(self, method_name, self.op_invalid)

            if method(instruction):
                break

            self.position += 1

    def op_alme(self, instruction):
        _, var_name = instruction
        self.registers[-1][var_name] = 0
        return False

    def op_armz(self, instruction):
        _, var_name = instruction
        value = self.data_stack.pop()
        self.registers[-1][var_name] = value
        return False

    def op_dsvi(self, instruction):
        _, target_position = instruction
        self.position = int(target_position)-1
        return False

    def op_dsvf(self, instruction):
        _, target_position = instruction
        value = self.data_stack.pop()
        if not value:
            self.position = int(target_position)-1
        return False

    def op_crct(self, instruction):
        _, number = instruction
        self.data_stack.append(float(number))
        return False

    def op_crvl(self, instruction):
        _, var_name = instruction
        value = self.registers[-1][var_name]
        self.data_stack.append(value)
        return False

    def op_soma(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 + val1)
        return False

    def op_subt(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 - val1)
        return False

    def op_mult(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 * val1)
        return False

    def op_divi(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 / val1)
        return False

    def op_inve(self, instruction):
        value = self.data_stack.pop()
        self.data_stack.append(-value)
        return False

    def op_cpme(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 < val1)
        return False

    def op_cpma(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 > val1)
        return False

    def op_cpig(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 == val1)
        return False

    def op_cdes(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 != val1)
        return False

    def op_cpmi(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 <= val1)
        return False

    def op_cmai(self, instruction):
        val1 = self.data_stack.pop()
        val2 = self.data_stack.pop()
        self.data_stack.append(val2 >= val1)
        return False

    def op_leit(self, instruction):
        value = float(input())
        self.data_stack.append(value)
        return False

    def op_impr(self, instruction):
        value = self.data_stack.pop()
        print(value)
        return False

    def op_para(self, instruction):
        return True

    def op_invalid(self, instruction):
        print(f'{instruction[0]} is not a valid operation!')
        return True

if __name__ == '__main__':
    interpreter = CodeInterpreter()
    interpreter.load_code('WorkOne/code.txt')
    interpreter.execute()
