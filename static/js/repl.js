$(document).ready(function(){
  var backlog = [];
  var multiline = "";
  var is_mul = false;
  var console1 = $('#fox-console').console({
    promptLabel: '=> ',
    commandValidate:function(line){
      if (line == '') return false;
      else return true;
    },
    commandHandle:function(line, report){
      if (line=='clear'){
        
        console1.reset();
        backlog = []
      }
      else if (line[line.length-1] == '\\')
      {
        multiline = multiline +  line.slice(0, line.length-1) + "\n";
        report([{msg:line}]);
        is_mul = true;
      }
      else 
      {
        
     
        multiline = multiline + line;
        if (is_mul) {
          is_mul = false;
          report([{msg:multiline}]);
        };
        $.ajax({
          type: 'POST',
          url: '/eval',
          data: JSON.stringify({code: multiline, env: backlog}),
          contentType: 'application/json',
          dataType: 'json',
          success: function(data) {
            report([{msg : data.stdout, className:'jquery-console-message-value'},
                    {msg : data.stderr, className:'jquery-console-message-error'}]);
          }
        });
        backlog.push(multiline);
        multiline=""
      }
  
    },
    animateScroll:true,
    promptHistory:true,
    autofocus:true,
    welcomeMessage: 'foxbase in cloud ({hy_version}) [{server_software}]'.supplant({
      hy_version: hy_version,
      server_software: server_software
    })
  });
  console1.promptText('? "hello world"');
});


if (!String.prototype.supplant) {
    String.prototype.supplant = function (o) {
        return this.replace(
            /\{([^{}]*)\}/g,
            function (a, b) {
                var r = o[b];
                return typeof r === 'string' || typeof r === 'number' ? r : a;
            }
        );
    };
}
