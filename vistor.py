# -*- coding:utf-8 -*-
__author__ = 'kyc'
import datetime
from fox_ast import *
from err import *
def wrap_fun(func):
    def _warp(cmd):
        print "Now execute %s" % (cmd)
        func(cmd)
    return _warp

def exec_cmd_block(cmd_bolck):
    cmd_list = cmd_bolck.cmd_list
    rt = None
    for i in cmd_list:
        rt = exec_cmd(i)
        if rt in ("EXIT", "LOOP"):
            break
    return rt
def exec_cmd(cmd):
    rt = None
    if not cmd:
        return None
    cmd_type_name = cmd.__class__.__name__
    cmd_type_name = cmd_type_name.replace("Box","exec")+"(cmd)"
    rt = eval(cmd_type_name)
    return rt
def exec_variable(cmd):
    pass
def exec_loop_cmd(cmd):
    return "LOOP"
def exec_exit_cmd(cmd):
    return "EXIT"
def exec_expr(expr):
    pass
def exec_assign_cmd(assgin):
    var = assgin.var
    exec_cmd(assgin.expr)
    var.val = assgin.expr.val
    pass
def exec_print_cmd(print_cmd):
    exec_cmd(print_cmd.expr)
    print print_cmd.expr.val
def exec_op(cmd):
    op = cmd.op
    left = cmd.left
    right = cmd.right
    exec_cmd(left)
    exec_cmd(right)
    #Plus
    if op == "PLUS":
        # DATE + NUMBER
        if left.type =="DATE" and right.type == "NUMBER":
            year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
            val = datetime.date(year, month,day) + datetime.timedelta(days=right.val)
            year ,month, day = (str(i) for i in (val.year, val.month, val.day))
            cmd.val = {"YEAR": year, "MONTH":month, "DAY":day}
        # NUMBER + NUMBER
        elif left.type == "NUMBER" and right.type == "NUMBER":
            cmd.val = left.val + right.val
        # STRING + STRING
        elif left.type == "STRING" and right.type == "STRING":
            cmd.val = left.val + right.val
        else:
            raise ParserError("EXEC error:exec type not match")
    #  Minus
    elif op =="MINUS":
        # DATE-DATE DATE-NUMBER
        if left.type == "DATE" and right.type == "DATE":
            year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
            year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
            delta    = datetime.datetime(year,month,day) -  datetime.datetime(year2, month2, day2)
            cmd.val = delta.days
        elif left.type == "DATE" and right.type == "NUMBER":
            year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
            val = datetime.date(year, month,day) - datetime.timedelta(days=right.val)
            year ,month, day = (str(i) for i in (val.year, val.month, val.day))
            cmd.val = {"YEAR": year, "MONTH":month, "DAY":day}
        # NUMBER - NUMBER
        elif left.type == "NUMBER" and right.type == "NUMBER":
            cmd.val = left.val - right.val
        else:
            raise ParserError("EXEC error:exec type not match")
    #  MUL DIV MOD
    elif op == "MUL":
        cmd.val = left.val * right.val
    elif op == "DIV":
        cmd.val = left.val / float(right.val)
    elif op == "MOD":
        cmd.val = left.val % right.val
    #  POWER
    elif op == "POWER":
        cmd.val = left.val**(right.val)
    #  uminus
    elif op == "UMINUS":
        cmd.val = -(left.val)
# relation op
# GT
def cmp_gt_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) > datetime.date(year2, month2,day2)

def cmp_gt_number(left, right):
    return left.val > right.val
def cmp_gt_string(left, right):
    return left.val > right.val
def cmp_gt_logic(left, right):
    return left > right
# LT
def cmp_lt_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) < datetime.date(year2, month2,day2)

def cmp_lt_number(left, right):
    return left.val < right.val
def cmp_lt_string(left, right):
    return left.val < right.val
def cmp_lt_logic(left, right):
    return left < right


# LE
def cmp_le_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) <= datetime.date(year2, month2,day2)

def cmp_le_number(left, right):
    return left.val <= right.val
def cmp_le_string(left, right):
    return left.val <= right.val
def cmp_le_logic(left, right):
    return left <= right

# GE
def cmp_ge_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) >= datetime.date(year2, month2,day2)

def cmp_ge_number(left, right):
    return left.val >= right.val
def cmp_ge_string(left, right):
    return left.val >= right.val
def cmp_ge_logic(left, right):
    return left >= right

# EQ
def cmp_eq_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) == datetime.date(year2, month2,day2)

def cmp_eq_number(left, right):
    return left.val == right.val
def cmp_eq_string(left, right):
    return left.val == right.val
def cmp_eq_logic(left, right):
    return left == right
# NE
def cmp_ne_date(left, right):
    year,month, day = int(left.val["YEAR"]), int(left.val["MONTH"]),int(left.val["DAY"])
    year2,month2, day2 = int(right.val["YEAR"]), int(right.val["MONTH"]),int(right.val["DAY"])
    return datetime.date(year,month,day) != datetime.date(year2, month2,day2)

def cmp_ne_number(left, right):
    return left.val != right.val
def cmp_ne_string(left, right):
    return left.val != right.val
def cmp_ne_logic(left, right):
    return left != right


def exec_relop(cmd):
    op = cmd.op
    exec_expr(cmd.left)
    exec_expr(cmd.right)
    left = cmd.left
    right = cmd.right
    type = left.type
    eval_cmd = "cmp_"+op.lower()+"_"+type.lower()+"(left, right)"
    if type == "LOGIC":
        left = left.val.upper() == '.T.' and True or False
        right = right.val.upper() == '.T.' and True or False
    if op == "CONTAIN":
        cmd.val = (left.val in right.val) and ".T." or ".F."
    else :
        cmd.val = eval(eval_cmd) and ".T." or ".F."

def exec_logic_expr(cmd):
    op = cmd.op
    exec_cmd(cmd.left)
    exec_cmd(cmd.right)
    left = cmd.left
    right = cmd.right
    if op == "NOT":
        val = left.val.upper() == '.T.'
        cmd.val =( not val) and '.T.' or '.F.'
    elif op == "AND":
        val_left = left.val.upper() == '.T.'
        val_right = right.val.upper() == '.T.'
        cmd.val = (val_left and val_right) and '.T.' or '.F.'
    elif op == "OR":
        val_left = left.val.upper() == '.T.'
        val_right = right.val.upper() == '.T.'
        cmd.val = (val_left or val_right) and '.T.' or '.F.'
def  exec_if_cmd(cmd):
    exec_cmd(cmd.expr)
    rt = None
    if cmd.expr.val == ".T.":
        rt = exec_cmd_block(cmd.cmd_if)
        pass
    elif cmd.cmd_else and cmd.expr.val == ".F.":
        rt =  exec_cmd_block(cmd.cmd_else)
    return rt
def exec_do_case(cmd):
    case_list = cmd.case_list.case_list
    otherwise = cmd.otherwise
    rt = None
    for case in case_list:
        expr, cmd_block  = case
        exec_cmd(expr)
        if expr.val =='.T.':
            rt = exec_cmd_block(cmd_block)
            return rt
    rt = exec_cmd_block(otherwise)
    return  rt
#  for while function
#  need support loop and exit
def exec_for_cmd(cmd):
    exec_cmd(cmd.initval )
    exec_cmd(cmd.finalval )
    exec_cmd(cmd.stepval  )
    initval = cmd.initval
    finalval = cmd.finalval
    stepval  = (cmd.stepval and cmd.stepval.val) or 1
    cmd_block      = cmd.cmd
    while initval.var.val <= finalval.val:
        rt = exec_cmd_block(cmd_block)
        if rt == "EXIT":
            break
        initval.var.val = initval.var.val + stepval

#  need support loop and exit
def exec_while_cmd(cmd):
    expr      = cmd.expr
    cmd_block =    cmd.cmd_block
    exec_cmd(expr)
    while expr.val == '.T.':
        rt = exec_cmd_block(cmd_block)
        if rt == "EXIT":
            break

def exec_func_cmd(cmd):
    func_name = cmd.func_name
    args = cmd.args.arglist
    _arg = []
    for i in args[:cmd.par_len]:
        exec_cmd(i)
        _arg.append(i.val)
    cmd.val = cmd.f(*_arg)
def  exec_do_cmd(cmd):
    file_name = cmd.file_name
    from lex import lexer
    from parse import parser
    source = open("./" + file_name).read()
    ast =  parser.parse(lexer.lex(source))
    exec_cmd_block(ast)
def exec_accept_cmd(cmd):
    if check_method() and check_method() == "GET":
        item_list = cmd.accept_list.item_list
        print "ACCEPT:[",
        for item in item_list:
            prompt, varname = item.prompt, item.varname
            print "{'prompt':'"+prompt+"', 'valname':'"+varname+"'},",
            #print
        print "]"
        raise AcceptError
    elif check_method() and check_method() == "POST":
        # set value to symbol
        pass
    else:
        print "heare", check_method()

