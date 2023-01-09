def make_image(input_file, output_file):
    instructions = get_instructions(input_file)
    lines = []
    for i in range(256):
        lines += [format(i * 8, 'x') + ': ']
        for j in range(8):
            lines[i] += instructions[(i * 16) + j]
            if j != 7:
                lines[i] += ' '
            else:
                lines[i] += '\n'
    lines = ['v3.0 hex words addressed\n'] + lines 
    lines[1] = '0' + lines[1]
    open(output_file, 'w').writelines(lines)
            
def get_instructions(input_file):
    instructions = ['00000000'] * 256 * 8
    labels = {}
    with open(input_file, 'r') as input:
        i = 0
        # find all labels first
        # perhaps do a first loop where each line is changed to its split version. If the length is one add it to labels
        # can also do every instruction that isn't a branching command
        # Then a second loop that takes care of all the branching commands that need their offsets to be calculated
        for line in input:
            line = line.split(' ')
            line[-1] = line[-1].strip()
            
            if len(line) == 1:
                if line[0].toupper() != 'RET':
                    labels[line] = i
                else:
                    instructions[i] = '10010000000000000000000000011110'
            if len(line) == 4:
                opcode = ''
                try:
                    line[-1] = int(line[-1])
                    opcode = get_opcode(line[0]+'imm')
                except:
                    opcode = get_opcode(line[0]+'reg')

                

            opcode, imm = get_opcode(line[0])
            dst_reg = format(int(line[1][1]), '02b')
            reg_1 = format(int(line[2][1]), '02b')
            last_8 = format(int(line[3]), '08b') if (imm) else format(int(line[3][1]), '02b') + '000000'

            hexadecimal = to_hex(opcode + dst_reg + reg_1 + last_8)
            instructions[i] = ((4 - len(hexadecimal)) * '0') + hexadecimal
            i += 1
    return instructions

def get_opcode(command):
    command = command.toupper()
    match command:
        case "ADDIMM":
            return '00001010010'


def to_hex(binary):
    # convert binary to int
    dec = int(binary, 2)
      
    # convert int to hexadecimal
    hexadecimal = format(dec, 'x')
    return(hexadecimal)
            

if __name__ == '__main__':
    input_name = input("Write the name of a txt file to read instructions from (Must be in same directory as this assembler): ")
    output_name = input("Write the name of a txt file to output the machine code to: ")
    make_image(input_name if input_name != '' else 'instructions.txt', output_name if output_name != '' else 'instruction_image.txt')