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


class InstructionA:
    def __init__(self, instruction : str, symbol_table : list):
        """Init this class

        Args:
            instruction (str): the a-instruction
            symbol_table (list): symbol_table used for translate a-instruction
        """
        self.instruction = instruction
        self.symbol_table = symbol_table
    
    def translate(self) -> str:
        symbol = self.instruction[1:]
        value = self.symbol_table[symbol]
        value16bit = bin(value)[2:].zfill(16)
        return value16bit
        
class InstructionC:
    def __init__(self, instruction : str):
        """Init this class

        Args:
            instruction (str): the c-instruction
        """
        self.instruction = instruction
    
    def translate(self) -> str:
        pass
    