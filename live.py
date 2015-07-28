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
ABPlayerHTML5_Py_Mac 1.09.91
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
from hashlib import md5
import xmltodict

from appdirs import user_cache_dir
from httpd import main2
import urllib2
import signal
import string
from multiprocessing import Process
from subprocess import Popen, PIPE
import atexit

reload(sys)
sys.setdefaultencoding('utf-8')

global SELF_PATH, CACHE_DIR, PORT, SECRETKEY


SELF_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = user_cache_dir('ABPlayerHTML5Py', 'cnbeining')
PORT = random.randint(30000, 45000)
APPKEY = '85eb6835b0a1034e'
SECRETKEY = '2ad42749773c441109bdc0191257a664'
VER = '0.98.85'
LOCATION_DIR = os.getcwd()


#----------------------------------------------------------------------
def calc_sign(string):
    """str/any->str
    return MD5."""
    return str(md5(str(string).encode('utf-8')).hexdigest())

#----------------------------------------------------------------------
def get_flash_live_address_from_cid(cid):
    """"""
    str_to_hash = 'cid={cid}&player=1&quality=0{SECRETKEY}'.format(cid = cid, SECRETKEY = SECRETKEY)
    url = 'http://live.bilibili.com/api/playurl?cid={cid}&player=1&quality=0&sign={sign}'.format(cid = cid, sign = calc_sign(str_to_hash))
    HEADER = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36',
    'Referer': 'http://live.bilibili.com/' + str(cid),
    'X-Requested-With': 'ShockwaveFlash/18.0.0.209'}
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = response.read()
    #print(data)
    return str(xmltodict.parse(data)['video']['durl']['url'])

#----------------------------------------------------------------------
def main(cid):
    os.setpgrp()
    # Prepare the cache dir
    if os.path.exists(CACHE_DIR):  #Force clean the cache
        os.unlink(CACHE_DIR)  # rmtree cannot be used on symlink
    
    local_cache_dir = SELF_PATH + '/cache'  # httpd.py can only run on its own path
    
    if os.path.exists(local_cache_dir):
        shutil.rmtree(local_cache_dir)
    os.makedirs(local_cache_dir)
    
    live_url = get_flash_live_address_from_cid(cid)
    
    # Prepare the webpage
    with open(SELF_PATH + '/webpage_live_temple.html', 'r') as file_this:
        b = string.Template(file_this.read()).substitute({'PORT': PORT, 'cid': cid})
    with open(SELF_PATH + '/webpage_live.html', 'w+') as file_this:
        file_this.write(b)
    
    
    # Time to put our stuff in the cache dir!
    #os.symlink(danmaku_relpath, local_cache_dir + '/comment.xml')
    os.symlink(SELF_PATH + '/css', local_cache_dir + '/css')
    os.symlink(SELF_PATH + '/js', local_cache_dir + '/js')
    os.symlink(SELF_PATH + '/webpage_live.html', local_cache_dir + '/webpage_live.html')
    os.symlink(SELF_PATH + '/favicon.ico', local_cache_dir + '/favicon.ico')
    # Connect to remote cache dir
    os.symlink(local_cache_dir, CACHE_DIR)
    
    #cmd = ['traceroute', 'google.com']
    
    
    print('INFO: Start HTTP server...')
    p = Process(target=main2 , args=(PORT, CACHE_DIR))
    p.start()
    
    
    ffmpeg_cmd = ['ffmpeg', '-i', live_url, '-c', 'copy', '-map', '0', '-bsf:v', 'h264_mp4toannexb', local_cache_dir + '/out.m3u8']
    print(ffmpeg_cmd)
    print('INFO: Starting ffmpeg...')
    pro = Popen(ffmpeg_cmd, stdout=PIPE, shell=False, preexec_fn=os.setsid)
    
    print('FFMPEG_PID: ' + str(pro.pid))
    print('HTTP SERVER PID: ' + str(p.pid))
    
    #atexit.register(cleanup)
    atexit.register(os.kill, pro.pid, signal.SIGTERM)
    atexit.register(os.killpg, p.pid, signal.SIGTERM)
    atexit.register(os.killpg, 0, signal.SIGKILL)
    
    webbrowser.open('http://127.0.0.1:' + str(PORT) + '/cache/webpage_live.html')
    
    try:
        while True:
            out = pro.stdout.read(1)
            if out == '' and pro.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
    except Exception:  #DIE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pro.kill()
        p.terminate()
        shutil.rmtree(local_cache_dir)
        os.kill(pro.pid, signal.SIGTERM)  #kill ffmpeg
        os.killpg(p.pid, signal.SIGTERM)
        os.killpg(0, signal.SIGKILL)
        os._exit(0)
    finally:
        pro.kill()
        p.terminate()
        shutil.rmtree(local_cache_dir)
        os.kill(pro.pid, signal.SIGTERM)  #kill ffmpeg
        os.killpg(p.pid, signal.SIGTERM)
        os.killpg(0, signal.SIGKILL)
        os._exit(0)
        
    os._exit(0)


#----------------------------------------------------------------------
if __name__=='__main__':
    cid = str(raw_input('cid'))
    main(cid)




