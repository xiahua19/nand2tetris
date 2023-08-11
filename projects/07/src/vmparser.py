from handle_whitespace import handle_whitespace

class VMParser:
    """Handles the parsing of a single .vm file.
       1. Reads a VM command, parses the command into its lexical components, 
       and provides convenient access to these components.
       2. Ignores all white space and comments.
       3. Generates assembly code from the parsed VM command.
    """
    def __init__(self, vmfile_path : str, asmfile_path : str):
        """Open the input file/stream and gets ready to parse it.

        Args:
            vmfilename (str): .vm file path
            asmfile_name (str): the translated .asm file path
        """
        # vm instructions removed whitespace 
        self.vm_instructions = handle_whitespace(file_path=vmfile_path)
        # vm file name
        self.vmfile_name = vmfile_path.split('/')[-1].split('.')[0]
        # instruction type codes
        self.C_ARITHMETIC = 1
        self.C_PUSH = 2
        self.C_POP = 3
        self.C_LABEL = 4
        self.C_GOTO = 5
        self.C_IF = 6
        self.C_FUNCTION = 7
        self.C_RETURN = 8
        self.C_CALL = 9
        # translated .asm code
        self.translated_code = []
        # translated .asm file path
        self.asmfile_path = asmfile_path
        # memory segments
        self.segments = ['local', 'argument', 'this', 'that', 'constant', 'static', 'pointer', 'temp']
        # segments pointer
        self.seg_info = {
            'local' : {'pointer': 1, 'abbreviate' : 'R1'},
            'argument' : {'pointer' : 2, 'abbreviate' : 'R2'},
            'this' : {'pointer': 3, 'abbreviate' : 'R3'},
            'that' : {'pointer' : 4, 'abbreviate' : 'R4'},
        }
        # THIS, THAT map
        self.this_that = {
            '0' : 'THIS',
            '1' : 'THAT'
        }
        # arithmetic / logical commands
        self.arithmetic_symbols = {
            1 : ['neg', 'not'],
            2 : ['add', 'sub' , 'gt', 'lt', 'and', 'or', 'eq']
        }
        # arithmetic / logical map
        self.arithmetic_map = {
            'neg' : '-', 
            'eq' : '==',
            'not' : 'not',
            'add' : '+', 
            'sub' : '-' ,
            'gt' : '>', 
            'lt' : '<', 
            'and' : 'and',
            'or' : 'or'
        }

    def instruction_type(self, vm_instruction : str):
        """Returns a constant representing the type of the current command.
           C_ARITHMETIC is returned for all the arithmetic/logical commands
        """
        if vm_instruction in self.arithmetic_symbols[1] or vm_instruction in self.arithmetic_symbols[2]:
            return self.C_ARITHMETIC
        if 'push' in vm_instruction:
            return self.C_PUSH
        if 'pop' in vm_instruction:
            return self.C_POP
        # more type need to be handle in project 8 ...

    def translate_arithmetic(self, vm_instruction : str):
        """Translates to the output the assembly code that implements the given arithmetic command.

        Args:
            instruction (str): _description_
        """
        self.translated_code.append('// ' + vm_instruction) # hold the vm instruction for debugging
        
        if vm_instruction in self.arithmetic_symbols[2]:
            self.translated_code.append('@SP')
            self.translated_code.append('M=M-1')
            self.translated_code.append('A=M')
            self.translated_code.append('D=M')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M-1')
            self.translated_code.append('M=M' + self.arithmetic_map[vm_instruction] + 'D')
        elif vm_instruction in self.arithmetic_symbols[1]:
            self.translated_code.append('@SP')
            self.translated_code.append('A=M-1')
            self.translated_code.append('M=' + self.arithmetic_map[vm_instruction] + 'M')

    def translate_push(self, vm_instruction : str):
        """Translates to the output the assembly code that implements the given command, where command is C_PUSH.

        Args:
            instruction (str): _description_
        """
        self.translated_code.append('// ' + vm_instruction) # hold the vm instruction for debugging

        command, segment, num = vm_instruction.split(' ')
        assert command == 'push' and segment in self.segments

        if segment in self.seg_info: # if segment is local, argument, this, that
            self.translated_code.append(f'@{num}')
            self.translated_code.append('D=A')
            self.translated_code.append('@' + self.seg_info[segment]['abbreviate'])
            self.translated_code.append('A=M+D')
            self.translated_code.append('D=M')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M+1')
        elif segment == 'temp':
            self.translated_code.append(f'@{int(num) + 5}')
            self.translated_code.append('D=M')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M+1')          
        elif segment == 'constant':
            self.translated_code.append(f'@{num}')
            self.translated_code.append('D=A')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M+1')
        elif segment == 'static':
            self.translated_code.append('@' + self.vmfile_name + '.' + str(num))
            self.translated_code.append('D=M')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M+1')
        elif segment == 'pointer':
            self.translated_code.append('@' + self.this_that[num])
            self.translated_code.append('D=M')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M+1')
        else:
            raise NotImplementedError

    def translate_pop(self, vm_instruction : str):
        """Translates to the output file the assembly code that implements the given command, where command is C_POP.

        Args:
            instruction (str): _description_
        """
        self.translated_code.append('// ' + vm_instruction) # hold the vm instruction for debugging

        command, segment, num = vm_instruction.split(' ')
        assert command == 'pop' and segment in self.segments
    
        if segment in self.seg_info: # if segment is local, argument, this, that
            self.translated_code.append('@' + num)
            self.translated_code.append('D=A')
            self.translated_code.append('@' + self.seg_info[segment]['abbreviate'])
            self.translated_code.append('M=D+M')
            self.translated_code.append('@SP')
            self.translated_code.append('M=M-1')
            self.translated_code.append('A=M')
            self.translated_code.append('D=M')
            self.translated_code.append('@' + self.seg_info[segment]['abbreviate'])
            self.translated_code.append('A=M')
            self.translated_code.append('M=D')
            self.translated_code.append('@' + num)
            self.translated_code.append('D=A')
            self.translated_code.append('@' + self.seg_info[segment]['abbreviate'])
            self.translated_code.append('M=M-D')
        elif segment == 'temp':
            self.translated_code.append('@SP')
            self.translated_code.append('M=M-1')
            self.translated_code.append('A=M')
            self.translated_code.append('D=M')
            self.translated_code.append(f'@{int(num) + 5}')
            self.translated_code.append('M=D')
        elif segment == 'static':
            self.translated_code.append('@SP')
            self.translated_code.append('M=M-1')
            self.translated_code.append('@SP')
            self.translated_code.append('A=M')
            self.translated_code.append('D=M')
            self.translated_code.append('@' + self.vmfile_name + '.' + str(num))
            self.translated_code.append('M=D')
        elif segment == 'pointer':
            self.translated_code.append('@SP')
            self.translated_code.append('M=M-1')
            self.translated_code.append('A=M')
            self.translated_code.append('D=M')
            self.translated_code.append('@' + self.this_that[num])
            self.translated_code.append('M=D')
        else:
            raise NotImplementedError

    def all(self):
        """Process and translate .vm code line by line.
        """
        for vm_instruction in self.vm_instructions:
            instruction_type = self.instruction_type(vm_instruction)
            if instruction_type == self.C_ARITHMETIC:
                self.translate_arithmetic(vm_instruction)
            elif instruction_type == self.C_PUSH:
                self.translate_push(vm_instruction)
            elif instruction_type == self.C_POP:
                self.translate_pop(vm_instruction)
            else:
                raise NotImplementedError
        with open(self.asmfile_path, 'w') as file:
            for lang in self.translated_code:
                file.write(lang + '\n')

if __name__ == '__main__':
    import sys
    args = sys.argv
    assert len(args) == 2
    
    vmparser = VMParser(vmfile_path=args[1], asmfile_path=args[1].replace('.vm', '.asm'))
    vmparser.all()