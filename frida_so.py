import frida
import sys
js_code="""
    Java.perform(function(){
    var securityCheck ="";
    var exports = Module.enumerateExports("libnative-lib.so");
    for(var i=0;i<exports.length;i++){
        //console.log("the method name is:"+exports[i].name);
        var methodname=exports[i].name;
        if(methodname.indexOf("getvalue")!=-1){
            console.log("the method name is:"+methodname);
            securityCheck=exports[i].address;
            break;
        }
    }
    
    Interceptor.attach(securityCheck,{
        onEnter: function(args){ 
        console.log("the args is:"+Memory.readCString(args[0])+"1:"+args[1]+",2:"+args[2]);
        Memory.writeUtf8String(args[0],"wocao");
        
        
        
    },
    onLeave: function (retval){
        console.log("the res is:"+Memory.readCString(retval));
       // Memory.writeUtf8String(retval,"wocao");
        var str="wocaowocaowaoowaooaoaoaoaooa";
        var bytes=stringToByte(str);
        //Memory.writeByteArray(retval,bytes);
    }
    });
    
});

function stringToByte(str) {
			var bytes = new Array();
			var len, c;
			len = str.length;
			for(var i = 0; i < len; i++) {
				c = str.charCodeAt(i);
				if(c >= 0x010000 && c <= 0x10FFFF) {
					bytes.push(((c >> 18) & 0x07) | 0xF0);
					bytes.push(((c >> 12) & 0x3F) | 0x80);
					bytes.push(((c >> 6) & 0x3F) | 0x80);
					bytes.push((c & 0x3F) | 0x80);
				} else if(c >= 0x000800 && c <= 0x00FFFF) {
					bytes.push(((c >> 12) & 0x0F) | 0xE0);
					bytes.push(((c >> 6) & 0x3F) | 0x80);
					bytes.push((c & 0x3F) | 0x80);
				} else if(c >= 0x000080 && c <= 0x0007FF) {
					bytes.push(((c >> 6) & 0x1F) | 0xC0);
					bytes.push((c & 0x3F) | 0x80);
				} else {
					bytes.push(c & 0xFF);
				}
			}
			return bytes;
		}
		
function byteToString(arr) {
			if(typeof arr === 'string') {
				return arr;
			}
			var str = '',
				_arr = arr;
			for(var i = 0; i < _arr.length; i++) {
				var one = _arr[i].toString(2),
					v = one.match(/^1+?(?=0)/);
				if(v && one.length == 8) {
					var bytesLength = v[0].length;
					var store = _arr[i].toString(2).slice(7 - bytesLength);
					for(var st = 1; st < bytesLength; st++) {
						store += _arr[st + i].toString(2).slice(2);
					}
					str += String.fromCharCode(parseInt(store, 2));
					i += bytesLength - 1;
				} else {
					str += String.fromCharCode(_arr[i]);
				}
			}
			return str;
		}
"""

package_name="com.example.frida_hook"
def on_message(message,data):
    print message

session=frida.get_device_manager().enumerate_devices()[-1].attach(package_name)
script=session.create_script(js_code)
script.on("message",on_message)
script.load()
sys.stdin.read()