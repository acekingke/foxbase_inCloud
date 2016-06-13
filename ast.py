# -*- coding:utf-8 -*-
from rply.token import BaseBox
from err import *
from threading import local
data = local()

setattr(data, "symbols", {
    "global":dict(),
    "local":dict()
})

class Box_expr(BaseBox):
    def __init__(self, val, type,subtype =None):
        self.type = type
        self.subtype= subtype
        if type == "NUMBER":
            self.val = val
        elif type == "DATE":
            self.val = {"YEAR":val[2:6],"MONTH":val[6:8],"DAY":val[8:10]}
        elif type == "STRING":
            self.val=val[1:-1]
        else:
            self.val = val
    def __str__(self):
        if self.type == "NUMBER":
            return  "(Box_expr: %s %s %f)"%(self.type, self.subtype, self.val)
        elif self.type == "DATE":
            return "(Box_expr : type %s %s)"%(self.type, self.val)
        elif self.type == "STRING":
            return "(Box_expr : type %s %s)"%(self.type, self.val)
        else:
            return "(Box_expr : type %s %s)"%(self.type, self.val)
# variable
def   get_variable(name):
    if name in data.symbols['local'].keys():
        return data.symbols['local'][name]
    elif name in data.symbols['global'].keys():
        return data.symbols['global'][name]
    else:
        return None

def new_variable(name, mode):
    vari = Box_variable(name)
    data.symbols[mode][name] = vari
    return vari
#  make assgin to
class Box_assign_cmd(BaseBox):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    def __str__(self):
        return "(assign %s with %s)" % (self.var, self.expr)
class Box_variable(Box_expr):
    def __init__(self, name):
        super(Box_variable, self).__init__(None, None,None)
        self.type = None
        self.name = name
    def set_expr(self, expr):
        self.type = expr.type
        self.expr = expr
    def __str__(self):
        return " (variable type %s %s) " % (self.type,self.name)
class Box_op(Box_expr):
    def __init__(self, op, left, right):
        super(Box_op, self).__init__(None, None,None)
        self.op = op
        self.left = left
        self.right = right
        # PLUS
        # number +/- number
        # date +/- number
        # string +/ string
        if op == 'PLUS':
            if left.type == "DATE" :
                if right.type == "NUMBER":
                    self.type = "DATE"
                else :
                    raise ParserError("Cannot add DATE to other type")
            elif left.type == "NUMBER":

                if right and right.type == "NUMBER":
                    self.type = "NUMBER"
                else :
                    raise ParserError("Cannot add number to other type")
            elif left.type == "STRING":
                if right.type == "STRING":
                    self.type = "STRING"
                else :
                    raise ParserError("Cannot add number to other type")
            else:
                raise ParserError("invalid type can make plus")
        elif op =="MINUS":
            if left.type == "DATE" :
                if right.type == "NUMBER":
                    self.type = "DATE"
                elif right.type == "DATE":
                    self.type = "NUMBER"
                else :
                    raise ParserError("Cannot minus DATE to other type")
            elif left.type == "NUMBER":
                if right.type == "NUMBER":
                    self.type = "NUMBER"
                else :
                    raise ParserError("Cannot minus number to other type")
            else:
                raise ParserError("invalid type can make MINUS")
        # MUL
        elif op =="MUL":
            if left.type == "NUMBER" and right.type == "NUMBER":
                self.type = "NUMBER"
            else :
                raise ParserError("cannot mul in error type")
        elif op =="DIV":
            if left.type == "NUMBER" and right.type == "NUMBER":
                self.type = "NUMBER"
            else :
                raise ParserError("cannot mul in error type")
        elif op == "MOD":
            if left.type == "NUMBER" and right.type == "NUMBER":
                self.type = "NUMBER"
            else :
                raise ParserError("cannot mul in error type")
        elif op =="POWER":
            if left.type == "NUMBER" and right.type == "NUMBER":
                self.type = "NUMBER"
            else :
                raise ParserError("cannot mul in error type")
        elif op =="UMINUS":
            self.type = "NUMBER"
            if left.type != "NUMBER":
                raise ParserError("just number can  uminus ")
        else:
            raise ParserError("UNKNOWN op ")
    def __str__(self):
        return "Base_op, op: %s (left: %s) (right: %s)"%(self.op, self.left, self.right)
class Box_relop(Box_expr):
    def __init__(self,  op, left, right):
        super(Box_relop, self).__init__(None, "LOGIC", None)
        self.op = op
        self.left = left
        self.right = right
        if left.type != right.type :
            raise ParserError("left type and right type must same")
    def __str__(self):
        return "(relation op:%s,left:%s, right:%s)"%(self.op, self.left, self.right)
#  print_cmd
class Box_print_cmd(BaseBox):
    def __init__(self, expr):
        self.name = "QPUT"
        self.expr = expr
    def __str__(self):
        return "(print %s )"%self.expr
class  Box_if_cmd(BaseBox):
    def __init__(self, expr, cmd_if, cmd_else):
        if expr.type == "LOGIC":
            self.expr = expr
            self.cmd_if = cmd_if
            self.cmd_else = cmd_else
        else:
            raise ParserError("expr must be logic in if cmd")
    def __str__(self):
        return "(if_cmd expr: %s if_cmd:%s, else_cmd:%s)" %(self.expr, self.cmd_if, (self.cmd_else and  self.cmd_else or "None"))

class Box_cmd_block(BaseBox):
    def __init__(self, cmd, cmd_list):
        self.cmd_list = []
        self.cmd_list.append(cmd)
        self.cmd_list =  self.cmd_list + cmd_list
    def __str__(self):
        s = ""
        for i in self.cmd_list:
            s = s + i.__str__()
            #print i
        return "(cmd_block : %s)"%(s)
#   case list
class Box_case_list(BaseBox):
    def __init__(self,case_tuple, cas_list):
        self.case_list = []
        self.case_list.append(case_tuple)
        self.case_list = self.case_list + cas_list
    def __str__(self):
        s = ""
        for i in self.case_list:
            s = s + "(expr:"+  i[0].__str__() +",cmd:" + i[1].__str__() +"),"
            #print i
        return "(Box_case_list : %s)"%(s)
#  docase
class Box_do_case(BaseBox):
    def __init__(self, case_lst, otherwise):
        self.case_list = case_lst
        self.otherwise = otherwise

    def __str__(self):
        return "(box docase case_list:%s, otherwise : %s)"%(self.case_list, (self.otherwise and self.otherwise or "None"))
class Box_exit_cmd(BaseBox):
    def __init__(self):
        pass
    def __str__(self):
        return "(EXIT cmd)"
class Box_loop_cmd(BaseBox):
    def __init__(self):
        pass
    def __str__(self):
        return "(LOOP cmd)"
class Box_while_cmd(BaseBox):
    def __init__(self, expr, cmd):
        self.expr = expr
        self.cmd_block = cmd
    def __str__(self):
        return "(while expr: %s cmd %s)"%(self.expr, self.cmd_block)
class Box_for_cmd(BaseBox):
    def __init__(self,  initval, finalval, stepval, cmd):
        self.initval = initval
        self.finalval = finalval
        self.stepval = stepval
        self.cmd = cmd
    def __str__(self):
        return "(for_cmd  init %s, final %s, stepval %s, cmd %s )"%( self.initval,
                            self.finalval, self.stepval, self.cmd)

class Box_arg_list(BaseBox):
    def __init__(self, arglist):
        self.arglist =    arglist or []
    def add(self, arg):
        if arg:
            self.arglist.append(arg)
    def __str__(self):
        return "(expr_list %s ) "

class Box_logic_expr(Box_expr):
    def __init__(self, op , expr1, expr2):
        super(Box_logic_expr, self).__init__(None, "LOGIC",None)
        self.op = op
        self.left = expr1
        self.right = None
        if op == "NOT":
            if expr1 and expr1.type == "LOGIC" :
                pass
            else:
                raise  ParserError("Must be logic type")
        else:
            self.right = expr2
    def __str__(self):
        return "(logic expr op %s, left: %s, right: %s)" %(self.op, self.left, self.right or "None")

class Box_func_cmd(Box_expr):
    def __init__(self, funname, arglist):
        super(Box_func_cmd,self).__init__(None, None,None)
        self.func_name = funname.upper()
        self.name = "FUNCTION"
        self.args = arglist
        fn_tab = {
            # FUN_NAME (para len, fun)
            "VAL": [(1,lambda x:float(x), "NUMBER"),],
            "STR": [(1, lambda x:str(x), "STRING"),],
            "LEN":[(1, lambda x : len(x), "NUMBER"),],
            "INT":[(1, lambda x : int(x), "NUMBER"),],
            "TRIM":[(1, lambda  x : x.strip(' '), "STRING"),],
            "SUBSTR":[(3, lambda x, y, z: x[y:z], "STRING"), (2, lambda x, y: x[y:],"STRING")],
            "LOWER":[(1, lambda  x:x.lower(), "STRING")],
            "UPPER":[(1, lambda  x:x.upper(), "STRING")],
        }
        for i in fn_tab[self.func_name]:
    	    if i[0] == len(arglist.arglist):
               self.par_len, self.f, self.type = i

    def __str__(self):
        s = ""
        for i in self.args.arglist:
            s = s + i.__str__()
        return "func_cmd: %s :arglist : %s " % (self.func_name,s)
class Box_do_cmd(BaseBox):
    def __init__(self, file_name):
        self.file_name=file_name
class Box_accept_cmd(BaseBox):
    def __init__(self,acc,  acc_lst):
        self.accept_list = acc_lst
        l = [acc] + acc_lst.item_list
        self.accept_list.item_list = l
    def __str__(self):
        return "(ACCEPT CMD %s)" % self.accept_list
class Box_accept_item(BaseBox):
    def __init__(self, prompt, varname):
       self.prompt = prompt[1:-1] # È¥µô¡° ¡® ºÍ [ ,]·ûºÅ
       self.varname = varname
    def __str__(self):
        return "(ACCEPT Item %s, %s )" %(self.prompt, self.varname)
class Box_accept_item_list(BaseBox):
    def __init__(self, item, ls):
       self.item_list = []
       if item:
          self.item_list.append(item)
       self.item_list = self.item_list + ls
       pass
    def __str__(self):
        s=""
        for i in self.item_list:
            s = s+ i.__str__() + ","
        return "(ACCEPT Item list %s )" %s

def check_method():
    if "method" in  data.symbols["global"]:
        return data.symbols["global"]["method"]
    else:
        return None