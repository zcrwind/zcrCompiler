'''
功能：浮点数、字符串识别、boolean等

''' 
import sys
import os

import ply.lex as lex

import logging

logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# List of token names.
part_tokens = [
   'INT_NUMBER',    # 整数
   'REAL_NUMBER',   # 浮点数
   'ID',            # 标识符 Identifier
   'PLUS',          # +
   'MINUS',         # -
   'TIMES',         # *
   'DIVIDE',        # /
   'ASSIGNMENT',    # :=
   'SEMICOLON',     # ;
   'COLON',         # :
   'COMMA',         # ,
   'EQ',            # =
   'LT',            # <
   'LE',            # <=
   'GT',            # >
   'GE',            # >=
   'NE',            # !=
   'LPAREN',        # (
   'RPAREN',        # )
   'LBRAC',         # [
   'RBRAC',         # ]
   'LLAVEI',        # {
   'LLAVED',        # }
   'ENDPOINT',      # .(结束符)
   'DIGSEQ',        # 十进制整数(可以用来做label,即只允许label是'DIGSEQ')
   'GOTO',
   'DOTDOT',        # ..(为了支持数组)
]

# 保留字
reserved = {
    'program' : 'PROGRAM',
    'begin' : 'BEGIN',
    'end' : 'END',
    'var' : 'VAR',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'case' : 'CASE',
    'of' : 'OF',
    'while' : 'WHILE',
    'do' : 'DO',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'mod' : 'MOD',
    'array' : 'ARRAY',
    'boolean' : 'BOOLEAN',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'integer' : 'INTEGER',
    'real' : 'REAL',
    'char' : 'CHAR',
    'string' : 'STRING',
    'uses' : 'USES',
    'const' : 'CONST',
    # 'true' : 'TRUE',
    # 'false' : 'FALSE',
    'type' : 'TYPE',
    'for' : 'FOR',
    'to' : 'TO',
    'downto' : 'DOWNTO',
}

tokens = part_tokens + list(reserved.values())

# 如果想要向re.compile()方法提供flag，使用reflags选项：lex.lex(reflags=re.UNICODE)

# Regular expression rules for simple tokens
# 't_'后面的字符串必须和tokens中定义的一样，否则会报SyntaxError: Can't build lexer的错
t_PLUS       = r'\+'
t_MINUS      = r'\-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_ASSIGNMENT = r':='
t_SEMICOLON  = r'\;'
t_COLON      = r':'
t_COMMA      = r','
t_EQ         = r'\='
t_LT         = r'\<'
t_LE         = r'<='
t_GT         = r'\>'
t_GE         = r'>='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRAC      = r'\['
t_RBRAC      = r'\]'
t_LLAVEI     = r'{'
t_LLAVED     = r'}'
t_NE         = r'!='    # 和Pascal中的<>不同
t_ENDPOINT   = r'.'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r\x0c'

# 浮点数(实数) ——> 必须写到整数匹配规则的前面！
def t_REAL_NUMBER(t):
    # r'\d+\.\d+'
    r"[\+-](\d+\.\d+([eE][\+-]\d+)?)|(\d+[eE][\+-]\d+)"
    # t.lexer.float_count += 1
    t.value = float(t.value)
    t.endlexpos = t.lexpos + len(str(t.value))
    return t

# 整数
def t_INT_NUMBER(t):
    r'\d+'  # 如果需要执行动作的话，规则可以写成一个方法。如果使用方法的话，正则表达式写成方法的文档字符串。
    # t.lexer.integer_count += 1  # 统计整数出现的次数
    t.value = int(t.value)
    t.endlexpos = t.lexpos + len(str(t.value))
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.endlexpos = t.lexpos + len(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.lower() in reserved: # 识别保留字
        t.type = reserved[t.value.lower()]    # 前面如果有下划线，则表示是保留字，而不是普通的ID
    else:
        t.type = 'ID'    # Check for reserved words
    t.endlexpos = t.lexpos + len(t.value)
    return t

# 丢弃注释,可以用 t_ignore_COMMENT = r'...' 来代替
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*\n)'
    # r"(?s)(\(\*.*?\*\))|({[^}]*})"
    t.lexer.lineno += (t.value.count("\n"))
    t.endlexpos = t.lexpos + len(t.value)
    pass

# 识别字符(取决于特定的实现) 
# 只支持转义字符：'\t' '\n' and '\\'
def t_CHAR(t):
    r"(\'(([^\\\'])|(\\[\\tn]))\')"
    t.value = t.value[1:-1]
    t.endlexpos = t.lexpos + len(t.value)
    return t

# 识别字符串。允许在字符串中出现 paired \'
def t_STRING(t):
    r"(\'((\'(([^\\\'])|(\\[\\tn]))*\')|((([^\\\'])|(\\[\\tn]))*))*\')"
    escaped = False
    s = t.value[1:-1]   # 提取单引号中间的字符
    new_str = ''
    for i in range(0, len(s)):
        c = s[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = False
        else:
            if c == "\\":
                escaped = True
            else:
                new_str += c
    t.endlexpos = t.lexpos + len(t.value)
    t.value = new_str
    return t

# leading zeros are allowed.
def t_DIGSEQ(t):
    r'[0-9]+'
    t.endlexpos = t.lexpos + len(t.value)
    return t
    
# -------------------- todo ----------------------
def t_STARs(t):
    r"\*\*"
    t.endlexpos = t.lexpos + len(t.value)
    return t

def t_UPARROW(t):
    r"\^"
    t.endlexpos = t.lexpos + len(t.value)
    return t
# ------------------------------------------------

# =========================== array ==============================

def t_DOTDOT(t):
    r"\.\."
    t.endlexpos = t.lexpos + len(t.value)
    return t


# 定义记录行号的规则
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("非法字符: '%s'" % t.value[0])
    t.lexer.skip(1) # 跳过非法的字符

# 计算列号，为了指示上下文的错误位置，只在必要时有用。 
# input is the input text string, token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# 构建lexer
def lexer(debug = False):
    tab = 'lextab'  # 在当前目录生成lextab.py文件，这个文件会包含所有的正则表达式规则和词法分析阶段的分析表，然后，lextab.py可以被导入用来构建lexer。这种方法大大改善了词法分析程序的启动时间，而且可以在Python的优化模式下工作。
    mod = sys.modules[__name__]
    return lex.lex(debug = debug, debuglog = log, optimize = 0, lextab = tab, outputdir = os.path.dirname(__file__), module = mod)


if __name__ == '__main__':
    '''测试词法分析器'''
    sourceBasePath = '../SourceProg4Test/'
    sourceFileName = input('Please input the source Pascal file name: ')
    sourceP_path = sourceBasePath + sourceFileName

    with open(sourceP_path, 'r', encoding = 'utf-8') as sourceF:
        data = sourceF.read()
    print('=' * 40 + ' Source Program ' + '=' * 40)
    print(data)
    print('=' * 48 + '=' * 48)

    lexer = lexer()
    lexer.integer_count = 0
    lexer.float_count = 0

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok)

    print('+' * 44 + ' Tokens ' + '+' * 44)
    for tok in lexer:
        # print(tok)
        # lineno是token在源程序字符串中的行号，lexpos表示标记相对于输入串起始位置的偏移。
        print('(' + tok.type, tok.value, tok.lineno, tok.lexpos, end = ')\n')
    print('+' * 48 + '+' * 48)
