# coding=utf-8
'''
ABPlayerHTML5_Py_Mac 2.000.06
Based on ABPlayerHTML5
MIT licence
Beining@ACICFG
cnbeining[at]gmail.com
'''
import thread
import random
import os
import getpass
import sys
import webbrowser
from multiprocessing import Process
import urllib
import threading
import shutil


reload(sys)
sys.setdefaultencoding('utf-8')
#try to fix the damn code problem

port = str(random.randint(6000, 15000))

def http_server():
    py_path = sys.path[0]
    real_path = getrelpath(py_path)
    os.chdir(py_path)
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import ThreadingMixIn
    class ThreadingServer(ThreadingMixIn,HTTPServer):
        pass
    serveraddr=('', int(port))   # http://yige.org
    srvr=ThreadingServer(serveraddr,SimpleHTTPRequestHandler)
    srvr.serve_forever()





def getrelpath(input_file):
    user = getpass.getuser()
    user_dir = '/Users/' + user
    os.chdir(user_dir)
    file_relpath = os.path.relpath(input_file)
    return file_relpath

def convert(v_relpath, video_dictionary, video_filename):
    os.system('ffmpeg -i '+v_relpath+' -c:v copy -c:a copy '+video_dictionary+'/'+video_filename.split('.')[0]+'_MP4.mp4')


def main(video_relpath, danmu_relpath):
    #danmu_relpath = getrelpath(danmu_relpath)
    #video_relpath = getrelpath(video_relpath)
    video_filename = video_relpath.split("/")[-1].strip()
    video_dictionary = os.path.dirname(v_relpath)
    danmu_filename = danmu_relpath.split("/")[-1]
    py_path = sys.path[0]
    os.chdir(py_path)
    user = getpass.getuser()
    user_dir = '/Users/' + user
    #print(user_dir)
    real_cache_dir = user_dir + '/.cache/abplayerhtml5_py'
    os.system('rm -rf /'+real_cache_dir)
    os.system('mkdir /'+real_cache_dir)
    os.chdir(py_path)
    os.system('rm -rf ./abpcache')
    os.system('mkdir abpcache')
    video_filename = video_filename.replace('\\', '')
    if 'mp4' not in video_filename[-5:] and 'MP4' not in video_filename[-5:] and 'Mp4' not in video_filename[-5:] and 'mP4'  not in video_filename[-5:] :
        print('Cannot read your file, trying to convert to MP4, need ffmpeg...')
        Process(target=convert(v_relpath, video_dictionary, video_filename), ).start()
        print('I made a MP4 file for you, next time please use the MP4 file directly!')
        video_relpath = video_dictionary+'/'+video_filename.split('.')[0]+'_MP4.mp4'
        video_filename = video_filename.split('.')[0]+'_MP4.mp4'
    print(video_relpath)
    video_filename_url = ''
    video_filename_url = urllib.quote(video_filename)
    os.system('ln -s '+ real_cache_dir+' ./abpcache ')
    os.system('cp /'+ video_relpath+'  '+ real_cache_dir)
    os.system('cp /'+ danmu_relpath+'  '+ real_cache_dir)
    os.system('mv '+real_cache_dir+'/'+danmu_filename +' '+real_cache_dir+'/webpage.html')
    html_to_write = '''<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta http-equiv="X-UA-Compatible" value="IE=9">
		<link rel="stylesheet" href="css/base.css?1" />
		<title>'''+ video_filename + ''' - ABPlayerHTML5PyMac</title>
		<script src="mobile.js"></script>
		<script src="CommentCore.js"></script>
		<script src="libxml.js"></script>
		<script src="Parsers.js"></script>
		<script src="player.js"></script>
		<script type="text/javascript">
			window.addEventListener("load",function(){
				var inst = ABP.bind(document.getElementById("player1"), isMobile());
				CommentLoader("comment.xml", inst.cmManager);
				inst.txtText.focus();
				inst.btnFull.addEventListener("click", function(){
					var player = document.getElementById("player1");
					player.style.position = "fixed";
					player.style.top = "0";
					player.style.bottom = "0";
					player.style.left = "0";
					player.style.right = "0";
					player.style.width = "";
					player.style.height= "";
					inst.cmManager.setBounds();
				});
				inst.txtText.addEventListener("keydown", function(e){
					if(e && e.keyCode === 13){
						if(/^!/.test(this.value)) return; //Leave the internal commands
						inst.txtText.value = "";
					}
				});
				window.abpinst = inst;
			});
		</script>
	</head>
	<body>
		<div id="player1" class="ABP-Unit" style="width:640px;height:480px;" tabindex="1">
			<div class="ABP-Video">
				<div class="ABP-Container"></div>
				<video id="abp-video" autobuffer="true" data-setup="{}">
					<source src="http://localhost:'''+port+'''/abpcache/abplayerhtml5_py/'''+video_filename_url + '''" type="video/mp4">
					<p>Your browser does not support html5 video!</p>
				</video>

			</div>
			<div class="ABP-Text">
				<input type="text">
			</div>
			<div class="ABP-Control">
				<div class="button ABP-Play"></div>
				<div class="progress-bar">
					<div class="bar dark"></div>
					<div class="bar"></div>
				</div>
				<div class="button ABP-CommentShow"></div>
				<div class="button ABP-FullScreen"></div>
			</div>
		</div>
	</body>
</html>'''
    html_to_write = html_to_write.encode("utf8")
    os.chdir(py_path)
    f = open('./webpage.html', "w")
    f.write(html_to_write)
    f.close()
    Process(target=http_server, ).start()
    os.chdir(py_path)
    os.system('cp -R ./*  '  + real_cache_dir+'/')
    webbrowser.open('http://localhost:'+port+'/abpcache/abplayerhtml5_py/webpage.html')


v_relpath = str(input('Vid'))
#v_relpath = v_relpath.encode('utf-8')
X_relpath = str(input('XML'))
#X_relpath = X_relpath.encode('utf-8')

main(v_relpath, X_relpath)