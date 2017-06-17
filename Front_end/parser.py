'''
MiniPascal 语法分析器

实现了以下文法(MiniPascal)并作适当修改：
Mini_Pascal_grammar.txt
''' 
import ply.yacc as yacc
import logging

# Get the token map from the lexer. [必须]
# from Front_end.lexer import tokens
from Front_end.lexer import *
from Front_end.Abstract_Syntax_Tree import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),     # Unary minus operator(%prec UMINUS覆盖了默认的优先级（MINUS的优先级），将UMINUS指代的优先级应用在该语法规则上)
)

from enum import Enum
statement_type = Enum('statement_type', ('assignStat', 'compoundStat', 'ifStat', 'whileStat', 'forStat', 'gotoStat', 'caseStat'))

def getPosition(p, num):
    line = p.lineno(num)
    span = p.lexspan(num)

    class PositionInfo(object):
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

        def __str__(self):
            return str(self.lineno)

    return PositionInfo(lineno = line, lexpos = span[0], lexendpos = span[1])

# ProgDef:     program Iden ';' SubProg '.'
# SubProg:     VarDef compound_statement

def p_ProgDef(p):
    'ProgDef : PROGRAM ID SEMICOLON SubProg ENDPOINT'
    p[0] = ProgramNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)

def p_SubProg(p):
    'SubProg : VarDef compound_statement'
    p[0] = SubProgNode(p[1], p[2])
    p[0].pos_info = getPosition(p, 0)

# *******************************************************************************************
# ------------------- 变量声明的文法(未加入数组时——>备份) ------------------------

# VarDef:      Var VarDefList ';'
# VarDefList:  VarDefList ';' VarDefState | VarDefState
# VarDefState: VarList ':' Type
# VarList:     VarList ',' Variable | Variable
# Type:        Integer | Real
# Variable:    Iden

# def p_VarDef(p):
#     'VarDef : VAR VarDefList SEMICOLON'
#     p[0] = VarDefNode(p[2])
#     p[0].pos_info = getPosition(p, 0)

# def p_VarDefList_1(p):
#     'VarDefList : VarDefList SEMICOLON VarDefState'
#     p[0] = VarDefListNode(p[3], p[1])
#     p[0].pos_info = getPosition(p, 0)

# def p_VarDefList_2(p):
#     'VarDefList : VarDefState'
#     p[0] = VarDefListNode(p[1])
#     p[0].pos_info = getPosition(p, 0)

# def p_VarDefState(p):
#     'VarDefState : VarList COLON Type'
#     p[0] = VarDefStateNode(p[1], p[3])
#     p[0].pos_info = getPosition(p, 0)

# def p_VarList_1(p):
#     'VarList : VarList COMMA Variable'
#     p[0] = VarListNode(p[3], p[1])
#     p[0].pos_info = getPosition(p, 0)

# def p_VarList_2(p):
#     'VarList : Variable'
#     p[0] = VarListNode(p[1])
#     p[0].pos_info = getPosition(p, 0)

# def p_type_1(p):
#     'Type : INTEGER'    # INTEGER关键字
#     p[0] = p[1]

# def p_type_2(p):
#     'Type : REAL'   # REAL关键字
#     p[0] = p[1]

# def p_type_3(p):
#     'Type : BOOLEAN'
#     p[0] = p[1]

# def p_variable_id(p):
#     'Variable : ID'
#     # p[0] = p[1]   # 这样写貌似不对
#     p[0] = IdNode(p[1])
#     p[0].pos_info = getPosition(p, 0)

# *******************************************************************************************

# ========================= [变量声明的文法]添加对数组的文法支持(6.17) =============================

# VarDef:         Var VarDefList ';'
# VarDefList:     VarDefList ';' VarDefState | VarDefState
# VarDefState:    VarList ':' Type
#                 | ArrayDefState
# VarList:        VarList ',' Variable | Variable
# Type:           Integer | Real | BOOLEAN | arrayName
# Variable:       Iden

# ArrayDefState:  TYPE arrayName '=' ARRAY '[' index_list ']' OF Type
# arrayName:      Iden
# index_list:     index_list ',' index | index
# index:          startIndex '.''.' endIndex
# startIndex:     Const
# endIndex:       Const

def p_VarDef(p):
    'VarDef : VAR VarDefList SEMICOLON'
    p[0] = VarDefNode(p[2])
    p[0].pos_info = getPosition(p, 0)

def p_VarDefList_1(p):
    'VarDefList : VarDefList SEMICOLON VarDefState'
    p[0] = VarDefListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)

def p_VarDefList_2(p):
    'VarDefList : VarDefState'
    p[0] = VarDefListNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_VarDefState_1(p):
    'VarDefState : VarList COLON Type'
    p[0] = VarDefStateNode(Varlist = p[1], Type = p[3])
    p[0].pos_info = getPosition(p, 0)

def p_VarDefState_2(p):
    'VarDefState : ArrayDefState'
    p[0] = VarDefStateNode(ArrayDefState = p[1])
    p[0].pos_info = getPosition(p, 0)

def p_VarList_1(p):
    'VarList : VarList COMMA Variable'
    p[0] = VarListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)

def p_VarList_2(p):
    'VarList : Variable'
    p[0] = VarListNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_ArrayDefState(p):
    'ArrayDefState : TYPE arrayName EQ ARRAY LBRAC index_list RBRAC OF Type'
    p[0] = ArrayNode(p[2], p[6], p[9])
    p[0].pos_info = getPosition(p, 0)

def p_arrayName(p):
    'arrayName : ID'
    p[0] = IdNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_index_list_1(p):
    'index_list : index_list COMMA index'
    p[0] = IndexListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)

def p_index_list_2(p):
    'index_list : index'
    p[0] = IndexListNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_index(p):
    'index : startIndex DOTDOT endIndex'
    p[0] = IndexNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_type_1(p):
    'Type : INTEGER'    # INTEGER关键字
    p[0] = p[1]

def p_type_2(p):
    'Type : REAL'   # REAL关键字
    p[0] = p[1]

def p_type_3(p):
    'Type : BOOLEAN'
    p[0] = p[1]

def p_type_4(p):
    'Type : arrayName'
    p[0] = p[1]

def p_variable_id(p):
    'Variable : ID'
    # p[0] = p[1]   # 这样写貌似不对
    p[0] = IdNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_startIndex(p):
    'startIndex : const'
    p[0] = p[1]

def p_endIndex(p):
    'endIndex : const'
    p[0] = p[1]
# ================== [变量声明的文法]添加对数组的文法支持(6.17) end ====================


#------------------------- 语句Statement的文法 ------------------------

# ******************* 原始的关于Statement的文法 *******************
# StateList:   S_L Statement | Statement
# S_L:         StateList ';'
# 将上面两条合并为一条如下：
# StateList:   StateList ';' Statement | Statement
# 
# Statement:   AsignState
#             | ISE Statement
#             | IBT Statement
#             | WBD Statement
#             | CompState
# 
# CompState:   Begin StateList End
# AsignState:  Variable':''='Expr
# ISE:         IBT Statement Else
# IBT:         If BoolExpr Then
# WBD:         while BoolExpr Do
# ******************* 原始的关于Statement的文法 *******************

# ————————————————————————————————————————————————————————————————————————————————————————————
# 改造文法：从[http://www.moorecad.com/standardpascal/pascal.y]上找到官方关于statement的文法

# StateList : StateList ';' Statement | Statement

# Statement : open_statement
#           | closed_statement

# open_statement : label COLON non_labeled_open_statement
#                | non_labeled_open_statement

# closed_statement : label COLON non_labeled_closed_statement
#                  | non_labeled_closed_statement

# non_labeled_open_statement : open_if_statement
#                            | open_while_statement
#                            | open_for_statement

# non_labeled_closed_statement : assignment_statement
#                              | compound_statement
#                              | closed_if_statement
#                              | closed_while_statement
#                              | closed_for_statement
#                              | goto_statement
#                              | case_statement   [暂未实现]
#                              | empty

# open_if_statement   : IF BoolExpr THEN Statement
#                     | IF BoolExpr THEN closed_statement ELSE open_statement
# closed_if_statement : IF BoolExpr THEN closed_statement ELSE closed_statement

# open_while_statement   : WHILE BoolExpr DO open_statement
# closed_while_statement : WHILE BoolExpr DO closed_statement

# open_for_statement   : FOR Variable ASSIGNMENT initial_value direction final_value DO open_statement
# closed_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO closed_statement

# initial_value : Expr
# final_value : Expr
# direction : TO
#           | DOWNTO

# assignment_statement : Variable ASSIGNMENT Expr

# compound_statement : BEGIN StateList END

# goto_statement : GOTO label
# label : DIGSEQ

# ————————————————————————————————————————————————————————————————————————————————————————————

def p_statementList_1(p):
    'StateList : StateList SEMICOLON Statement'
    p[0] = StateListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)

def p_statementList_2(p):
    'StateList : Statement'
    p[0] = StateListNode(p[1])
    p[0].pos_info = getPosition(p, 0)

def p_statement_1(p):
    'Statement : open_statement'
    p[0] = p[1]

def p_statement_2(p):
    'Statement : closed_statement'
    p[0] = p[1]

def p_open_statement_1(p):
    'open_statement : label COLON non_labeled_open_statement'
    p[0] = LabeledStatementNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_open_statement_2(p):
    'open_statement : non_labeled_open_statement'
    p[0] = p[1]

def p_closed_statement_1(p):
    'closed_statement : label COLON non_labeled_closed_statement'
    p[0] = LabeledStatementNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_closed_statement_2(p):
    'closed_statement : non_labeled_closed_statement'
    p[0] = p[1]

def p_non_labeled_open_statement_1(p):
    'non_labeled_open_statement : open_if_statement'
    p[0] = p[1]

def p_non_labeled_open_statement_2(p):
    'non_labeled_open_statement : open_while_statement'
    p[0] = p[1]

def p_non_labeled_open_statement_3(p):
    'non_labeled_open_statement : open_for_statement'
    p[0] = p[1]

def p_non_labeled_closed_statement_1(p):
    'non_labeled_closed_statement : assignment_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.assignStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_2(p):
    'non_labeled_closed_statement : compound_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.compoundStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_3(p):
    'non_labeled_closed_statement : closed_if_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.ifStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_4(p):
    'non_labeled_closed_statement : closed_while_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.whileStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_5(p):
    'non_labeled_closed_statement : closed_for_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.forStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_6(p):
    'non_labeled_closed_statement : goto_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.gotoStat)
    p[0].pos_info = getPosition(p, 0)

def p_non_labeled_closed_statement_7(p):
    'non_labeled_closed_statement : empty'
    pass

# [暂时没实现case]
# def p_non_labeled_closed_statement_8(p):
#     'non_labeled_closed_statement : case_statement'
#     p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.caseStat)

def p_open_if_statement_1(p):
    'open_if_statement : IF BoolExpr THEN Statement'
    p[0] = IfNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)

def p_open_if_statement_2(p):
    'open_if_statement : IF BoolExpr THEN closed_statement ELSE open_statement'
    p[0] = IfNode(p[2], p[4], p[6])
    p[0].pos_info = getPosition(p, 0)
    
def p_closed_if_statement(p):
    'closed_if_statement : IF BoolExpr THEN closed_statement ELSE closed_statement'
    p[0] = IfNode(p[2], p[4], p[6])
    p[0].pos_info = getPosition(p, 0)

def p_open_while_statement(p):
    'open_while_statement : WHILE BoolExpr DO open_statement'
    p[0] = WhileNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)

def p_closed_while_statement(p):
    'closed_while_statement : WHILE BoolExpr DO closed_statement'
    p[0] = WhileNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)

def p_open_for_statement(p):
    'open_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO open_statement'
    p[0] = ForNode(p[2], p[4], p[5], p[6], p[8])
    p[0].pos_info = getPosition(p, 0)

def p_closed_for_statement(p):
    'closed_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO closed_statement'
    p[0] = ForNode(p[2], p[4], p[5], p[6], p[8])
    p[0].pos_info = getPosition(p, 0)

def p_initial_value(p):
    'initial_value : Expr'
    p[0] = p[1]

def p_final_value(p):
    'final_value : Expr'
    p[0] = p[1]

def p_direction_1(p):
    'direction : TO'
    p[0] = p[1]

def p_direction_2(p):
    'direction : DOWNTO'
    p[0] = p[1]

def p_assignment_statement(p):
    'assignment_statement : Variable ASSIGNMENT Expr'
    p[0] = AssignmentNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_compound_statement(p):
    'compound_statement : BEGIN StateList END'
    # p[0] = p[2]   # 建立语法分析树的时候,发现有错误,SubPorg的子结点compound_statement没有生成,后来发现是这里的下标写错了...把p[2]写成p[1]了
    # 上面这样写也是对的,对于后面的分析来说,和下面的把compound_statement单独建一个结点是等价的.但是为了打印出来的语法树更直观,就建立一个compound_statement结点，但是这个结点只有一个子节点(就是Statement_List)
    p[0] = CompoundStatementNode(p[2])
    p[0].pos_info = getPosition(p, 0)

def p_goto_statement(p):
    'goto_statement : GOTO label'
    p[0] = GotoNode(p[2])
    p[0].pos_info = getPosition(p, 0)

def p_label(p):
    'label : DIGSEQ'
    p[0] = p[1]


# def p_Statement_1(p):
#     'Statement : AsignState'
#     p[0] = StatementNode(AsignState = p[1])

# def p_Statement_2(p):
#     'Statement : ISE Statement'
#     p[0] = StatementNode(ISE = p[1], Statement = p[2])

# def p_Statement_3(p):
#     'Statement : IBT Statement'
#     p[0] = StatementNode(IBT = p[1], Statement = p[2])

# def p_Statement_4(p):
#     'Statement : WBD Statement'
#     p[0] = StatementNode(WBD = p[1], Statement = p[2])

# def p_Statement_5(p):
#     'Statement : CompState'
#     p[0] = StatementNode(CompState = p[1])

# def p_CompState(p):
#     'CompState : BEGIN StateList END'   # CompState 表示符合语句(compound statement)
#     p[0] = CompStateNode(p[2])

# def p_AsignState(p):
#     'AsignState : Variable ASSIGNMENT Expr'
#     P[0] = AsignStateNode(p[1], p[3])

# def p_ISE(p):
#     'ISE : IBT Statement ELSE'
#     p[0] = ISE_Node(p[1], p[2], p[3])

# def p_IBT(p):
#     'IBT : IF BoolExpr THEN'
#     p[0] = IBT_Node(p[2])

# def p_WBD(p):   # while循环
#     'WBD : WHILE BoolExpr DO Statement'
#     p[0] = WBD_Node(p[2], p[4])


# -------------------------------------------------------------------

# -------------------- 表达式Expression的文法--------------

# Expr:       Expr'+'Expr | Expr'-'Expr | Expr'*'Expr
#             | Expr'/'Expr | '('Expr')' | '-' Expr %prec UMINUS
#             | Variable | Const
# Const:      IntNo | RealNo

# ************** 只能对于简单的算术运算起作用 **************
# def p_expression_plus(p):
#     'Expr : Expr PLUS Expr'
#     p[0] = p[1] + p[3]

# def p_expression_minus(p):
#     'Expr : Expr MINUS Expr'
#     p[0] = p[1] - p[3]

# def p_expression_times(p):
#     'Expr : Expr TIMES Expr'
#     p[0] = p[1] * p[3]

# def p_expression_div(p):
#     'Expr : Expr DIVIDE Expr'
#     p[0] = p[1] / p[3]

# ************************** end **************************

def p_expression_plus(p):
    'Expr : Expr PLUS Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_expression_minus(p):
    'Expr : Expr MINUS Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_expression_times(p):
    'Expr : Expr TIMES Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_expression_div(p):
    'Expr : Expr DIVIDE Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_expr_Parentheses(p):
    'Expr : LPAREN Expr RPAREN'
    p[0] = p[2]

def p_expression_uminus(p):
    'Expr : MINUS Expr %prec UMINUS'
    p[0] = UnaryOpNode(p[1], p[2])
    p[0].pos_info = getPosition(p, 0)

def p_expression_variable(p):
    'Expr : Variable'
    p[0] = p[1]

def p_expression_const(p):
    'Expr : const'
    p[0] = p[1]

# 常量(整数和浮点数)
def p_const_INT_NUMBER(p):
    'const : INT_NUMBER'
    p[0] = p[1]

def p_const_REAL_NUMBER(p):
    'const : REAL_NUMBER'
    p[0] = p[1]

# -------------------- Expression end -------------------------

# -------------------- 布尔表达式BoolExpr的文法 --------------

# BoolExpr:    Expr RelationOp Expr | BoolExpr And BoolExpr | BoolExpr Or BoolExpr
#             | Not BoolExpr | '(' BoolExpr ')'
#             | Expr                                                                ——>[zcr补充]
# RelationOp:  '<' | '>' | '=' | GE | NE | LE

def p_BoolExpr_LT(p):
    'BoolExpr : Expr LT Expr'
    # p[0] = (p[1] < p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_LE(p):
    'BoolExpr : Expr LE Expr'
    # p[0] = (p[1] <= p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_GT(p):
    'BoolExpr : Expr GT Expr'
    # p[0] = (p[1] > p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_GE(p):
    'BoolExpr : Expr GE Expr'
    # p[0] = (p[1] >= p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_EQ(p):
    'BoolExpr : Expr EQ Expr'
    # p[0] = (p[1] == p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_NE(p):
    'BoolExpr : Expr NE Expr'
    p[0] = (p[1] != p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_AND(p):
    'BoolExpr : BoolExpr AND BoolExpr'
    # p[0] = p[1] and p[3]
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_OR(p):
    'BoolExpr : BoolExpr OR BoolExpr'
    # p[0] = p[1] or p[3]
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_NOT(p):
    'BoolExpr : NOT BoolExpr'
    # p[0] = not p[2]
    p[0] = UnaryBoolNode(p[1], p[2])    # 这里一元bool运算其实只有非运算(not)
    p[0].pos_info = getPosition(p, 0)

def p_BoolExpr_Parentheses(p):
    'BoolExpr : LPAREN BoolExpr RPAREN'
    p[0] = p[2]

def p_BoolExpr(p):
    'BoolExpr : Expr'
    p[0] = p[1]

# -------------------- BoolExpr end -------------------------


# 处理空产生式，这样就可以在其他产生式中使用empty这个标识了,后来发现没必要
def p_empty(p):
    'empty : '
    pass


# 处理错误的语法(
def report_error(prefix, msg, *args, **kwargs):
    logger = logging.getLogger(prefix)
    logger.error(msg, *args, **kwargs)

def p_error(p):
    print("Syntax error in input:")
    if p:
        report_error("grammar", "invalid token '%s' at %s line. (total Position: %d)" % (p.value, p.lineno, p.lexpos))
    else:
        report_error("grammar", "Unknown error")

# logging.basicConfig(
#     level = logging.DEBUG,
#     filename = "parselog.txt",
#     filemode = "w",
#     format = "%(filename)10s:%(lineno)4d:%(message)s"
# )
# log = logging.getLogger()

def parser(debug = True):
    tab = "parsetab"
    mod = sys.modules[__name__]
    # return yacc.yacc(debug = debug, debuglog = log, 
    return yacc.yacc(
                    optimize = 0, tabmodule = tab,
                    outputdir = os.path.dirname(__file__), module = mod)

if __name__ == '__main__':
    # 开发时测试用
    lexer()     # 构建词法分析器.如果没有,会报错:AttributeError: module 'ply.lex' has no attribute 'lexer'
    # Build the parser
    parser = yacc.yacc()
    print('parser: Done.')

    # 开发时测试用
    # while True:
    #     try:
    #        s = input('calc > ')
    #     except EOFError:
    #        break
    #     if not s:
    #         continue
    #     result = parser.parse(s)
    #     print(result)