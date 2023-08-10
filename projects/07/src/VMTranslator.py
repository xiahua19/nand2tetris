from vmparser import VMParser
if __name__ == '__main__':
    import sys
    args = sys.argv
    assert len(args) == 2
    
    vmparser = VMParser(vmfile_name=args[1], asmfile_name=args[1].replace('.vm', '.asm'))
    vmparser.all()