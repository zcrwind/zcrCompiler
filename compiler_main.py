
import sys
import os

import compiler

def showUsage():
    print("Usage: python compiler_main.py inputFile -o outputFile")
    print("   -h: Show this message.")
    print("   -o: Specify the output file name")
    print("   -t: Show the abstract syntax tree")

def main():
    # print(len(sys.argv))    # 命令行参数个数(调试用)
    if len(sys.argv) < 2:
        print('Error: no input file.')
        showUsage()
        exit()

    InputFileName = None
    OutputFileName = None
    showAST = False
    testBasePath = 'SourceProg4Test/'    # 测试源程序所在的路径
    for arg in sys.argv[1:]:
        if arg == '-h':
            showUsage()
        elif arg == '-t':
            showAST = True
        elif InputFileName is None:
            InputFileName = testBasePath + arg
        elif arg == '-o':
            OutputFileName = None
        elif OutputFileName is None:
            OutputFileName = arg

    # print("the Inputfile is: %s" % InputFileName)
    # print("the OutputFile is: %s" % OutputFileName)

    compilerObj = compiler.Compiler(InputFileName)
    # print(compilerObj)

    # 测试一下__name__
    # print(compilerObj.__class__.__name__)   # 输出为 Compiler
    compilerObj.analyze()

    if showAST is True:
        compilerObj.show_AST()

    print('*' * 97)
    compilerObj.gen_symbol_table()

    print("semantics_analyze begin:")
    compilerObj.semantics_analyze()

    print("the Intermedia Codes are:")
    compilerObj.gen_intermedia_code()


if __name__ == '__main__':
    main()