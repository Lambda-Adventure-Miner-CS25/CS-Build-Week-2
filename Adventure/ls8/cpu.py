import sys

LDI     = 0b10000010
PRA     = 0b01001000
HLT     = 0b00000001
AND     = 0b10101000
XOR     = 0b10101011
OR      = 0b10101010
NOT     = 0b01101001
MUL     = 0b10100010
PUSH    = 0b01000101
POP     = 0b01000110
CALL    = 0b01010000 
RET     = 0b00010001
ADD     = 0b10100000
PRA     = 0b01001000


class CPU:
    def __init__(self):
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.clue = ''

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, filename):
        print(filename)
        try:
            address = 0
            # Open the file
            with open(filename) as f:
                # Read all the lines
                for line in f:
                    comment_split = line.strip().split()
                    del comment_split[0:8]
                    comment_split[-1] = '00000001'
                for i in range(0, len(comment_split)):
                    value = comment_split[i]

                    num = int(value, 2)
                    print(num)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    if len(sys.argv) != 2:
        print("ERROR: Must have file name")
        sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while True:
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI:
                # print('LDI')
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == MUL:
                # print('MUL')
                product = self.reg[operand_a] * self.reg[operand_b]
                print(product)
                self.pc += 3
            elif opcode == PUSH:
                # print('PUSH')
                val = self.reg[operand_a]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                self.pc += 2
            elif opcode == POP:
                # print('POP')
                val = self.ram[self.reg[SP]]
                self.reg[operand_a] = val
                self.reg[SP] += 1
                self.pc += 2
            elif opcode == CALL:
                # print('CALL')
                val = self.pc + 2
                reg = self.ram[self.pc + 1]
                sub = self.reg[reg]
                self.reg[SP]-=1  
                self.ram[self.reg[SP]]=val
                self.pc=sub  
            elif opcode == RET:
                # print('RET')
                ret=self.reg[SP]
                self.pc=self.ram[ret]
                self.reg[SP]+=1
            elif opcode == ADD:
                # print('ADD')
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3
            elif opcode == PRA:
                # print('PRA')
                self.clue += chr(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            elif opcode == AND:
                # print('AND')
                self.reg[operand_a] &= self.reg[operand_b]
                self.pc += 3
            elif opcode == XOR:
                # print('XOR')
                self.reg[operand_a] ^= self.reg[operand_b]
                self.pc += 3
            elif opcode == OR:
                # print('OR')
                self.reg[operand_a] |= self.reg[operand_b]
                self.pc += 3
            elif opcode == NOT:
                # print('NOT')
                self.reg[operand_a] = ~(self.reg[operand_a])
                self.pc += 2
            elif opcode == HLT:
                # print('HLT')
                print(self.clue)
                sys.exit(0)
            else:
                print(f'I did not understand that command: {opcode}')
                sys.exit(1)


