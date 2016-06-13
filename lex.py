# -*- coding:utf-8 -*-
from rply import  LexerGenerator
from rply.token import BaseBox
lg = LexerGenerator()
# Add takes a rule name, and a regular expression that defines the rule.
#lg.add("COMMENT", r"\s*\*[^\n]*")
#  ([0-9]+)|([0-9]*\.[0-9]+)|(0x[0-9A-Fa-f]+)
lg.add("DATE", r"0d[0-9]{8}")
lg.add("NUMBER", r"(0x[0-9A-Fa-f]+)|([0-9]*\.[0-9]+)|([0-9]+)")
#if
lg.add("IF",r"if|IF")
#lg.add("THEN",r"then|THEN")
lg.add("ELSE",r"ELSE|else")
lg.add("ELSEIF","ELSEIF|elseif")
lg.add("ENDIF","endif|ENDIF")
# do
lg.add("DO", "do|DO")
# do while
lg.add("WHILE",r"while|WHILE")
# end do
lg.add("ENDDO",r"ENDDO|enddo")
# do case
lg.add("CASE",r"case|CASE")
lg.add("ENDCASE", r"ENDCASE|endcase")
# otherwise
lg.add("OTHERWISE",r"otherwise|OTHERWISE")
# exit
lg.add("EXIT",r"exit|EXIT")
# for, for each
lg.add("FOR",r"for|FOR")
lg.add("TO", r"to|TO")
lg.add("STEP", r"STEP|step")
lg.add("EACH",r"each|EACH")
lg.add("ENDFOR",r"ENDFOR|endfor")
lg.add("NEXT",r"NEXT|next")
lg.add("ACCEPT",r"ACCEPT|accept")
lg.add("TO", r"TO|to")
# LOGIC
lg.add("AND",r"and|AND")
lg.add("NOT",r"NOT|not|!")
lg.add("OR", r"OR|or")
#loop
lg.add("LOOP",r"loop|LOOP")
lg.add("FILE_NAME", r"[_a-zA-Z0-9]+(\.prg|\.PRG)")
lg.add("IDENTIFIER", r"(([_a-zA-Z][_a-zA-Z0-9]+)|([a-zA-Z]))")
lg.add("TrueValue", r"\.t\.|\.T\.")
lg.add("FalseValue", r"\.f\.|\.F\.")
# STRING
lg.add('STRING',r"(\x27[^\x27\n]*\x27)|(\x22[^\x22\n]*\x22)|(\[[^\]]*\])")
# operator
#   1. relation
# not equal
lg.add('NE', r"#|!=|<>")
#eq
lg.add('EQ', r"==")
#ge
lg.add('GE', r">=")
#le
lg.add("LE", r"<=")
#gt
lg.add("GT", r">")
#lt
lg.add("LT", r"<")
#contain
lg.add("CONTAIN", r"\$")
# add sub
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
# expo
lg.add("POWER",r"\^")
# mul div
lg.add("MUL", r"\*")
lg.add("DIV", r"/")
lg.add("MOD",r"%")
# ()
lg.add("LPAREN",r"\(")
lg.add("RPAREN",r"\)")

#other = ?
lg.add("EQU",r"=")
# question put print
lg.add("QPUT",r"\?")
lg.add("DOT",r"\.")
lg.add("COMMA",r",")
lg.add("MICRO", r"&")
# function
#procedure
lg.ignore(r"\s+")
lg.ignore( r"\s*\*[^\n]*")
lg.ignore( r"&&[^\n]*")
lexer = lg.build()
if __name__=='__main__':
    print [i.name for i in lg.rules]
    for i in lexer.lex("12.2+0x12f+0.2+12if+ 'IF' \"HELLO\" <> # != ** ^ ! if ass"):
        print i
    for i in lexer.lex("[z]"):
        print i