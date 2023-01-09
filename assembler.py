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
        input = input.read().split('\n')
        i = 0
        # find all labels first
        # perhaps do a first loop where each line is changed to its split version. If the length is one add it to labels
        # can also do every instruction that isn't a branching command
        # Then a second loop that takes care of all the branching commands that need their offsets to be calculated
        for line in input:
            line = line.split(' ')
            
            if len(line) == 1:
                if line[0].upper() != 'RET':
                    labels[line[0]] = i
                else:
                    instructions[i] = to_hex('10010000000000000000000000011110')
            elif len(line) == 4:
                opcode = ''
                dst_reg = format(int(line[1][1:]), '05b')
                reg_1 = format(int(line[2][1:]), '05b')
                hexadecimal = ''
                try:
                    line[3] = int(line[3])
                    opcode = get_opcode(line[0]+'imm')
                    imm = format(line[3], '011b')
                    hexadecimal = to_hex(opcode + imm + reg_1 + dst_reg)
                except ValueError:
                    opcode = get_opcode(line[0]+'reg')
                    reg_2 = format(int(line[3][1:]), '05b')
                    hexadecimal = to_hex(opcode + reg_2 + '111000' + reg_1 + dst_reg)
                input[i] = (8 - len(hexadecimal)) * '0' + hexadecimal
            i += 1
        i = 0
        for line in input:
            line = line.split(' ')
            if line[0].upper() == 'B' or line[0].upper() == 'BL':
                opcode = get_opcode(line[0])
                imm = format(labels[line[1]] - i, '011b')
                hexadecimal = to_hex(opcode + imm + '0000011110')
                input[i] = (8 - len(hexadecimal)) * '0' + hexadecimal
            elif line[0].upper() == 'CBZ':
                opcode = get_opcode(line[0])
                imm = format(labels[line[2]], '011b')
                target_reg = format(int(line[1][1:]))
                hexadecimal = to_hex(opcode + imm + '00000' + target_reg)
                input[i] = (8 - len(hexadecimal)) * '0' + hexadecimal
            i += 1
    return instructions

def get_opcode(command):
    command = command.upper()
    match command:
        case 'ADDREG':
            return '00001010010'
        case 'ADDIMM':
            return '00001000010'
        case 'SUBREG':
            return '00001110010'
        case 'SUBIMM':
            return '0000100010'
        case 'ANDREG':
            return '00000010010'
        case 'ANDIMM':
            return '00000000010'
        case 'ORRREG':
            return '00000110010'
        case 'ORRIMM':
            return '00000100010'
        case 'ADDSREG':
            return '00011010010'
        case 'ADDSIMM':
            return '00011000010'
        case 'SUBSREG':
            return '00011110010'
        case 'SUBSIMM':
            return '00011100010'
        case 'ANDSREG':
            return '00010110010'
        case 'ANDSIMM':
            return '00010100010'
        case 'LDRREG':
            return '00001011010'
        case 'LDRIMM':
            return '00001001010'
        case 'STRREG':
            return '00001010110'
        case 'STRIMM':
            return '00001000110'
        case 'B':
            return '00110000000'
        case 'BL':
            return '00110000011'
        case 'CBZ':
            return '01010000000'
        case 'RET':
            return '10010000000'


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