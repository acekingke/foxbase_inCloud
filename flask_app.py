# -*- coding: utf-8 -*-
"""
    Flaskapp for cloud foxbase
    ~~~~~~

   
"""

import json
import sys
from flask import Flask, request,  redirect, url_for, abort, \
     render_template


# create our little application :)
app = Flask(__name__)
from lex import lexer
from parse import parser
import fox_ast as ast
import err as myerr
import vistor


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


@capture
def out(source):    
    try:
        ast2 =  parser.parse(lexer.lex(source))
        vistor.exec_cmd_block(ast2)
        del ast2
    except myerr.ParserError as e:
        print >>sys.stderr , e.message 
    except Exception ,e:
        print >>sys.stderr, e
@app.route('/')
def index(): 
    return render_template('index.html', hy_version="v0.1", server_software='cloud foxbase')
@app.route('/eval', methods = ["POST"])
def evals():

    from fox_ast import data
    v = getattr(data, "symbols", None)
    if v is None:
        setattr(data, "symbols", {
        "global":dict(),
        "local":dict()
    })
    input = request.get_json() 
    for i in input["env"]:
        o,err = out(i)
    o,err = out(input["code"])
    return json.dumps({"stdout":o, "stderr":err})

@app.route('/test')
def test():
    from fox_ast import data
    v = getattr(data, "symbols", None)
    if v is None:
        setattr(data, "symbols", {
        "global":dict(),
        "local":dict()
    })
    source = open("a.prg", "r").read()
    o,err = out(source)
    o.replace('\n', "<br />")
    return render_template("content.html", title="test", lines=[o])

@app.route('/testform/<file_name>', methods=['POST', 'GET'])
def testform(file_name):
    print file_name
    from err import AcceptError
    if  request.method == 'GET':
        from fox_ast import data
        v = getattr(data, "symbols", None)
        if v is None:
            setattr(data, "symbols", {
            "global":dict(),
            "local":dict()
        })
        data.symbols["global"]["method"]  = "GET"
        f = open(file_name+".prg", "r")
        source = f.read()
        f.close()
        asks = dict()       
        try:
            o,err = out(source)
            #print "out:", o
            if o.startswith("ACCEPT:"):
                asks = eval(o[7:])  
            else:
                lines =[o]
                return render_template("content.html", title="testform", lines=[o])         
        except AcceptError,e:
            pass
        #print asks
        return render_template("form.html", file_name=file_name, title="testform", asks=asks)
    elif request.method == "POST":
        #print 'here'
        from fox_ast import data
        v = getattr(data, "symbols", None)
        if v is None:
            print 'in here'
            setattr(data, "symbols", {
            "global":dict(),
            "local":dict()
        })
        data.symbols["global"]["method"] = "POST"
        #print 'hyere', request.form["fname"]
        for i in  request.form.items():
            s = "%s=%s" %(i[0],i[1])
            o,err = out(s)
        f = open(file_name+".prg", "r")
        o,err = out(f.read())
        f.close()
        o.replace('\n', "<br />")
        return render_template("content.html", title="testform", lines=[o])
    else:
        return "zzzzzzz"
@app.route('/testform2/<file_name>', methods=['POST', 'GET'])
def show_user_profile(file_name):
    # show the user profile for that user
    return 'User %s' % file_name
if __name__ == '__main__':
    app.run(threaded=True)
    #app.run(debug=True)


