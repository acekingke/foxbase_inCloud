#-*_ coding:utf-8 -*-
__author__ = 'kyc'
from lex import lg
from rply import ParserGenerator
import fox_ast as ast
from err import  *

pg = ParserGenerator([i.name for i in lg.rules],
        precedence=[("right", ["OR"]),("right",["AND"]),("right",["NOT"]),
                    ("left",["GT","GE","LT","LE"]),
                    ("left", ['PLUS', 'MINUS']),("left",["MUL","DIV","MOD"]) ,
                    ("right",["UMINUS"]),("left",["POWER"])
        ], cache_id="myparser")

@pg.production("prog : block_cmd")
def main(p):
    return p[0]
@pg.production("block_cmd : cmd block_cmd")
def block_cmd_many(p):
    return ast.Box_cmd_block(p[0], p[1].cmd_list)
@pg.production("block_cmd : cmd ")
def block_cmd_one(p):
    return ast.Box_cmd_block(p[0], list())
@pg.production("cmd : expr")
@pg.production("cmd : assign_cmd")
@pg.production("cmd : print_cmd")
@pg.production("cmd : if_cmd")
@pg.production("cmd : docase_cmd")
@pg.production("cmd : do_while_cmd")
@pg.production("cmd : exit_cmd")
@pg.production("cmd : loop_cmd")
@pg.production("cmd : for_cmd")
@pg.production("cmd : do_cmd")
@pg.production("cmd : accept_cmd")
# for while docmd
def cmd(p):
    return p[0]
@pg.production("loop_cmd : LOOP")
@pg.production("exit_cmd : EXIT")
def loop_or_exit(p):
    if p[0].name == 'EXIT':
        return ast.Box_exit_cmd()
    elif p[0].name == 'LOOP':
        return ast.Box_loop_cmd()

@pg.production("expr : NUMBER")
@pg.production("expr : DATE")
@pg.production("expr : TrueValue")
@pg.production("expr : FalseValue")
@pg.production("expr : STRING")
@pg.production("expr : IDENTIFIER")
#func_cmd
@pg.production("expr : func_cmd")
def expression_number(p):
    if p[0].name == 'NUMBER':
        if "." in p[0].getstr():
            return ast.Box_expr(float(p[0].getstr()), "NUMBER", "FLOAT")
        else :
            return ast.Box_expr(int(p[0].getstr()), "NUMBER", "INT")
    elif p[0].name == "DATE":
        return ast.Box_expr(p[0].getstr(), "DATE")
    elif  p[0].name == "TrueValue" or p[0].name == 'FalseValue':
        return ast.Box_expr(p[0].getstr(), "LOGIC")
    elif p[0].name == "STRING":
        return ast.Box_expr(p[0].getstr(), "STRING")
    elif p[0].name == 'IDENTIFIER':
        return ast.get_variable(p[0].getstr())
    elif p[0].name == "FUNCTION":
        return p[0]
    else:
        raise ParserError("type error")

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
@pg.production("expr : expr DIV expr")
@pg.production("expr : expr MUL expr")
@pg.production("expr : expr MOD expr")
@pg.production("expr : expr POWER expr")
def expression_op(p):
    op = p[1].name
    left = p[0]
    right = p[2]
    return ast.Box_op(op, left, right)
#   负号处理
@pg.production("expr : MINUS  expr",precedence='UMINUS')
def expression_op2(p):
    op = "UMINUS"
    return ast.Box_op(op, p[1], None)
# relation  op
# contain
@pg.production("expr : expr GT expr")
@pg.production("expr : expr LT expr")
@pg.production("expr : expr LE expr")
@pg.production("expr : expr GE expr")
@pg.production("expr : expr CONTAIN expr")
@pg.production("expr : expr EQ expr")
@pg.production("expr : expr NE expr")
def expression_relation_op(p):
    op = p[1].name
    left = p[0]
    right = p[2]
    return ast.Box_relop( op, left, right)
# logic op
@pg.production("expr : expr AND expr")
@pg.production("expr : expr OR expr")
@pg.production("expr : NOT expr")
def expression_logic_op(p):
    if len(p) == 2: #is not
        op = p[0].name
        left = p[1]
        return ast.Box_logic_expr(op, left, None )
    else : # is and or
        op = p[1].name
        left = p[0]
        right = p[2]
        return ast.Box_logic_expr(op, left, right)

@pg.production("expr : LPAREN expr RPAREN")
def p_expression_group(p):
    return p[1]
# assign cmd
@pg.production("assign_cmd : IDENTIFIER EQU expr")
def assign_cmd(p):
    varname = p[0].getstr()
    r = None
    if not ast.get_variable(varname):
        r =  ast.new_variable(varname, "global")
    else:
        r =  ast.get_variable(varname)

    r.set_expr(p[2])
    return ast.Box_assign_cmd(r, p[2])
#  print cmd
@pg.production("print_cmd : QPUT expr")
def print_cmd(p):
    return ast.Box_print_cmd( p[1])

# if

@pg.production("if_cmd : IF expr    block_cmd   ENDIF")
def if_cmd1(p):
      return ast.Box_if_cmd(p[1], p[2], None)


@pg.production("if_cmd : IF expr    block_cmd ELSE block_cmd   ENDIF")
def if_cmd4(p):
     return ast.Box_if_cmd(p[1], p[2], p[4])
#todo: do cmd
@pg.production("do_cmd : DO FILE_NAME")
def do_cmd(p):
    return ast.Box_do_cmd(p[1].getstr())
@pg.production("docase_cmd : DO CASE case_list OTHERWISE block_cmd ENDCASE")
def docase_cmd(p):
    return  ast.Box_do_case(p[2], p[4])
@pg.production("docase_cmd : DO CASE case_list   ENDCASE")
def docase_cmd2(p):
    return  ast.Box_do_case(p[2],None)
@pg.production("case_list : CASE expr block_cmd ")
def case_list_one(p):
    return ast.Box_case_list((p[1], p[2]), [])
@pg.production("case_list : CASE expr block_cmd case_list")
def case_list_many(p):
    return ast.Box_case_list((p[1], p[2]), p[3].case_list)

#do while
#
#DO WHILE lExpression
#      Commands
#   [LOOP]
#   [EXIT]
# ENDDO
@pg.production("do_while_cmd : DO WHILE expr block_cmd ENDDO")
def do_while(p):
    return  ast.Box_while_cmd(p[2], p[3])
# for
#FOR VarName = nInitialValue TO nFinalValue [STEP nIncrement]
#      Commands
#   [EXIT]
#   [LOOP]
#ENDFOR | NEXT
@pg.production("for_cmd : FOR assign_cmd TO expr block_cmd ENDFOR")
@pg.production("for_cmd : FOR assign_cmd TO expr block_cmd NEXT")
@pg.production("for_cmd : FOR assign_cmd TO expr STEP expr block_cmd NEXT")
@pg.production("for_cmd : FOR assign_cmd TO expr STEP expr block_cmd ENDFOR")
def do_for_cmd(p):
    initval = p[1]
    finalval = p[3]
    cmd = None
    step = None
    if len(p) == 6:
         cmd = p[4]
    elif len(p) == 8:
        step = p[5]
        cmd = p[6]
    return ast.Box_for_cmd( initval, finalval, step, cmd)
#todo: procedure

# function
@pg.production("func_cmd : IDENTIFIER LPAREN arg_list RPAREN ")
def do_func_cmd(p):
    return ast.Box_func_cmd(p[0].getstr(), p[2])

@pg.production("arg_list : arg_list COMMA expr")
def arg_list(p):
    p[0].add(p[2])
    return p[0]
@pg.production("arg_list : expr")
@pg.production("arg_list : none")
def arg_list_none(p):
    #return []
    return  ast.Box_arg_list(p[0] and [p[0]])
#FUNCTION FunctionName
#   [ LPARAMETERS parameter1 [ ,parameter2 ] , ... ]
#      Commands
#  [ RETURN [ eExpression ] ]
#[ENDFUNC]
@pg.production("accept_cmd : ACCEPT  accept_item accept_lst")
def accept_cmd(p):
    return ast.Box_accept_cmd(p[1], p[2])

@pg.production("accept_lst :  COMMA  accept_item accept_lst")
@pg.production("accept_lst : none")
def accept_lst(p):
    if len(p) == 1:
       return ast.Box_accept_item_list(None, [])
    else:
       return  ast.Box_accept_item_list(p[1], p[2].item_list)
@pg.production("accept_item : STRING TO IDENTIFIER")
def accept_item(p):
    return ast.Box_accept_item(p[0].getstr(), p[2].getstr())
# just for "none"
@pg.production("none : ")
def do_none(p):
    return None
@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected, at line %d, col %d" % (token.gettokentype(),token.source_pos.lineno, token.source_pos.colno))
parser = pg.build()