#!/usr/bin/env python
#coding:utf-8
# Author: Beining --<cnbeining#gmail.com>
# Purpose: An HTML5 solution of danmaku playing.
# Created: 12/12/2013

# This code includes appdirs 1.4.0
# appdirs is under MIT license
# https://github.com/ActiveState/appdirs
# MIT LICENSE as in LICENSE file
# Commit version dbf3ff1b66

# This code includes httpd.py
# Used Under License by Author
# Author: Xia Kai --<xiaket@corp.netease.com/xiaket@gmail.com>
# http://xiaket.org/2011/extending-simplehttpserver.html
# Special thanks to him.

'''
ABPlayerHTML5_Py_Mac 1.09.9
Based on ABPlayerHTML5 and ABPlayerHTML5-bilibili-ver
MIT licence
Beining@ACICFG
cnbeining[at]gmail.com
'''

import os
import random
import shutil
import sys
import webbrowser

from appdirs import user_cache_dir
from httpd import main2

reload(sys)
sys.setdefaultencoding('utf-8')

global SELF_PATH, CACHE_DIR, PORT

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = user_cache_dir('ABPlayerHTML5Py', 'cnbeining')
PORT = random.randint(30000, 45000)

#----------------------------------------------------------------------
def main(video_relpath, danmaku_relpath):
    #Get relatiive patch of video and danmaku, or find danmaku
    (video_relpath, danmaku_relpath) = map(lambda x: x.strip().replace('\\', ''), (video_relpath, danmaku_relpath))
    
    video_dictionary = os.path.dirname(video_relpath)
    
    video_filename = os.path.basename(video_relpath)
    (video_filename_bare, video_extension) = os.path.splitext(video_filename)

    if not os.path.exists(danmaku_relpath):
        # No Danmaku path inputed
        for item in os.listdir(video_dictionary):
            if item.startswith(video_filename_bare) and item.lower().endswith('.xml'):
                danmaku_relpath = video_dictionary + "/" + item
                break
    
    danmaku_filename = os.path.basename(danmaku_relpath)
    (danmaku_filename_bare, danmaku_extension) = os.path.splitext(danmaku_filename)
    
    # Prepare the cache dir
    if os.path.exists(CACHE_DIR):  #Force clean the cache
        os.unlink(CACHE_DIR)  # rmtree cannot be used on symlink
    
    local_cache_dir = SELF_PATH + '/cache'  # httpd.py can only run on its own path
    
    if os.path.exists(local_cache_dir):
        shutil.rmtree(local_cache_dir)
    os.makedirs(local_cache_dir)
    
    video_extension_strip = video_extension[1:].lower()
    
    
    # Prepare the webpage
    # TODO: Find a better way to format multiline string like this
    a = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="css/base.css" />
        <link rel="stylesheet" href="css/colpick.css" />
        <title>ABPlayerHTML5Py</title>
        <script src="js/jquery.min.js"></script>
        <script src="js/CommentCoreLibrary.min.js"></script>
        <script src="js/ABPMobile.js"></script>
        <script src="js/ABPLibxml.js"></script>
        <script src="js/ABPlayer.js"></script>
        <script src="js/ColPick.js"></script>
        <script type="text/javascript">
            window.addEventListener("load",function(){
                var inst = ABP.create(document.getElementById("player1"), {
                    src: {
                        playlist: [{
                            video: document.getElementById("video-1"),
                            comments: "/cache/comment.xml"
                        }]
                    },
                    width: "95%",//magic number
                    height: 960,
                    mobile: isMobile()
                });
                window.abpinst = inst;
            });
        </script>
    </head>
    <body>
        <div id="player1">
            <video id="video-1" autobuffer="true" data-setup="{}">
                <source src="http://127.0.0.1:""" + str(PORT) + """/cache/video""" +video_extension + """\" type="video/""" + video_extension_strip + """">
                <p>Your browser does not support html5 video!</p>
            </video>
        </div>
    </body>
</html>
"""
    f = open(SELF_PATH + '/webpage.html', 'w')
    a = str(a.encode("utf8"))
    f.write(a)
    f.close()
    
    
    
    # Time to put our stuff in the cache dir!
    os.symlink(danmaku_relpath, local_cache_dir + '/comment.xml')
    os.symlink(video_relpath, local_cache_dir + '/video' + video_extension)
    os.symlink(SELF_PATH + '/css', local_cache_dir + '/css')
    os.symlink(SELF_PATH + '/js', local_cache_dir + '/js')
    os.symlink(SELF_PATH + '/webpage.html', local_cache_dir + '/webpage.html')
    os.symlink(SELF_PATH + '/favicon.ico', local_cache_dir + '/favicon.ico')
    # Connect to remote cache dir
    os.symlink(local_cache_dir, CACHE_DIR)
    webbrowser.open('http://127.0.0.1:' + str(PORT) + '/cache/webpage.html')
    # Start HTTP server now
    main2(PORT, CACHE_DIR)



v_relpath = raw_input('Vid')
X_relpath = raw_input('XML')
main(v_relpath, X_relpath)


