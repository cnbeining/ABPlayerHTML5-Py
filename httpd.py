#!/usr/bin/env python
#coding=utf-8
"""
Author:         Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com>
Filename:       httpd.py
Type:           httpd that support resume.
Last modified:  2011-06-27 17:38

Description:
"""
import os
import socket
import sys

from SocketServer import ThreadingMixIn
from random import randint
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urllib2
import StringIO
import binascii
import urllib
import atexit


class NotracebackServer(ThreadingMixIn, HTTPServer):
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
        #print('PATH:' + self.path)
        if self.path.startswith('/__proxy__/'):  #Reverse proxy this
            #print()
            url = self.path[11:]
            print(url)
            #request = urllib2.Request(url)
            #response = urllib2.urlopen(request)
            #print(response.code)
            #self.send_response(response.code)
            response = response_copy = urllib.urlopen(url)
            response_code = response.code
            self.send_response(response.code)
            response_headers = response.headers
            [self.send_header(i, response_headers[i]) for i in response_headers]
            #print(self.headers['Origin'])
            try:
                self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
            except:
                self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Credentials', 'true')
            #print(dict(self.response_headers))
            #print('HERE!')
            self.end_headers()
            self.copyfile(response, self.wfile)
            return None
        f = self.send_head()
        if f:
            self.mycopy(f)


    def send_head(self):
        """
        added support for partial content. i'm not surprised if http HEAD
        method would fail.
        """
        
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            # oh, we do not support directory listing.
            self.send_error(404, "File not found")
            return None

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
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            start = start.replace("=", " ")
            self.send_header("Content-Range", "%s%s/%s" % (start, full-1, full))
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


def main(port, server_class=NotracebackServer,
        handler_class=PartialContentHandler):
    os.setpgrp()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    #httpd.serve_forever()
    try:  # Handle connections at the same time, so loading will not fail
        while 1:
            httpd.handle_request()
    except Exception:
        print "Finished"
        os.killpg(os.getpid(), signal.SIGTERM)
        os._exit(0)
    os._exit(0)

#----------------------------------------------------------------------
def main2(port, folder):
    """"""
    
    sys.stdout.flush()
    print(folder)
    ip = '127.0.0.1'
    print("serving on: http://%s:%s/" % (ip, port))
    print("===== local files =====")
    cwd = folder
    for f in os.listdir(cwd):
        if f == sys.argv[0] or f.startswith("."):
            continue
        fullpath = os.path.join(cwd, f)
        if os.path.isfile(fullpath):
            print("link: http://%s:%s/%s" % (ip, port, f))
    print("===== start logging =====\n")
    main(port=port)
    os.killpg(os.getpid(), signal.SIGTERM)
    

if __name__ == "__main__":
    port = 30000
    #ip = socket.gethostbyname(socket.gethostname())
    ip = '127.0.0.1'
    print("serving on: http://%s:%s/" % (ip, port))
    print("===== local files =====")
    cwd = os.getcwd()
    for f in os.listdir(cwd):
        if f == sys.argv[0] or f.startswith("."):
            continue
        fullpath = os.path.join(cwd, f)
        if os.path.isfile(fullpath):
            print("link: http://%s:%s/%s" % (ip, port, f))
    print("===== start logging =====\n")
    main(port=port)