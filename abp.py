# coding=utf-8
'''
ABPlayerHTML5_Py_Mac 1.07.1
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
import socket
from random import randint
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import commands



def getrelpath(input_file):
    '''makes this OSX only...'''
    user = getpass.getuser()
    user_dir = '/Users/' + user
    os.chdir(user_dir)
    file_relpath = os.path.relpath(input_file)
    return file_relpath

reload(sys)
sys.setdefaultencoding('utf-8')
# try to fix the damn code problem
global port
port = str(random.randint(6000, 15000))
# or interesting things would happen...

'''
HTTP Server that supports partial, which would solve Issue #1 :
Author:         Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com>
Filename:       httpd.py
Type:           httpd that support resume.
'''


class NotracebackServer(HTTPServer):

    """
    could make this a mixin, but decide to keep it simple for a simple script.
    """

    def handle_error(self, *args):
        """override default function to disable traceback."""
        pass


class PartialContentHandler(SimpleHTTPRequestHandler):

    def mycopy(self, f):
        """
        This would do the actual file tranfer. if client terminated transfer,
        we would log it.
        """
        py_path = sys.path[0]
        real_path = getrelpath(py_path)
        os.chdir(py_path)
        try:
            self.copyfile(f, self.wfile)
            self.log_message('"%s" %s', self.requestline, "req finished.")
        except socket.error:
            self.log_message('"%s" %s', self.requestline, "req terminated.")
        finally:
            f.close()
        return None

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.mycopy(f)

    def send_head(self):
        """
        added support for partial content. i'm not surprised if http HEAD
        method would fail.
        """
        py_path = sys.path[0]
        real_path = getrelpath(py_path)
        os.chdir(py_path)
        path = self.translate_path(self.path)
        f = None

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        if self.headers.get("Range"):
            # partial content all treated here.
            # we do not support If-Range request.
            # range could only be of the form:
            #   Range: bytes=9855420-
            start = self.headers.get("Range")
            try:
                pos = int(start[6:-1])
            except ValueError:
                self.send_error(400, "bad range specified.")
                f.close()
                return None

            self.send_response(206)
            self.send_header("Content-type", ctype)
            self.send_header("Connection", "keep-alive")
            fs = os.fstat(f.fileno())
            full = fs.st_size
            self.send_header("Content-Length", str(fs[6] - pos))
            self.send_header(
                "Last-Modified",
                self.date_time_string(fs.st_mtime))
            start = start.replace("=", " ")
            self.send_header(
                "Content-Range", "%s%s/%s" %
                (start, full - 1, full))
            self.end_headers()
            f.seek(pos)
            self.mycopy(f)
            return None

        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f


def smain(port, server_class=NotracebackServer,
          handler_class=PartialContentHandler):
    # have to give you a funny name...sorry
    py_path = sys.path[0]
    real_path = getrelpath(py_path)
    os.chdir(py_path)
    server_address = ('', int(port))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def http_server():
    #port = randint(20000, 50000)
    py_path = sys.path[0]
    real_path = getrelpath(py_path)
    os.chdir(py_path)
    ip = socket.gethostbyname(socket.gethostname())
    print "serving on: http://%s:%s/" % (ip, port)
    # used to print local files, ignore it.
    print "===== start logging =====\n"
    smain(port=int(port))


def convert(v_relpath, video_dictionary, video_filename):
    # check: http://www.cnbeining.com/?p=265
    os.system(
        'ffmpeg -i "' +
        v_relpath +
        '" -c:v copy -c:a copy ' +
        video_dictionary +
        '/"' +
        video_filename.split(
            '.')[
            0] +
        '_MP4.mp4"')


def main(video_relpath, danmu_relpath):
    #danmu_relpath = getrelpath(danmu_relpath)
    #video_relpath = getrelpath(video_relpath)
    output = commands.getstatusoutput('ffmpeg --help')
    if str(output[0]) == '32512':
        print('FFmpeg does not exist! Trying to get you a binary, need root...')
        os.system('sudo curl -o /usr/bin/ffmpeg https://raw.githubusercontent.com/superwbd/ABPlayerHTML5-Py--nix/master/ffmpeg')
    video_filename = video_relpath.split("/")[-1].strip()
    video_dictionary = os.path.dirname(v_relpath)
    if danmu_relpath is '':
        danmu_relpath = video_relpath.split('.')[:-1][0] + '.xml'
    # detect the comment file by itself
    danmu_filename = danmu_relpath.split("/")[-1].strip()
    py_path = sys.path[0]
    os.chdir(py_path)
    user = getpass.getuser()
    user_dir = '/Users/' + user
    # print(user_dir)
    try:
        os.system('mkdir '+user_dir+'/.cache/')
    except:
        pass
    real_cache_dir = user_dir + '/.cache/abplayerhtml5_py'
    os.system('rm -rf /' + real_cache_dir)
    os.system('mkdir /' + real_cache_dir)
    os.chdir(py_path)
    os.system('rm -rf ./abpcache')
    # clean up, then do the job
    os.system('mkdir abpcache')
    video_filename = video_filename.replace('\\', '')
    if 'mp4' not in video_filename[-5:].lower():
        print(
            'Cannot read your file, trying to convert to MP4, need ffmpeg...')
        Process(
            target=convert(
                v_relpath,
                video_dictionary,
                video_filename),
        ).start(
        )
        print(
            'I made a MP4 file for you, next time please use the MP4 file directly!')
        video_relpath = video_dictionary + '/' + \
            video_filename.split('.')[0] + '_MP4.mp4'
        video_filename = video_filename.split('.')[0] + '_MP4.mp4'
    print(video_relpath)
    video_filename_url = ''
    video_filename_url = urllib.quote(video_filename)
    os.system('ln -s ' + real_cache_dir + ' ./abpcache ')
    os.system('cp /' + video_relpath + '  ' + real_cache_dir)
    os.system('cp /' + danmu_relpath + '  ' + real_cache_dir + '/comment.xml')
    # in case someone use funny filename in their file...
    os.system(
        'mv ' +
        real_cache_dir +
        '/' +
        danmu_filename +
        ' ' +
        real_cache_dir +
        '/webpage.html')
    html_to_write = '''<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta http-equiv="X-UA-Compatible" value="IE=9">
		<link rel="stylesheet" href="css/base.css?1" />
		<title>''' + video_filename + ''' - ABPlayerHTML5PyMac</title>
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
		<div id="player1" class="ABP-Unit" style="width:1440px;height:900px;" tabindex="1">
			<div class="ABP-Video">
				<div class="ABP-Container"></div>
				<video id="abp-video" autobuffer="true" data-setup="{}">
					<source src="http://localhost:''' + port + '''/abpcache/abplayerhtml5_py/''' + video_filename_url + '''" type="video/mp4">
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
</html>
'''
    html_to_write = html_to_write.encode("utf8")
    os.chdir(py_path)
    f = open('./webpage.html', "w")
    f.write(html_to_write)
    f.close()
    Process(target=http_server, ).start()
    os.chdir(py_path)
    os.system('cp -R ./*  ' + real_cache_dir + '/')
    webbrowser.open(
        'http://localhost:' +
        port +
        '/abpcache/abplayerhtml5_py/webpage.html')


v_relpath = raw_input('Vid')
#v_relpath = v_relpath.encode('utf-8')
X_relpath = raw_input('XML')
#X_relpath = X_relpath.encode('utf-8')

main(v_relpath, X_relpath)
