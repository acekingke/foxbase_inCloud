# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import json
import sys
from flask import Flask, request,  redirect, url_for, abort, g, current_app,\
     render_template
from lex import lexer
from parse import parser
import ast
import vistor
import code

# create our little application :)
app = Flask(__name__)

id = 1
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def capture(f):
    """
    Decorator to capture standard output
    """
    def captured(*args, **kwargs):        
        from cStringIO import StringIO
        # setup the environment
        backup = sys.stdout
        backup2 = sys.stderr
        try:
            sys.stdout = StringIO()     # capture output
            sys.stderr = StringIO()
            f(*args, **kwargs)
            out = sys.stdout.getvalue() # release output
            err = sys.stderr.getvalue()
        finally:
            sys.stdout.close()  # close the stream 
            sys.stderr.close()
            sys.stdout = backup # restore original stdout
            sys.stderr = backup2
        return out,err # captured output wrapped in a string
    return captured

class repl(code.InteractiveConsole):
    def __init__(self,  locals=None, filename="<input>"):
        code.InteractiveConsole.__init__(self, locals=locals,
                                         filename=filename)
    def runsource(self, source, filename="<input>", symbol="single"):
    	ast =  parser.parse(lexer.lex(source))
        vistor.exec_cmd_block(ast)
        #exec source
@capture
def out(s):    
    try:
       r = repl(locals=locals)
       r.runsource(source=s)
    except Exception ,err:
        print >>sys.stderr , err

@app.route('/')
def index(): 
    return render_template('index.html', hy_version="v0.1", server_software='cloud foxbase')
@app.route('/eval', methods = ["POST"])
def evals():
    input = request.get_json() 
    o,err = out(input["code"])
    return json.dumps({"stdout":o, "stderr":err})


if __name__ == '__main__':
    app.run()
