'''
构建编译器
'''
import sys
import os

from Front_end import lexer
from Front_end import parser
from Front_end import AST_Dumper
from Front_end import Symbol_table
from Front_end import semantics_Analyze
import Gen_IntermediateCode

class Compiler(object):
    def __init__(self, sourceFileName):
        self.file = sourceFileName
        self.Abstract_Syntax_Tree = None
        self.symbol_table = None

    def analyze(self):
        lexerObj = lexer.lexer(debug = False)
        parserObj = parser.parser(debug = False)

        def get_source_data(filename):
            if filename == '-':
                data = sys.stdin.read()
            else:
                with open(filename, 'r', encoding = 'utf-8') as sourceF:
                    data = sourceF.read()
            return data

        data = get_source_data(self.file)

        # 打印源程序[For Debug]
        # print('-' * 30 + ' Source Program ' + '-' * 30)
        # print(data)
        # print('-' * 28 + ' Source Program end ' + '-' * 28)
        
        # 打印tokens[For Debug]
        # lexerObj.input(data)
        # print('-' * 30 + ' tokens ' + '-' * 30)
        # for tok in lexerObj:
        #     print(tok)
        # print('-' * 28 + ' tokens end ' + '-' * 28)

        self.Abstract_Syntax_Tree = parserObj.parse(input = data, lexer = lexerObj, tracking = True)
        # print(self.Abstract_Syntax_Tree)    # 打印出的是ProgDef,即根节点
        if not self.Abstract_Syntax_Tree:
            print("Abstract Syntax Tree can't be built!")
            sys.exit(1)

    def show_AST(self):
        if self.Abstract_Syntax_Tree:
            print("The Abstract Syntax Tree is: ")
            AST_Dumper.showNode(self.Abstract_Syntax_Tree, 0)
        else:
            print("The Abstract Syntax Tree is None...")
            
    def gen_symbol_table(self):
        symbol_table_obj = Symbol_table.SymbolTable(self.Abstract_Syntax_Tree)
        symbol_table_obj.generate_symbolTable()
        self.symbol_table = symbol_table_obj
        self.symbol_table.print_SymbolTable()

    def semantics_analyze(self):
        rootNode = self.Abstract_Syntax_Tree
        symbol_table = self.symbol_table
        semantics_analyze_obj = semantics_Analyze.SemanticsAnalyze(rootNode, symbol_table)
        semantics_analyze_obj.analyze()
        semantics_analyze_obj.print_newSymbolTable()

    def gen_intermedia_code(self):
        rootNode = self.Abstract_Syntax_Tree
        ic_generator_obj = Gen_IntermediateCode.IC_Generator(rootNode)
        ic_generator_obj.print_IC()
        ic_generator_obj.storeIC()  # 将四元式保存在文件中

