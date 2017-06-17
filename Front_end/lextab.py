# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('SEMICOLON', 'EQ', 'LT', 'GT', 'PROGRAM', 'INT_NUMBER', 'GE', 'BEGIN', 'DO', 'CHAR', 'OF', 'RETURN', 'FLOAT_NUMBER', 'VAR', 'STRING', 'TIMES', 'ELSE', 'INTEGER', 'LPAREN', 'DIF', 'CASE', 'DIVIDE', 'NOT', 'IF', 'ASSIGNMENT', 'LBRAC', 'COMMA', 'MINUS', 'END', 'LLAVEI', 'WHILE', 'ARRAY', 'FUNCTION', 'LLAVED', 'USES', 'OR', 'COLON', 'BOOLEAN', 'ID', 'ENDPOINT', 'LE', 'CONST', 'AND', 'PLUS', 'RPAREN', 'RBRAC', 'MOD', 'THEN'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [("(?P<t_FLOAT_NUMBER>\\d+\\.\\d+)|(?P<t_INT_NUMBER>\\d+)|(?P<t_BOOLEAN>true|false)|(?P<t_EQ>=)|(?P<t_ID>[a-zA-Z_][a-zA-Z_0-9]*)|(?P<t_COMMENT>(/\\*(.|\\n)*?\\*/)|(//.*\\n))|(?P<t_CHAR>^'p'$)|(?P<t_STRING>(\\'((\\'(([^\\\\\\'])|(\\\\[\\\\tn]))*\\')|((([^\\\\\\'])|(\\\\[\\\\tn]))*))*\\'))|(?P<t_STARs>\\*)|(?P<t_UPARROW>\\^)|(?P<t_newline>\\n+)|(?P<t_GE>\\>\\=)|(?P<t_LE>\\<\\=)|(?P<t_ASSIGNMENT>:=)|(?P<t_DIF>!=)|(?P<t_GT>\\>)|(?P<t_LBRAC>\\[)|(?P<t_LPAREN>\\()|(?P<t_LT>\\<)|(?P<t_PLUS>\\+)|(?P<t_RBRAC>\\])|(?P<t_RPAREN>\\))|(?P<t_TIMES>\\*)|(?P<t_COLON>:)|(?P<t_COMMA>,)|(?P<t_DIVIDE>/)|(?P<t_LLAVED>})|(?P<t_LLAVEI>{)|(?P<t_MINUS>-)|(?P<t_SEMICOLON>;)", [None, ('t_FLOAT_NUMBER', 'FLOAT_NUMBER'), ('t_INT_NUMBER', 'INT_NUMBER'), ('t_BOOLEAN', 'BOOLEAN'), ('t_EQ', 'EQ'), ('t_ID', 'ID'), ('t_COMMENT', 'COMMENT'), None, None, None, ('t_CHAR', 'CHAR'), ('t_STRING', 'STRING'), None, None, None, None, None, None, None, None, None, None, ('t_STARs', 'STARs'), ('t_UPARROW', 'UPARROW'), ('t_newline', 'newline'), (None, 'GE'), (None, 'LE'), (None, 'ASSIGNMENT'), (None, 'DIF'), (None, 'GT'), (None, 'LBRAC'), (None, 'LPAREN'), (None, 'LT'), (None, 'PLUS'), (None, 'RBRAC'), (None, 'RPAREN'), (None, 'TIMES'), (None, 'COLON'), (None, 'COMMA'), (None, 'DIVIDE'), (None, 'LLAVED'), (None, 'LLAVEI'), (None, 'MINUS'), (None, 'SEMICOLON')])]}
_lexstateignore = {'INITIAL': ' \t\r\x0c'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}