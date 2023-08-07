def handle_whitespace(file_path : str) -> list:
    """handle whitespace
    Given the .asm file path, this function will do the below things:
    (1) reads the asm code in this file;
    (2) remove all white space in this code, white space is:
        a. Empty lines/ indentation
        b. line comments
        c. in-line comments
    (3) return the processed code
    Args:
        file_path (str): path of the .asm file

    Returns:
        list: a list of strings, every string is one line of processed code, in original order
    """
    import re
    # line comment
    line_comment = re.compile(r'^//.*')
    # empty line
    empty_line = re.compile(r'^$')
    # in-line comment
    inline_comment = re.compile(r'.*//.*')


    handled_code = []
    with open (file_path, 'r') as file:
        for line in file:
            if (line_comment.match(line)):
                continue
            elif (empty_line.match(line)):
                continue
            elif (inline_comment.match(line)):
                line = re.sub('//.*', '', line)
                line = line.strip()
                handled_code.append(line)
            else:
                line = line.strip()
                handled_code.append(line)
    
    return handled_code

if __name__ == '__main__':
    import sys
    args = sys.argv
    assert len(args) == 2

    handled_code = handle_whitespace(args[1])
    for line in handled_code:
        print(line)

