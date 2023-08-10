from handle_whitespace import handle_whitespace

class VMParser:
    """Handles the parsing of a single .vm file.
       1. Reads a VM command, parses the command into its lexical components, 
       and provides convenient access to these components.
       2. Ignores all white space and comments.
       3. Generates assembly code from the parsed VM command.
    """
    def __init__(self, vmfile_name : str, asmfile_name : str):
        """Open the input file/stream and gets ready to parse it.

        Args:
            vmfilename (str): .vm file path
            asmfile_name (str): the translated .asm file path
        """
        # vm instructions removed whitespace 
        self.vm_instructions = handle_whitespace(file_path=vmfile_name)
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
        self.asmfile_name = asmfile_name
        # memory segments
        self.segments = ['local', 'argument', 'this', 'that', 'constant', 'static', 'pointer', 'temp']
        # segments pointer
        self.seg_pointers = {
            'local' : 1,
            'argument' : 2,
            'this' : 3,
            'that' : 4,
            'temp' : 5
        }

    def instruction_type(self, vm_instruction : str):
        """Returns a constant representing the type of the current command.
           C_ARITHMETIC is returned for all the arithmetic/logical commands
        """
        if vm_instruction in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
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

    def translate_push(self, vm_instruction : str):
        """Translates to the output the assembly code that implements the given command, where command is C_PUSH.

        Args:
            instruction (str): _description_
        """
        self.translated_code.append('// ' + vm_instruction) # hold the vm instruction for debugging

        command, segment, num = vm_instruction.split(' ')
        assert command == 'push' and segment in self.segments

        if segment in self.seg_pointers: # if segment is local, argument, this, that or temp
            pass
        elif segment == 'constant':
            pass
        elif segment == 'static':
            pass
        elif segment == 'pointer':
            pass
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
    
        if segment in self.seg_pointers: # if segment is local, argument, this, that or temp
            pass
        elif segment == 'constant':
            pass
        elif segment == 'static':
            pass
        elif segment == 'pointer':
            pass
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
        with open(self.asmfile_name, 'w') as file:
            for lang in self.translated_code:
                file.write(lang + '\n')