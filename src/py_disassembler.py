import dis, marshal
import os, sys
import py_compile
import tempfile
import traceback

''' if python version less than 3.3, the length of pyc file's 
magic and timestamp header is 8, otherwise is 12'''
header_size = 12 if sys.version_info >= (3, 3) else 8

def compile_py(pyfile, target=None):
    """ Compile a .py file to a temp file
    """
    if not target:
        target = tempfile.mkstemp()[1]
    py_compile.compile(pyfile, target)
    return target
    

def dis_pyc(pycfile):
    """ Disassembling a .pyc file
    """
    with open(pycfile, "rb") as f:
        magic_and_timestamp = f.read(header_size)
        code = marshal.load(f)
    dis.dis(code)

def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: python py_disassembler.py <py/pyc/pyo_file>")
        return
    try:
        source = args[-1]
        if source.endswith(".pyc"):
            dis_pyc(args[-1])
        elif source.endswith(".py"):
            temp = compile_py(source)
            dis_pyc(temp)
            os.unlink(temp)
    except:
        traceback.print_exc()

if __name__ == "__main__":
    main()

