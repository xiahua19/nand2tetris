from handle_whitespace import handle_whitespace

def instruction_typeis_a(instruction : str) -> bool:
    """Determine whether the type of an instruction is a

    Args:
        instruction (str): one instruction

    Returns:
        bool: whether the type of an instruction is a
    """
    import re
    a_instruction = re.compile(r'^@.*')
    
    if (a_instruction.match(instruction)):
        return True
    return False

def instruction_typeis_label(instruction : str) -> bool:
    """Determine whether the type of an instruction is label

    Args:
        instruction (str): one instruction

    Returns:
        bool: whether the type of an instruction is label
    """
    import re
    a_instruction = re.compile(r'^\(.*\)$')
    
    if (a_instruction.match(instruction)):
        return True
    return False


def translate_instruction_a(instruction : str, symbol_table : list) -> str:
    """translate a-intruction 

    Args:
        instruction (str): the a-instruction
        symbol_table (list): symbol_table used for translate a-instruction
    
    Return: the a-intruction in machine language
    """
    symbol = instruction[1:]
    if symbol in symbol_table:
        value16bit = bin(symbol_table[symbol])[2:].zfill(16)
        return value16bit
    else:
        return bin(int(symbol))[2:].zfill(16)
        

def translate_instruction_c(instruction : str, dest_dict : dict, comp_dict : dict, jump_dict : dict) -> str:
    """translate c-instruction

    Args:
        instruction (str): the c-instruction

    Returns:
        str: the c-intruction in machine language
    """
    import re
    has_dest_jump = re.compile(r'^.*=.*;.*')
    no_dest = re.compile(r'^.*;.*')
    no_jump = re.compile(r'.*=.*')


    if has_dest_jump.match(instruction):
        dest = instruction.split('=')[0].strip()
        comp = instruction.split('=')[1].split(';')[0].strip()
        jump = instruction.split('=')[1].split(';')[1].strip()
        
        dest16value = dest_dict[dest]
        comp16value = comp_dict[comp] if comp in comp_dict else '000'
        jump16value = jump_dict[jump] if jump in jump_dict else '000'

        return '111' + comp16value + dest16value + jump16value
    
    elif no_dest.match(instruction):
        comp = instruction.split(';')[0].strip()
        jump = instruction.split(';')[1].strip()
        
        comp16value = comp_dict[comp] if comp in comp_dict else '000'
        jump16value = jump_dict[jump] if jump in jump_dict else '000'

        return '111' + comp16value + '000' + jump16value
    
    elif no_jump.match(instruction):
        dest = instruction.split('=')[0].strip()
        comp = instruction.split('=')[1].split(';')[0].strip()

        dest16value = dest_dict[dest]
        comp16value = comp_dict[comp] if comp in comp_dict else '000'
        
        return '111' + comp16value + dest16value + '000'

def get_symbol_table(full_asm : list) -> dict:
    """Get the symbol table of a .asm file

    Args:
        full_asm (list): list of code in a .asm file, which has been remove all whitespaces

    Returns:
        dict: symbol table {symbol : int}
    """
    import re

    # init the symbol_table
    symbol_table = dict()

    # add all pre-defined symbols to symbol_table
    some_defined_symbols = ['SP', 'LCL', 'ARG', 'THIS', 'THAT']
    for i in range(len(some_defined_symbols)):
        symbol_table[some_defined_symbols[i]] = i
    for i in range(16):
        symbol_table[f'R{i}'] = i
    symbol_table['SCREEN'] = 16384
    symbol_table['KBD'] = 24576    

    label_num = 0
    start_addr = 16
    # select the label and variable symbols, add them to symbol_table
    for i in range(len(full_asm)):
        line = full_asm[i]

        label_pattern = re.compile(r'^\(.*\)$')
        if label_pattern.match(line):
            label = line[1:][:-1]
            address = i - label_num
            label_num += 1
            symbol_table[label] = address

        if instruction_typeis_a(line):
            symbol = line[1:]
            if symbol not in symbol_table and not symbol.isdigit():
                symbol_table[symbol] = start_addr
                start_addr += 1
    
    return symbol_table

def get_c_comp_dict():
    return {
        '0' : '0101010',
        '1' : '0111111',
        '-1' : '0111010',
        'D' : '0001100',
        'A' : '0110000',
        'M' : '1110000',
        '!D' : '0001101',
        '!A' : '0110001',
        '!M' : '1110001',
        '-D' : '0001111',
        '-A' : '0110011',
        '-M' : '1110011',
        'D+1' : '0011111',
        'A+1' : '0110111',
        'M+1' : '1110111',
        'D-1' : '0001110',
        'A-1' : '0110010',
        'M-1' : '1110010',
        'D+A' : '0000010',
        'D+M' : '1000010',
        'D-A' : '0010011',
        'D-M' : '1010011',
        'A-D' : '0000111',
        'M-D' : '1000111',
        'D&A' : '0000000',
        'D&M' : '1000000',
        'D|A' : '0010101',
        'D|M' : '1010101'
    }

def get_c_dest_dict():
    return {
        'M' : '001',
        'D' : '010',
        'MD' : '011',
        'A' : '100',
        'AM' : '101',
        'AD' : '110',
        'AMD' : '111'
    }

def get_c_jump_dict():
    return {
        'JGT' : '001',
        'JEQ' : '010',
        'JGE' : '011',
        'JLT' : '100',
        'JNE' : '101',
        'JLE' : '110',
        'JMP' : '111'
    }

if __name__ == '__main__':
    import sys
    args = sys.argv
    assert len(args) == 2

    handled_code = handle_whitespace(file_path=args[1])
    symbol_table = get_symbol_table(full_asm=handled_code)
    print(symbol_table)
    c_dest = get_c_dest_dict()
    c_comp = get_c_comp_dict()
    c_jump = get_c_jump_dict()

    machine_lang = []
    for line in handled_code:
        if instruction_typeis_a(line):
            machine_lang.append(translate_instruction_a(line, symbol_table))
        elif not instruction_typeis_label(line):
            machine_lang.append(translate_instruction_c(line, c_dest, c_comp, c_jump))
    
    # for lang in machine_lang:
    #     print(lang)
    with open(args[1].replace('asm', 'hack'), 'w') as file:
        for lang in machine_lang:
            file.write(lang + '\n')
