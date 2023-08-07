from instruction import instruction_typeis_a
from handle_whitespace import handle_whitespace

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

if __name__ == '__main__':
    import sys
    args = sys.argv
    assert len(args) == 2

    handled_code = handle_whitespace(file_path=args[1])
    print(handled_code)
    symbol_table = get_symbol_table(full_asm=handled_code)
    print(symbol_table)
