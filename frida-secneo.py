#coding:utf-8

import frida
import sys

jscode="""
if(Java.available) {
	Java.perform(function(){
		var application = Java.use("android.app.Application");
		var Toast = Java.use('android.widget.Toast');
		application.attach.overload('android.content.Context').implementation = function(context) {
			var result = this.attach(context); 
			var classloader = context.getClassLoader(); 
			Java.classFactory.loader = classloader;
			var AyWelcome = Java.classFactory.use("flytv.run.monitor.fragment.user.AyWelcome"); 
			console.log("AyWelcome: " + AyWelcome);
			
			AyWelcome.onCreate.overload('android.os.Bundle').implementation = function(bundle) {
				var ret = this.onCreate(bundle);
				Toast.makeText(context, "onCreate called", 1).show(); //弹出Toast
				return ret;
			}
			return result;
		}
	});
}

"""

package_name="com.citicbank.comb"
def on_message(message,data):
    print message

session=frida.get_device_manager().enumerate_devices()[-1].attach(7688)
script=session.create_script(jscode)
script.on("message",on_message)
script.load()
sys.stdin.read()